"""Metrics collection for agent workflows."""

import time
from typing import Any, Dict, Optional

from prometheus_client import Counter, Histogram, Gauge

# Prometheus metrics
agent_executions_total = Counter(
    "agent_executions_total",
    "Total number of agent executions",
    ["agent_id", "status"],
)

agent_execution_duration = Histogram(
    "agent_execution_duration_seconds",
    "Agent execution duration in seconds",
    ["agent_id"],
)

workflow_executions_total = Counter(
    "workflow_executions_total",
    "Total number of workflow executions",
    ["workflow_id", "status"],
)

workflow_execution_duration = Histogram(
    "workflow_execution_duration_seconds",
    "Workflow execution duration in seconds",
    ["workflow_id"],
)

active_executions = Gauge(
    "active_executions",
    "Number of currently active executions",
    ["type"],  # "agent" or "workflow"
)

llm_tokens_total = Counter(
    "llm_tokens_total",
    "Total LLM tokens used",
    ["model", "type"],  # type: "prompt" or "completion"
)

llm_cost_total = Counter(
    "llm_cost_total",
    "Total LLM cost in USD",
    ["model"],
)


class MetricsCollector:
    """Collects metrics for agent workflows."""

    def __init__(self):
        """Initialize metrics collector."""
        pass

    def record_agent_execution(
        self,
        agent_id: str,
        status: str,
        duration: float,
        tokens: Optional[Dict[str, int]] = None,
        cost: Optional[float] = None,
    ) -> None:
        """Record an agent execution.

        Args:
            agent_id: Agent identifier
            status: Execution status
            duration: Execution duration in seconds
            tokens: Token usage
            cost: Cost in USD
        """
        agent_executions_total.labels(agent_id=agent_id, status=status).inc()
        agent_execution_duration.labels(agent_id=agent_id).observe(duration)

        if tokens:
            for token_type, count in tokens.items():
                llm_tokens_total.labels(model=agent_id, type=token_type).inc(count)

        if cost:
            llm_cost_total.labels(model=agent_id).inc(cost)

    def record_workflow_execution(
        self,
        workflow_id: str,
        status: str,
        duration: float,
    ) -> None:
        """Record a workflow execution.

        Args:
            workflow_id: Workflow identifier
            status: Execution status
            duration: Execution duration in seconds
        """
        workflow_executions_total.labels(workflow_id=workflow_id, status=status).inc()
        workflow_execution_duration.labels(workflow_id=workflow_id).observe(duration)

    def increment_active_executions(self, execution_type: str) -> None:
        """Increment active executions counter.

        Args:
            execution_type: Type of execution ("agent" or "workflow")
        """
        active_executions.labels(type=execution_type).inc()

    def decrement_active_executions(self, execution_type: str) -> None:
        """Decrement active executions counter.

        Args:
            execution_type: Type of execution ("agent" or "workflow")
        """
        active_executions.labels(type=execution_type).dec()

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics snapshot.

        Returns:
            Dictionary of metrics
        """
        # This would collect metrics from Prometheus
        # For now, return placeholder
        return {
            "agent_executions_total": "N/A",
            "workflow_executions_total": "N/A",
            "active_executions": "N/A",
        }


class ExecutionTimer:
    """Context manager for timing executions."""

    def __init__(self, metrics_collector: MetricsCollector, execution_type: str, execution_id: str):
        """Initialize timer.

        Args:
            metrics_collector: Metrics collector
            execution_type: Type of execution ("agent" or "workflow")
            execution_id: Execution identifier
        """
        self.metrics_collector = metrics_collector
        self.execution_type = execution_type
        self.execution_id = execution_id
        self.start_time = None

    def __enter__(self):
        """Start timing."""
        self.start_time = time.time()
        self.metrics_collector.increment_active_executions(self.execution_type)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop timing and record metrics."""
        duration = time.time() - self.start_time
        status = "failed" if exc_type else "completed"

        if self.execution_type == "agent":
            self.metrics_collector.record_agent_execution(
                self.execution_id, status, duration
            )
        elif self.execution_type == "workflow":
            self.metrics_collector.record_workflow_execution(
                self.execution_id, status, duration
            )

        self.metrics_collector.decrement_active_executions(self.execution_type)

