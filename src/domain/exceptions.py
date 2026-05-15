from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from functools import partial
from typing import Any, ClassVar


def _dict_factory_excluding(
    excluded: tuple[str, ...],
    items: list[tuple[str, Any]],
) -> dict[str, Any]:
    return {k: v for k, v in items if k not in excluded and v is not None}


@dataclass
class DomainException(Exception):
    alias: ClassVar[str]
    description_template: ClassVar[str]

    @property
    def params(self) -> dict[str, Any]:
        return dataclasses.asdict(
            self,
            dict_factory=partial(_dict_factory_excluding, ("alias", "description_template")),
        )

    @property
    def description(self) -> str:
        return self.description_template.format(**self.params)

    def __str__(self) -> str:
        return self.description
