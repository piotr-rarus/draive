from collections.abc import Iterable
from typing import Any

from draive.generation.text.state import TextGeneration
from draive.lmm import Toolbox
from draive.scope import ctx
from draive.types import Instruction, MultimodalContent, MultimodalContentElement

__all__ = [
    "generate_text",
]


async def generate_text(
    *,
    instruction: Instruction | str,
    input: MultimodalContent | MultimodalContentElement,  # noqa: A002
    tools: Toolbox | None = None,
    examples: Iterable[tuple[MultimodalContent | MultimodalContentElement, str]] | None = None,
    **extra: Any,
) -> str:
    return await ctx.state(TextGeneration).generate(
        instruction=instruction,
        input=input,
        tools=tools,
        examples=examples,
        **extra,
    )
