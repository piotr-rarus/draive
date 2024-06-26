from collections.abc import Iterable
from typing import Any

from draive.embedding.embedded import Embedded
from draive.embedding.state import Embedding
from draive.scope import ctx

__all__ = [
    "embed_text",
]


async def embed_text(
    values: Iterable[str],
    **extra: Any,
) -> list[Embedded[str]]:
    return await ctx.state(Embedding).embed_text(
        values=values,
        **extra,
    )
