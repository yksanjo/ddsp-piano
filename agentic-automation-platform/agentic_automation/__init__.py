"""
Agentic AI Automation Platform

A production-ready automation platform for the agentic AI era.
"""

__version__ = "0.1.0"

from agentic_automation.core.agent import Agent
from agentic_automation.core.workflow import Workflow
from agentic_automation.orchestrator import Orchestrator

__all__ = [
    "Agent",
    "Workflow",
    "Orchestrator",
]

