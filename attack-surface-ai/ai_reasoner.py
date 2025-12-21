"""
AI-powered explanation and reasoning for security findings.
Provides plain-English explanations of security risks.
"""
from typing import Dict, List

# Risk explanations mapped by secret type
RISK_EXPLANATIONS = {
    "AWS Access Key": {
        "what": "An AWS Access Key ID that can be used to authenticate to AWS services.",
        "why_dangerous": "Attackers can use this key to access your AWS account, view/modify resources, create new services, and incur charges on your account. They could also exfiltrate data from S3 buckets, databases, or other cloud resources.",
        "attacker_capabilities": [
            "Access and modify your cloud infrastructure",
            "Create new AWS resources and run up charges",
            "Steal data from S3 buckets, databases, or other services",
            "Modify or delete critical resources",
            "Use your account for cryptocurrency mining or other malicious activities"
        ],
        "remediation_steps": [
            "Immediately rotate the AWS access key in the AWS IAM console",
            "Remove the key from all code and commit history",
            "Use AWS Secrets Manager or environment variables instead",
            "Review CloudTrail logs for any unauthorized access",
            "Consider using IAM roles instead of access keys where possible"
        ],
        "severity": "critical"
    },
    "AWS Secret Key": {
        "what": "An AWS Secret Access Key paired with an Access Key ID.",
        "why_dangerous": "This is the private half of AWS credentials. Combined with an Access Key ID, it provides full programmatic access to your AWS account.",
        "attacker_capabilities": [
            "Full access to your AWS account and all services",
            "Complete control over cloud infrastructure",
            "Ability to exfiltrate all data and resources"
        ],
        "remediation_steps": [
            "Rotate the AWS access key pair immediately",
            "Remove from code and git history (consider using git-filter-repo)",
            "Use AWS Secrets Manager, Parameter Store, or environment variables",
            "Enable MFA for all IAM users",
            "Review and restrict IAM permissions using least privilege"
        ],
        "severity": "critical"
    },
    "Stripe Live Key": {
        "what": "A Stripe live API key that can be used to process real payments.",
        "why_dangerous": "This key allows full access to your Stripe account, including charging customer cards, refunding payments, accessing customer data, and modifying your account settings.",
        "attacker_capabilities": [
            "Charge customer credit cards without authorization",
            "Refund payments to their own accounts",
            "Access customer payment information and PII",
            "Modify webhook endpoints to intercept payment events",
            "View and export all transaction history"
        ],
        "remediation_steps": [
            "Immediately revoke the exposed key in Stripe Dashboard",
            "Generate a new API key",
            "Remove the old key from all code and git history",
            "Use environment variables or Stripe's secure key management",
            "Review Stripe logs for any unauthorized transactions",
            "Notify affected customers if data was accessed"
        ],
        "severity": "critical"
    },
    "Stripe Test Key": {
        "what": "A Stripe test API key used for development and testing.",
        "why_dangerous": "While test keys can't process real payments, they can still be used to test your payment flows, access test customer data, and potentially identify vulnerabilities in your payment integration.",
        "attacker_capabilities": [
            "Test payment flows and identify vulnerabilities",
            "Access test customer data",
            "Potentially find ways to escalate to live keys"
        ],
        "remediation_steps": [
            "Rotate the test key in Stripe Dashboard",
            "Remove from code and use environment variables",
            "Ensure test keys are never committed to production repos"
        ],
        "severity": "medium"
    },
    "GitHub Personal Access Token": {
        "what": "A GitHub Personal Access Token (classic) that grants API access to your GitHub account.",
        "why_dangerous": "Depending on scopes, this token can read/write repositories, access private code, modify settings, and potentially access other connected services via GitHub integrations.",
        "attacker_capabilities": [
            "Read and clone private repositories",
            "Push code changes or create malicious commits",
            "Access secrets stored in GitHub Actions or repository settings",
            "Modify repository settings or delete repositories",
            "Access connected services (CI/CD, deployments, etc.)"
        ],
        "remediation_steps": [
            "Immediately revoke the token in GitHub Settings > Developer settings",
            "Review token usage logs in GitHub",
            "Remove the token from all code and git history",
            "Use fine-grained tokens with minimal required scopes",
            "Consider using GitHub Apps instead of personal tokens"
        ],
        "severity": "critical"
    },
    "GitHub OAuth Token": {
        "what": "A GitHub fine-grained Personal Access Token (new format).",
        "why_dangerous": "These tokens have specific permissions but can still access repositories, code, and settings based on their configured scopes.",
        "attacker_capabilities": [
            "Access repositories and code based on token permissions",
            "Modify code and settings if write permissions are granted",
            "Access secrets and environment variables"
        ],
        "remediation_steps": [
            "Revoke the token in GitHub Settings",
            "Remove from code and git history",
            "Use tokens with minimal required permissions",
            "Consider using deploy keys or GitHub Apps for automation"
        ],
        "severity": "critical"
    },
    "Generic API Key": {
        "what": "An API key that provides access to a third-party service or your own API.",
        "why_dangerous": "The risk depends on what the API key can access. It could allow unauthorized access to services, data, or functionality.",
        "attacker_capabilities": [
            "Access the API with the same permissions as the key",
            "Make unauthorized API calls",
            "Access or modify data depending on key permissions",
            "Potentially incur charges or rate limit your legitimate usage"
        ],
        "remediation_steps": [
            "Identify which service the key belongs to",
            "Rotate or revoke the key in the service's dashboard",
            "Remove from code and use environment variables or secrets management",
            "Review API usage logs for unauthorized access",
            "Implement API key rotation policies"
        ],
        "severity": "high"
    },
    "Generic Token": {
        "what": "A generic authentication token or secret that could be used to access services.",
        "why_dangerous": "The exact risk depends on what the token protects, but it likely grants some level of unauthorized access.",
        "attacker_capabilities": [
            "Use the token to authenticate to protected services",
            "Access resources the token is authorized for",
            "Potentially escalate privileges or access additional systems"
        ],
        "remediation_steps": [
            "Identify the service or system the token belongs to",
            "Rotate or revoke the token immediately",
            "Remove from code and use secure storage",
            "Review access logs for the affected service",
            "Implement proper secrets management"
        ],
        "severity": "high"
    },
    "Private Key": {
        "what": "A private cryptographic key (RSA, EC, etc.) used for authentication or encryption.",
        "why_dangerous": "Private keys are meant to be secret. If exposed, attackers can impersonate you, decrypt encrypted data, or access systems that trust this key.",
        "attacker_capabilities": [
            "Impersonate your identity or service",
            "Decrypt encrypted communications or data",
            "Access SSH servers, APIs, or other systems that trust this key",
            "Sign code or commits in your name"
        ],
        "remediation_steps": [
            "Immediately revoke or remove the key from all systems that use it",
            "Generate a new key pair",
            "Remove the private key from code and git history (use git-filter-repo)",
            "Update all systems to use the new public key",
            "Review access logs for systems that used this key",
            "Never commit private keys - use environment variables or secure key management"
        ],
        "severity": "critical"
    },
    "MongoDB Connection String": {
        "what": "A MongoDB connection string containing database credentials.",
        "why_dangerous": "This provides direct access to your database, allowing attackers to read, modify, or delete all data.",
        "attacker_capabilities": [
            "Access and read all database data",
            "Modify or delete data",
            "Create new users or modify permissions",
            "Exfiltrate sensitive information",
            "Potentially access other databases on the same server"
        ],
        "remediation_steps": [
            "Immediately change the database password",
            "Remove the connection string from code and git history",
            "Use environment variables or secrets management",
            "Review database access logs for unauthorized connections",
            "Restrict database network access (firewall, VPC, etc.)",
            "Enable MongoDB authentication and use least privilege users"
        ],
        "severity": "high"
    },
    "PostgreSQL Connection String": {
        "what": "A PostgreSQL database connection string with credentials.",
        "why_dangerous": "Provides direct database access, allowing attackers to read, modify, or delete data, and potentially execute arbitrary SQL.",
        "attacker_capabilities": [
            "Read, modify, or delete all database data",
            "Execute arbitrary SQL commands",
            "Access other databases if permissions allow",
            "Modify database schema or permissions",
            "Exfiltrate sensitive data"
        ],
        "remediation_steps": [
            "Immediately change the database password",
            "Remove connection string from code and git history",
            "Use environment variables or secrets management",
            "Review PostgreSQL logs for unauthorized access",
            "Restrict database network access",
            "Use database users with minimal required permissions"
        ],
        "severity": "high"
    },
    "Slack Token": {
        "what": "A Slack API token that provides access to Slack workspace data and functionality.",
        "why_dangerous": "Depending on scopes, this token can read messages, access files, post messages, or modify workspace settings.",
        "attacker_capabilities": [
            "Read private messages and channels",
            "Access shared files and data",
            "Post messages as your bot or user",
            "Modify workspace settings if permissions allow",
            "Access user information and PII"
        ],
        "remediation_steps": [
            "Revoke the token in Slack App Management settings",
            "Remove from code and use environment variables",
            "Review Slack audit logs for unauthorized access",
            "Use tokens with minimal required scopes",
            "Regenerate the token if needed"
        ],
        "severity": "high"
    },
    "Discord Bot Token": {
        "what": "A Discord bot token that controls a Discord bot application.",
        "why_dangerous": "This token provides full control over the bot, allowing attackers to read messages, post content, manage servers, and access bot data.",
        "attacker_capabilities": [
            "Control the bot's actions and behavior",
            "Read messages in all accessible channels",
            "Post messages, delete messages, or ban users",
            "Access server and user data",
            "Potentially escalate to server admin if bot has high permissions"
        ],
        "remediation_steps": [
            "Immediately regenerate the bot token in Discord Developer Portal",
            "Remove the old token from all code and git history",
            "Review bot activity logs for unauthorized actions",
            "Use environment variables for token storage",
            "Review and restrict bot permissions to minimum required"
        ],
        "severity": "high"
    }
}


