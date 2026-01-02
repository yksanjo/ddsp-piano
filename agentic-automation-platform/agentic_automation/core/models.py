"""Data models for the agentic automation platform."""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class LLMBackend(str, Enum):
    """Supported LLM backends."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    MOCK = "mock"  # For testing


class TaskType(str, Enum):
    """Types of workflow tasks."""

    AGENT = "agent"
    TOOL = "tool"
    CONDITION = "condition"
    LOOP = "loop"
    PARALLEL = "parallel"
    HUMAN_IN_LOOP = "human_in_loop"


class MemoryConfig(BaseModel):
    """Configuration for agent memory."""

    short_term_enabled: bool = True
    long_term_enabled: bool = False
    max_context_tokens: int = 8000
    summarization_threshold: int = 6000
    vector_db_provider: Optional[str] = None  # "weaviate", "qdrant", etc.


class RetryConfig(BaseModel):
    """Configuration for retry logic."""

    max_retries: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True


class ErrorHandlingConfig(BaseModel):
    """Configuration for error handling."""

    on_error: str = "fail"  # "fail", "retry", "skip", "continue"
    error_notification: Optional[str] = None
    fallback_task: Optional[str] = None


class AgentDefinition(BaseModel):
    """Definition of an agent."""

    id: str
    name: str
    description: str
    llm_backend: LLMBackend = LLMBackend.OPENAI
    model: str = "gpt-4"
    system_prompt: str
    tools: List[str] = Field(default_factory=list)  # Tool IDs
    memory_config: MemoryConfig = Field(default_factory=MemoryConfig)
    max_iterations: int = 10
    temperature: float = 0.7
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ToolDefinition(BaseModel):
    """Definition of a tool."""

    id: str
    name: str
    description: str
    function_schema: Dict[str, Any]  # JSON Schema for function
    implementation: Optional[str] = None  # Python code or module path
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TaskDefinition(BaseModel):
    """Definition of a workflow task."""

    id: str
    name: str
    type: TaskType
    agent_id: Optional[str] = None
    tool_id: Optional[str] = None
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, str] = Field(default_factory=dict)  # output_name -> task_id.input_name
    condition: Optional[str] = None  # For conditional tasks
    loop_config: Optional[Dict[str, Any]] = None  # For loop tasks
    retry_config: RetryConfig = Field(default_factory=RetryConfig)
    error_handling: ErrorHandlingConfig = Field(default_factory=ErrorHandlingConfig)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class WorkflowDefinition(BaseModel):
    """Definition of a workflow."""

    id: str
    name: str
    version: str = "1.0.0"
    description: str = ""
    tasks: List[TaskDefinition]
    dependencies: Dict[str, List[str]] = Field(
        default_factory=dict
    )  # task_id -> [dependency_ids]
    retry_config: RetryConfig = Field(default_factory=RetryConfig)
    error_handling: ErrorHandlingConfig = Field(default_factory=ErrorHandlingConfig)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ExecutionState(str, Enum):
    """State of workflow/agent execution."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ExecutionResult(BaseModel):
    """Result of an execution."""

    execution_id: str
    state: ExecutionState
    result: Optional[Any] = None
    error: Optional[str] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)
    trace_id: Optional[str] = None

