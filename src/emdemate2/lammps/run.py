from pydantic import BaseSettings, Field
import subprocess

class LammpsSettings(BaseSettings):

    LAMMPS_CMD: str = Field("lmp", description="The command to run LAMMPS.")

LAMMPS_SETTINGS = LammpsSettings()


def run_lammps(
    lammps_input_file: str,
    lammps_cmd: str = LAMMPS_SETTINGS.LAMMPS_CMD,
    mpi_cmd: str = "mpirun",
    omp_num_threads: int = 1,
    mpi_num_processes: int = 1,
    max_walltime: int | None = None,
) -> None:
    stdout = open("stdout.log", "a") 
    stderr = open("stderr.log", "a")
    process = subprocess.Popen(
        [f"OMP_NUM_THREADS={omp_num_threads}", mpi_cmd, "-n", mpi_num_processes, lammps_cmd, "-in", lammps_input_file], stdout=stdout, stderr=stderr
    )

    try:
        process.communicate(timeout=max_walltime)
    except subprocess.TimeoutExpired:
        process.terminate()

    return

