from dataclasses import dataclass, field

from pymatgen.io.lammps_new.sets import LammpsMinimization, BaseLammpsGenerator

from ..jobs.base import BaseLammpsMaker


@dataclass
class MinimizationMaker(BaseLammpsMaker):
    name: str = "minimization"
    input_set_generator: BaseLammpsGenerator = field(default_factory=LammpsMinimization)
