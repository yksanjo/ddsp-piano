"""Distributed tracing for agent workflows."""

import contextvars
import time
from typing import Any, Dict, Optional

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.trace import Status, StatusCode

# Context variable for current trace
current_trace_context: contextvars.ContextVar[Optional[Dict[str, Any]]] = (
    contextvars.ContextVar("current_trace_context", default=None)
)


class Tracer:
    """Distributed tracer for agent workflows."""

    def __init__(self, service_name: str = "agentic-automation"):
        """Initialize tracer.

        Args:
            service_name: Name of the service
        """
        self.service_name = service_name
        self.provider = TracerProvider()
        self.provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
        trace.set_tracer_provider(self.provider)
        self.tracer = trace.get_tracer(service_name)

    def start_span(
        self,
        name: str,
        context: Optional[Dict[str, Any]] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Start a new span.

        Args:
            name: Span name
            context: Optional trace context
            attributes: Optional span attributes

        Returns:
            Span context manager
        """
        span = self.tracer.start_as_current_span(name)
        if attributes:
            for key, value in attributes.items():
                span.set_attribute(key, str(value))
        return span

    def set_attribute(self, key: str, value: Any) -> None:
        """Set an attribute on the current span.

        Args:
            key: Attribute key
            value: Attribute value
        """
        span = trace.get_current_span()
        if span:
            span.set_attribute(key, str(value))

    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Add an event to the current span.

        Args:
            name: Event name
            attributes: Optional event attributes
        """
        span = trace.get_current_span()
        if span:
            span.add_event(name, attributes or {})

    def set_status(self, status: StatusCode, description: Optional[str] = None) -> None:
        """Set status on the current span.

        Args:
            status: Status code
            description: Optional description
        """
        span = trace.get_current_span()
        if span:
            span.set_status(Status(status, description))

    def get_trace_id(self) -> Optional[str]:
        """Get the current trace ID.

        Returns:
            Trace ID or None
        """
        span = trace.get_current_span()
        if span:
            span_context = span.get_span_context()
            if span_context.is_valid:
                return format(span_context.trace_id, "032x")
        return None


class TraceContext:
    """Context manager for tracing."""

    def __init__(
        self,
        tracer: Tracer,
        name: str,
        attributes: Optional[Dict[str, Any]] = None,
    ):
        """Initialize trace context.

        Args:
            tracer: Tracer instance
            name: Span name
            attributes: Optional attributes
        """
        self.tracer = tracer
        self.name = name
        self.attributes = attributes
        self.span = None

    def __enter__(self):
        """Enter context."""
        self.span = self.tracer.start_span(self.name, attributes=self.attributes)
        return self.span.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context."""
        if exc_type:
            self.tracer.set_status(StatusCode.ERROR, str(exc_val))
        else:
            self.tracer.set_status(StatusCode.OK)
        return self.span.__exit__(exc_type, exc_val, exc_tb)

