from dataclasses import dataclass, field

from jobflow import Flow, Maker
from pymatgen.core import Structure

from .jobs.base import LammpsMaker
from .jobs.core import MinimizationMaker


@dataclass
class FMinimizationMaker(Maker):
    name: str = "minimization"
    minimization_maker: LammpsMaker = field(default_factory=MinimizationMaker)

    def make(self, structure):
        return Flow([self.minimization_maker.make(structure)], name=self.name)
