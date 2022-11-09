from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from atomate2 import SETTINGS
from jobflow import Maker, Response, job
from monty.serialization import dumpfn
from monty.shutil import gzip_dir
from pymatgen.core import Structure

_DATA_OBJECTS = []

__all__ = ("BaseLammpsMaker", "lammps_job")


class LammpsInputGenerator:
    ...


class TaskDocument:
    ...


def write_lammps_input_set():
    ...


def lammps_job(method: Callable):
    return job(method, data=_DATA_OBJECTS, output_schema=TaskDocument)


def run_lammps(
    wall_time: int | None = None,
    lammps_cmd: str = SETTINGS.LAMMPS_CMD,
    **run_lammps_kwargs
):
    ...


@dataclass
class BaseLammpsMaker(Maker):
    name: str = "base lammps job"
    input_set_generator: LammpsInputGenerator = field(
        default_factory=LammpsInputGenerator
    )
    write_input_set_kwargs: dict = field(default_factory=dict)
    copy_lammps_kwargs: dict = field(default_factory=dict)
    run_lammps_kwargs: dict = field(default_factory=dict)
    task_document_kwargs: dict = field(default_factory=dict)
    stop_children_kwargs: dict = field(default_factory=dict)
    write_additional_data: dict = field(default_factory=dict)

    @lammps_job
    def make(self, input_structure: Structure | Path):
        """Run a LAMMPS calculation."""
        write_lammps_input_set()

        for filename, data in self.write_additional_data.items():
            dumpfn(data, filename.replace(":", "."))

        run_lammps(**self.run_lammps_kwargs)

        task_doc = TaskDocument.from_directory(Path.cwd(), **self.task_document_kwargs)
        task_doc.task_label = self.name

        gzip_dir(".")

        return Response(output=task_doc)
