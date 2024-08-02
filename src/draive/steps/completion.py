from collections.abc import Iterable
from typing import Any, Protocol, runtime_checkable

from draive.instructions import Instruction
from draive.steps.model import Step
from draive.types import MultimodalContent, MultimodalContentConvertible

__all__ = [
    "StepsCompletion",
]


@runtime_checkable
class StepsCompletion(Protocol):
    async def __call__(
        self,
        *,
        instruction: Instruction | str,
        steps: Iterable[Step | MultimodalContent | MultimodalContentConvertible],
        **extra: Any,
    ) -> MultimodalContent: ...