def explain_finding(finding: Dict) -> Dict:
    """
    Generate a plain-English explanation of a security finding.
    
    Args:
        finding: A finding dictionary from github_scan
        
    Returns:
        Dictionary with explanation, risk assessment, and remediation steps
    """
    secret_type = finding.get("type", "Unknown")
    explanation = RISK_EXPLANATIONS.get(secret_type, {
        "what": f"An exposed {secret_type.lower()} was found in your code.",
        "why_dangerous": "This credential could be used by attackers to gain unauthorized access to your systems or data.",
        "attacker_capabilities": [
            "Use the credential to access protected resources",
            "Potentially escalate access or cause damage"
        ],
        "remediation_steps": [
            "Immediately rotate or revoke the credential",
            "Remove it from code and git history",
            "Use environment variables or secrets management",
            "Review access logs for unauthorized usage"
        ],
        "severity": finding.get("severity", "high")
    })
    
    return {
        "summary": f"Exposed {secret_type} found in {finding.get('file', 'unknown file')}",
        "what": explanation["what"],
        "why_dangerous": explanation["why_dangerous"],
        "attacker_capabilities": explanation["attacker_capabilities"],
        "remediation_steps": explanation["remediation_steps"],
        "severity": explanation.get("severity", finding.get("severity", "high")),
        "file": finding.get("file"),
        "line_number": finding.get("line_number"),
        "snippet": finding.get("snippet", "")[:200]  # Limit snippet length
    }


