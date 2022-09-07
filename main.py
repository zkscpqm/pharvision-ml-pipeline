import argparse
from pathlib import Path

from src.executor import PipelineExecutor
from src.pipeline import MLPipeline


def _dbg_print(pipeline: MLPipeline):
    for _, comp in pipeline._component_map.items():
        print(comp)
    for group_name, group in pipeline._group_map.items():
        print(f"{group_name} -> {[c.name for c in group]}")


def main(pipeline_file: Path, target: str, n_cores: int, save_to: Path, show: bool):
    if not pipeline_file.is_file():
        print(f"The pipeline file {pipeline_file} does not exist. Exiting!")
        exit(1)
    if n_cores < 1:
        print(f"At least 1 CPU core required to calculate pipeline! Got: {n_cores}")
        exit(1)
    save_location = save_to / (f"{n_cores}_" + pipeline_file.name.rstrip(".txt") + "_REPORT.txt")

    pipeline = MLPipeline.from_file(pipeline_definition=pipeline_file)
    executor = PipelineExecutor(cores=n_cores)
    # _dbg_print(pipeline)

    line = pipeline.execution_line(target)

    executor.execute(line)

    executor.get_report(save_to=save_location, show=show)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog="ML Pipeline Optimizer")
    parser.add_argument('--pipeline', type=str, help='Path to file containing ML pipeline steps', required=True)
    parser.add_argument('--target', type=str, help='Which component to build', required=True)
    parser.add_argument('--cpu_cores', type=int, help='Number of parallel executions allowed', default=1)
    parser.add_argument('--save_to', type=str, help='Directory where the report should be saved', default='.')
    parser.add_argument('--show', type=bool, help='Should the report be flushed to stdout?', default=False)

    args = parser.parse_args()
    main(
        pipeline_file=Path(args.pipeline).absolute(),
        target=args.target,
        n_cores=args.cpu_cores,
        save_to=Path(args.save_to).absolute(),
        show=args.show,
    )
