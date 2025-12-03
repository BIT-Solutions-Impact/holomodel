import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StructuredOutput(BaseModel):
    """Base structured output."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_serialization_defaults_required=True,
        json_schema_mode_override="serialization",
        use_attribute_docstrings=True,
        revalidate_instances="always",
        validate_assignment=True,
        validate_default=True,
    )

    @classmethod
    def get_snake_case_name(cls) -> str:
        """Get snake case name."""
        name = cls.__name__
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()

    @classmethod
    def get_json_schema(cls) -> dict:
        """Get the json schema."""
        return {
            "json_schema": {
                "name": cls.get_snake_case_name(),
                "schema": cls.model_json_schema(),
                "description": cls.__doc__ or "",
                "strict": True,
            },
            "type": "json_schema",
        }

    @classmethod
    def get_only_properties_schema(cls) -> dict:
        """Get the json schema properties."""
        schema = cls.model_json_schema()
        return schema


class BaseAction(StructuredOutput):
    """Base action."""

    action: str


class AbsClickElementAction(BaseAction):
    """Click at coordinates of a web element identified by its description."""

    action: Literal["click_element"] = "click_element"
    element: str
    """text description of the element"""
    x: int
    """The x coordinate, number of pixels from the left edge."""
    y: int
    """The y coordinate, number of pixels from the top edge."""


class AbsWriteElementAction(BaseAction):
    """Write content at coordinates of a web element identified by its description. Don't Enter at the end."""

    action: Literal["write_element"] = "write_element"
    content: str
    """Content to write"""
    element: str
    """Text description of the element and the text it contains"""
    x: int
    """The x coordinate, number of pixels from the left edge."""
    y: int
    """The y coordinate, number of pixels from the top edge."""


class ScrollAction(BaseAction):
    """Scroll in a specified direction."""

    action: Literal["scroll"] = "scroll"
    direction: Literal["up", "down", "left", "right"] = "down"
    """The direction to scroll in"""


class GoBackAction(BaseAction):
    """Go back to the previous screen."""

    action: Literal["go_back"] = "go_back"


class RefreshAction(BaseAction):
    """Refresh the current page."""

    action: Literal["refresh"] = "refresh"


class WaitAction(BaseAction):
    """Wait for screen changes or page load."""

    action: Literal["wait"] = "wait"


class RestartAction(BaseAction):
    """Restart the task from the beginning."""

    action: Literal["restart"] = "restart"


class AnswerAction(BaseAction):
    """Return a final answer to the task. This is the last action to call in an episode."""

    action: Literal["answer"] = "answer"
    content: str
    """The answer content"""


WebAgentNavigateAction = (
    AbsClickElementAction
    | AbsWriteElementAction
    | ScrollAction
    | GoBackAction
    | RefreshAction
    | WaitAction
    | RestartAction
    | AnswerAction
)


class AbsWebAgentNavigate(StructuredOutput):
    """Output of the Web navigation agent."""

    thought: str = ""
    """Brief thoughts, summarizing the reasoning steps that will help answer the task."""
    notes: str = ""
    """Information extracted (i.e. captionned) from the screenshots relevant to the task"""
    action: WebAgentNavigateAction
    """The action to perform"""


class NavigationState(BaseModel):
    task: str = Field(description="The task to solve")
    previous_actions: str = Field(description="The previous actions taken by the agent")

    step: str = Field(description="The current step the agent is trying to achieve to solve the task", default="")
    notes: str = Field(description="The previous notes taken by the agent", default="")
    force_answer: bool = False
    screenshots: list[str] = Field(description="The last N screenshots.")


class WebAgentAnswer(StructuredOutput):
    """Output of the Web answer agent."""

    thought: str = ""
    """Brief thoughts, summarizing the reasoning steps that will help answer the task."""
    notes: str
    """Information extracted (i.e. captionned) from the screenshots relevant to the task"""
    action: AnswerAction
