from pathlib import Path
from typing import Type

from atomate2.common.schemas.structure import StructureMetadata
from pydantic import Field


class TaskDocument(StructureMetadata):

    dir_name: str = Field()

    task_label: str = Field()

    @classmethod
    def from_directory(
        cls: Type["TaskDocument"],
        dir_name: str | Path,
    ) -> "TaskDocument":
        return TaskDocument(dir_name=dir_name)

    class Config:
        extras = "allow"
