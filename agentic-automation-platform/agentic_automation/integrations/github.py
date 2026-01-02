"""GitHub API adapter."""

from typing import Any, Dict

import httpx

from agentic_automation.integrations.base import Adapter


class GitHubAdapter(Adapter):
    """GitHub API adapter."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize GitHub adapter.

        Args:
            config: Configuration with 'token' key
        """
        super().__init__(
            adapter_id="github",
            name="GitHub",
            config=config,
        )
        self.token = config.get("token")
        self.base_url = "https://api.github.com"
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json",
            }
        )

    async def authenticate(self) -> bool:
        """Authenticate with GitHub."""
        try:
            response = await self.client.get(f"{self.base_url}/user")
            return response.status_code == 200
        except Exception:
            return False

    async def call(self, method: str, endpoint: str, **kwargs: Any) -> Any:
        """Make a GitHub API call.

        Args:
            method: HTTP method
            endpoint: API endpoint (relative to base URL)
            **kwargs: Additional parameters

        Returns:
            API response
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = await self.client.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    async def get_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository information.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Repository data
        """
        return await self.call("GET", f"repos/{owner}/{repo}")

    async def create_issue(
        self, owner: str, repo: str, title: str, body: str
    ) -> Dict[str, Any]:
        """Create a GitHub issue.

        Args:
            owner: Repository owner
            repo: Repository name
            title: Issue title
            body: Issue body

        Returns:
            Created issue data
        """
        return await self.call(
            "POST",
            f"repos/{owner}/{repo}/issues",
            json={"title": title, "body": body},
        )

