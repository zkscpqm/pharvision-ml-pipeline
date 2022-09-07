import time
from pathlib import Path
from typing import Iterator, Callable

from src.component import Component


class PipelineExecutor:

    def __init__(self, cores: int):
        self._n_cores: int = cores
        self._passed: set[str] = set()
        self._pool: list[Component] = []
        self._current_group: str | None = None
        self._time: int = 0
        self._component_start_times: dict[str, int] = {}
        self._report: list[tuple[str, str]] = []

    def can_execute(self, component: Component) -> bool:
        if len(self._pool) == 0:
            return True
        for dep in component.dependencies:
            if dep.name not in self._passed:
                return False
        return len(self._pool) < self._n_cores and component.group == self._current_group

    def _is_finished(self, component: Component) -> bool:
        return self._time - self._component_start_times[component.name] >= component.execution_time

    def add_component(self, component: Component):
        if not self.can_execute(component):
            raise RuntimeError(f"Cannot execute component {component} group: {self._current_group}), cores: {len(self._pool)}/{self._n_cores}")
        if len(self._pool) == 0:
            self._current_group = component.group
        self._pool.append(component)
        self._component_start_times[component.name] = self._time

    def cycle(self):
        self._time += 1
        self._report.append((",".join((t.name for t in self._pool)), self._current_group))
        done = []
        for i, comp in enumerate(self._pool):
            if self._is_finished(comp):
                self._passed.add(comp.name)
                done.append(i)
        for i in done[::-1]:
            self._pool.pop(i)

    def execute(self, line: list[Component]) -> int:
        while len(line) > 0:
            grouped = []
            group = line[0].group
            while len(line) > 0:
                if line[0].group != group:
                    break
                else:
                    grouped.append(line.pop(0))

            for component in _yield_until_empty(grouped, self.can_execute):
                if not component:
                    self.cycle()
                else:
                    self.add_component(component)
            while len(self._pool) > 0:
                self.cycle()
        return len(self._report)

    def get_report(self, save_to: Path = None, show: bool = True) -> list[tuple[str, str]]:
        rep_s = self._report_formatted()
        if save_to:
            save_to.parent.mkdir(parents=True, exist_ok=True)
            with open(save_to, 'w') as report_file:
                report_file.write(rep_s)
        if show:
            print(rep_s)
        return self._report

    def _report_formatted(self) -> str:
        s = ""
        t_header = "Time"
        exec_header = "Tasks being executed"
        group_header = "Executing Group Name"
        s += f"| {t_header} | {exec_header} | {group_header} \n"
        s += f"| {'-' * len(t_header)} | {'-' * len(exec_header)} | {'-' * len(group_header)} \n"
        for i, (tasks, group) in enumerate(self._report):
            s += f"| {str(i):<{len(t_header)}} | {tasks:<{len(exec_header)}} | {group:<{len(group_header)}} \n"
        return s


def _yield_until_empty(from_: list[Component], should_yield: Callable) -> Iterator[Component]:
    i = 0
    while len(from_) > 0:
        if should_yield(from_[i]):
            yield from_.pop(i)
            i = max(0, i - 1)
        else:
            i += 1
            if i >= len(from_):
                i = 0
                yield None
