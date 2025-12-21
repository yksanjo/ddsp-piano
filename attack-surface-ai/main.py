"""
AI-native Attack Surface Intelligence Platform
FastAPI application for scanning GitHub repositories and explaining security findings.
"""
import os
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from github_scan import scan_repo
from ai_reasoner import explain_finding, analyze_findings

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Attack Surface Guard",
    description="Automatically discover, explain, and help fix public security exposures",
    version="0.1.0"
)


class ScanResponse(BaseModel):
    """Response model for scan endpoint."""
    repo: str
    status: str
    message: str
    summary: dict
    total_findings: int
    findings: list
    recommendations: list


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": "AI Attack Surface Guard",
        "version": "0.1.0",
        "description": "Automatically discover, explain, and help fix public security exposures",
        "endpoints": {
            "/scan": "Scan a GitHub repository for exposed secrets",
            "/health": "Health check endpoint",
            "/docs": "API documentation (Swagger UI)"
        }
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/scan", response_model=ScanResponse)
def scan(
    owner: str = Query(..., description="GitHub username or organization"),
    repo: str = Query(..., description="Repository name"),
    token: Optional[str] = Query(None, description="GitHub personal access token (or set GITHUB_TOKEN env var)")
):
    """
    Scan a GitHub repository for exposed secrets and credentials.
    
    Returns:
        - Scan results with findings
        - AI-powered explanations for each finding
        - Risk assessment and remediation steps
    """
    # Get token from parameter or environment
    github_token = token or os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        raise HTTPException(
            status_code=400,
            detail="GitHub token required. Provide via 'token' parameter or GITHUB_TOKEN environment variable."
        )
    
    try:
        logger.info(f"Starting scan for {owner}/{repo}")
        
        # Scan repository
        scan_results = scan_repo(owner, repo, github_token)
        
        # Analyze findings with AI explanations
        findings_with_explanations = []
        for finding in scan_results.get("findings", []):
            explanation = explain_finding(finding)
            findings_with_explanations.append({
                "finding": finding,
                "analysis": explanation
            })
        
        # Get overall analysis
        overall_analysis = analyze_findings(scan_results.get("findings", []))
        
        return ScanResponse(
            repo=scan_results["repo"],
            status=overall_analysis["status"],
            message=overall_analysis["message"],
            summary=overall_analysis.get("summary", {}),
            total_findings=scan_results["total_findings"],
            findings=findings_with_explanations,
            recommendations=overall_analysis.get("recommendations", [])
        )
    
    except Exception as e:
        logger.error(f"Error scanning repository: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error scanning repository: {str(e)}"
        )


@app.get("/scan/org")
def scan_org(
    org: str = Query(..., description="GitHub organization name"),
    token: Optional[str] = Query(None, description="GitHub personal access token")
):
    """
    Scan all repositories in a GitHub organization.
    
    Note: This is a placeholder for future implementation.
    """
    github_token = token or os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        raise HTTPException(
            status_code=400,
            detail="GitHub token required"
        )
    
    return {
        "message": "Organization scanning coming soon",
        "org": org
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

