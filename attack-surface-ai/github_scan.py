"""
GitHub repository scanner for detecting exposed secrets and credentials.
"""
import requests
import re
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

GITHUB_API = "https://api.github.com"

# Comprehensive secret patterns
SECRET_PATTERNS = {
    "AWS Access Key": {
        "pattern": r"AKIA[0-9A-Z]{16}",
        "severity": "critical"
    },
    "AWS Secret Key": {
        "pattern": r"(?i)(aws_secret_access_key|aws_secret_key)\s*[=:]\s*['\"]?([A-Za-z0-9/+=]{40})['\"]?",
        "severity": "critical"
    },
    "Stripe Live Key": {
        "pattern": r"sk_live_[0-9a-zA-Z]{24,}",
        "severity": "critical"
    },
    "Stripe Test Key": {
        "pattern": r"sk_test_[0-9a-zA-Z]{24,}",
        "severity": "medium"
    },
    "GitHub Personal Access Token": {
        "pattern": r"ghp_[0-9a-zA-Z]{36}",
        "severity": "critical"
    },
    "GitHub OAuth Token": {
        "pattern": r"github_pat_[0-9a-zA-Z_]{82}",
        "severity": "critical"
    },
    "Generic API Key": {
        "pattern": r"(?i)(api[_-]?key|apikey)\s*[=:]\s*['\"]?([0-9a-zA-Z\-_]{20,})['\"]?",
        "severity": "high"
    },
    "Generic Token": {
        "pattern": r"(?i)(token|secret|password)\s*[=:]\s*['\"]?([0-9a-zA-Z\-_]{20,})['\"]?",
        "severity": "high"
    },
    "Private Key": {
        "pattern": r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----",
        "severity": "critical"
    },
    "MongoDB Connection String": {
        "pattern": r"mongodb\+srv://[^\s'\"]+",
        "severity": "high"
    },
    "PostgreSQL Connection String": {
        "pattern": r"postgresql://[^\s'\"]+",
        "severity": "high"
    },
    "Slack Token": {
        "pattern": r"xox[baprs]-[0-9a-zA-Z\-]{10,}",
        "severity": "high"
    },
    "Discord Bot Token": {
        "pattern": r"[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}",
        "severity": "high"
    }
}

# Files to skip (binary, large, or irrelevant)
SKIP_PATTERNS = [
    r"\.(png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot|mp4|mp3|wav|pdf|zip|tar|gz)$",
    r"node_modules",
    r"\.git",
    r"package-lock\.json",
    r"yarn\.lock",
    r"\.min\.(js|css)",
    r"\.map$"
]

MAX_FILE_SIZE = 1024 * 1024  # 1MB max file size


def should_skip_file(file_path: str) -> bool:
    """Check if a file should be skipped during scanning."""
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, file_path, re.IGNORECASE):
            return True
    return False


def scan_file_content(content: str, file_path: str) -> List[Dict]:
    """Scan file content for secrets."""
    findings = []
    
    for secret_type, config in SECRET_PATTERNS.items():
        matches = re.finditer(config["pattern"], content, re.MULTILINE)
        for match in matches:
            # Extract a snippet around the match for context
            start = max(0, match.start() - 50)
            end = min(len(content), match.end() + 50)
            snippet = content[start:end].replace('\n', ' ').strip()
            
            findings.append({
                "type": secret_type,
                "severity": config["severity"],
                "file": file_path,
                "match": match.group(0)[:50],  # Truncate long matches
                "snippet": snippet,
                "line_number": content[:match.start()].count('\n') + 1
            })
    
    return findings


def scan_repo_contents(owner: str, repo: str, token: str, path: str = "", max_depth: int = 10) -> List[Dict]:
    """
    Recursively scan repository contents for secrets.
    
    Args:
        owner: GitHub username or organization
        repo: Repository name
        token: GitHub personal access token
        path: Current path in repository (for recursion)
        max_depth: Maximum recursion depth
    
    Returns:
        List of findings
    """
    if max_depth <= 0:
        return []
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    findings = []
    
    try:
        # Get contents of current path
        if path:
            contents_url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
        else:
            contents_url = f"{GITHUB_API}/repos/{owner}/{repo}/contents"
        
        response = requests.get(contents_url, headers=headers, timeout=10)
        
        if response.status_code == 404:
            logger.warning(f"Path not found: {path}")
            return findings
        elif response.status_code != 200:
            logger.error(f"API error {response.status_code}: {response.text}")
            return findings
        
        items = response.json()
        
        # Handle single file response
        if isinstance(items, dict):
            items = [items]
        
        for item in items:
            if item.get("type") == "file":
                file_path = item.get("path", item.get("name", ""))
                
                # Skip files that shouldn't be scanned
                if should_skip_file(file_path):
                    continue
                
                # Skip large files
                if item.get("size", 0) > MAX_FILE_SIZE:
                    logger.debug(f"Skipping large file: {file_path}")
                    continue
                
                # Download and scan file content
                download_url = item.get("download_url")
                if not download_url:
                    continue
                
                try:
                    file_response = requests.get(download_url, timeout=10)
                    if file_response.status_code == 200:
                        content = file_response.text
                        file_findings = scan_file_content(content, file_path)
                        findings.extend(file_findings)
                except Exception as e:
                    logger.warning(f"Error scanning file {file_path}: {e}")
                    continue
                    
            elif item.get("type") == "dir":
                # Recursively scan subdirectories
                sub_path = item.get("path", "")
                if sub_path:
                    sub_findings = scan_repo_contents(
                        owner, repo, token, sub_path, max_depth - 1
                    )
                    findings.extend(sub_findings)
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error scanning {path}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error scanning {path}: {e}")
    
    return findings


def scan_repo(owner: str, repo: str, token: str) -> Dict:
    """
    Scan a GitHub repository for exposed secrets.
    
    Args:
        owner: GitHub username or organization
        repo: Repository name
        token: GitHub personal access token
    
    Returns:
        Dictionary with scan results
    """
    logger.info(f"Scanning {owner}/{repo}")
    
    findings = scan_repo_contents(owner, repo, token)
    
    # Deduplicate findings (same secret in same file)
    seen = set()
    unique_findings = []
    for finding in findings:
        key = (finding["file"], finding["type"], finding["match"])
        if key not in seen:
            seen.add(key)
            unique_findings.append(finding)
    
    # Count by severity
    severity_counts = {
        "critical": sum(1 for f in unique_findings if f["severity"] == "critical"),
        "high": sum(1 for f in unique_findings if f["severity"] == "high"),
        "medium": sum(1 for f in unique_findings if f["severity"] == "medium"),
        "low": sum(1 for f in unique_findings if f["severity"] == "low")
    }
    
    return {
        "repo": f"{owner}/{repo}",
        "total_findings": len(unique_findings),
        "severity_counts": severity_counts,
        "findings": unique_findings
    }

