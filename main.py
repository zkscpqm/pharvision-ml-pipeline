import argparse
from pathlib import Path


def main(pipeline_file: Path, n_cores: int):
    if not pipeline_file.is_file():
        print(f"The pipeline file {pipeline_file} does not exist. Exiting!")
        exit(1)
    if n_cores < 1:
        print(f"At least 1 CPU core required to calculate pipeline! Got: {n_cores}")
        exit(1)
    print(f"OK! {pipeline_file} {n_cores}")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog="ML Pipeline Optimizer")
    parser.add_argument('--pipeline', type=str, help='Path to file containing ML pipeline steps', required=True)
    parser.add_argument('--cpu_cores', type=int, help='sum the integers (default: find the max)', default=1)

    args = parser.parse_args()
    main(
        pipeline_file=Path(args.pipeline).absolute(),
        n_cores=args.cpu_cores
    )
