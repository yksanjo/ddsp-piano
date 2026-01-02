"""Structured logging for agent workflows."""

import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional

from agentic_automation.observability.tracer import Tracer


class StructuredLogger:
    """Structured logger for agent workflows."""

    def __init__(self, name: str, tracer: Optional[Tracer] = None):
        """Initialize structured logger.

        Args:
            name: Logger name
            tracer: Optional tracer for correlation
        """
        self.logger = logging.getLogger(name)
        self.tracer = tracer
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def _get_trace_id(self) -> Optional[str]:
        """Get current trace ID if available."""
        if self.tracer:
            return self.tracer.get_trace_id()
        return None

    def _log(
        self,
        level: int,
        message: str,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a message with structured data.

        Args:
            level: Log level
            message: Log message
            extra: Additional structured data
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "trace_id": self._get_trace_id(),
        }

        if extra:
            log_data.update(extra)

        self.logger.log(level, json.dumps(log_data))

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message."""
        self._log(logging.DEBUG, message, kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message."""
        self._log(logging.INFO, message, kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message."""
        self._log(logging.WARNING, message, kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message."""
        self._log(logging.ERROR, message, kwargs)

    def exception(self, message: str, **kwargs: Any) -> None:
        """Log exception with traceback."""
        self._log(logging.ERROR, message, kwargs, exc_info=True)


def get_logger(name: str, tracer: Optional[Tracer] = None) -> StructuredLogger:
    """Get a structured logger instance.

    Args:
        name: Logger name
        tracer: Optional tracer

    Returns:
        Structured logger instance
    """
    return StructuredLogger(name, tracer)