def analyze_findings(findings: List[Dict]) -> Dict:
    """
    Analyze a list of findings and provide overall assessment.
    
    Args:
        findings: List of findings from github_scan
        
    Returns:
        Dictionary with overall analysis and prioritized recommendations
    """
    if not findings:
        return {
            "status": "clean",
            "message": "No security exposures detected in the scanned repository.",
            "recommendations": [
                "Continue using environment variables and secrets management",
                "Set up pre-commit hooks to prevent committing secrets",
                "Regularly scan your repositories for exposed credentials"
            ]
        }
    
    # Count by severity
    critical_count = sum(1 for f in findings if f.get("severity") == "critical")
    high_count = sum(1 for f in findings if f.get("severity") == "high")
    medium_count = sum(1 for f in findings if f.get("severity") == "medium")
    
    # Determine overall status
    if critical_count > 0:
        status = "critical"
        message = f"🚨 CRITICAL: {critical_count} critical security exposure(s) found. Immediate action required."
    elif high_count > 0:
        status = "high"
        message = f"⚠️  HIGH: {high_count} high-severity exposure(s) found. Address promptly."
    elif medium_count > 0:
        status = "medium"
        message = f"ℹ️  MEDIUM: {medium_count} medium-severity exposure(s) found."
    else:
        status = "low"
        message = "Low-severity exposures found."
    
    # Get unique file count
    affected_files = len(set(f.get("file") for f in findings))
    
    # Prioritize recommendations
    recommendations = []
    if critical_count > 0:
        recommendations.append("IMMEDIATE: Rotate all critical credentials (AWS keys, Stripe keys, GitHub tokens)")
        recommendations.append("Remove exposed credentials from git history using git-filter-repo")
    if high_count > 0:
        recommendations.append("Rotate high-severity credentials and review access logs")
    recommendations.append("Set up environment variables or secrets management for all credentials")
    recommendations.append("Add pre-commit hooks to prevent committing secrets in the future")
    recommendations.append("Review and restrict permissions on all exposed credentials")
    
    return {
        "status": status,
        "message": message,
        "summary": {
            "total_findings": len(findings),
            "critical": critical_count,
            "high": high_count,
            "medium": medium_count,
            "affected_files": affected_files
        },
        "recommendations": recommendations
    }

