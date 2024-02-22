from collections.abc import Iterable
from typing import TypeVar

from draive.openai.chat import openai_chat_completion
from draive.openai.config import OpenAIChatConfig
from draive.scope import ctx
from draive.types import ConversationMessage, StringConvertible, Toolset
from draive.types.generated import Generated

__all__ = [
    "openai_generate",
    "openai_generate_text",
]

_Generated = TypeVar(
    "_Generated",
    bound=Generated,
)

INSTRUCTION: str = """\
{instruction}

Please respond using only a JSON with following structure:
{format}
"""


async def openai_generate_text(
    *,
    instruction: str,
    input: StringConvertible,  # noqa: A002
    toolset: Toolset | None = None,
    examples: Iterable[tuple[str, str]] | None = None,
) -> str:
    return await openai_chat_completion(
        instruction=instruction,
        input=input,
        history=(
            [
                message
                for example in examples
                for message in [
                    ConversationMessage(
                        author="user",
                        content=example[0],
                    ),
                    ConversationMessage(
                        author="assistant",
                        content=example[1],
                    ),
                ]
            ]
            if examples
            else None
        ),
        toolset=toolset,
    )


async def openai_generate(
    model: type[_Generated],
    *,
    instruction: str,
    input: StringConvertible,  # noqa: A002
    toolset: Toolset | None = None,
    examples: Iterable[tuple[str, _Generated]] | None = None,
) -> _Generated:
    with ctx.updated(
        ctx.state(OpenAIChatConfig).updated(
            response_format={"type": "json_object"},
        )
    ):
        return model.from_json(
            value=await openai_chat_completion(
                instruction=INSTRUCTION.format(
                    instruction=instruction,
                    format=model.specification(),
                ),
                input=input,
                history=(
                    [
                        message
                        for example in examples
                        for message in [
                            ConversationMessage(
                                author="user",
                                content=example[0],
                            ),
                            ConversationMessage(
                                author="assistant",
                                content=example[1].__str__(),
                            ),
                        ]
                    ]
                    if examples
                    else None
                ),
                toolset=toolset,
            )
        )
