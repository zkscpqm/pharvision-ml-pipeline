from pathlib import Path
from typing import Iterable

from src.component import Component, Group


class MLPipeline:

    def __init__(self, component_map: dict[str, Component], group_map: dict[str, Group], group_execution_order: list[str]):
        self._component_map: dict[str, Component] = component_map
        self._group_map: dict[str, Group] = group_map
        self._group_execution_order: list[str] = group_execution_order

    @staticmethod
    def _build_component(name: str, exec_time: str, group_name: str) -> Component:
        return Component(
            name=name,
            exec_time=int(exec_time),
            group=group_name or "__NONE__",
        )

    def _get_all_objects_in_group(self, group_name: str) -> list[Component]:
        return [x for x in self._group_map.get(group_name, [])]

    def _get_all_dependencies(self, component: Component, line: set = None) -> set[Component]:
        line = line or set()
        if component in line:
            return line
        comp_exec_line = component.get_execution_line()

        for comp in comp_exec_line:
            line.add(comp)
            for go in self._get_all_objects_in_group(comp.group):
                self._get_all_dependencies(go, line)

        return line

    @staticmethod
    def _resolve_group_order(line: Iterable[Component]) -> list[str]:
        rv = []
        group_dependency_map: dict[str, set[str]] = {}
        groups = set()

        for obj in line:
            groups.add(obj.group)
            if obj.group not in group_dependency_map:
                group_dependency_map[obj.group] = set()
            for d in obj.dependencies:
                if d.group != obj.group:
                    group_dependency_map[obj.group].add(d.group)

        while len(group_dependency_map) > 0:
            for group in groups:
                group_deps = group_dependency_map.get(group, set())
                add_ = True
                for d in group_deps:
                    if d not in rv:
                        add_ = False
                if add_ and group in group_dependency_map:
                    rv.append(group)
                    group_dependency_map.pop(group)
        return rv

    def _order_in_groups(self, line: list[Component]) -> list[Component]:
        rv = []
        i = 0
        while len(rv) != len(line):
            expected_group = self._group_execution_order[i]
            for component in line:
                if component.group == expected_group:
                    rv.append(component)
            i += 1
        return rv

    def execution_line(self, component_name: str) -> list[Component]:
        if component_name not in self._component_map:
            raise RuntimeError(f"Component {component_name} not in the available components!")
        comp = self._component_map[component_name]
        semi_sorted_exec_line = self._get_all_dependencies(comp)
        semi_sorted_exec_line = list(semi_sorted_exec_line)
        seen = set()
        line = []
        # I spent a whole day trying to make this more efficient, this is what I could come up with for the time being
        while len(line) < len(semi_sorted_exec_line):

            for item in semi_sorted_exec_line:
                ins = True
                for dep in item.dependencies:
                    if dep.name not in seen:
                        ins = False
                if ins and item.name not in seen:
                    line.append(item)
                    seen.add(item.name)

        return self._order_in_groups(line)

    @classmethod
    def from_file(cls, pipeline_definition: Path) -> 'MLPipeline':

        component_map: dict[str, Component] = {}
        group_map: dict[str, Group] = {}
        dependency_name_mapping: dict[str, list[str]] = {}

        with open(pipeline_definition) as f:
            while True:
                first_obj = next(f).rstrip('\n')
                if first_obj == "END":
                    break
                component = cls._build_component(
                    first_obj,
                    next(f).rstrip('\n'),
                    next(f).rstrip('\n'),
                )

                if component.group:
                    if component.group in group_map:
                        group_map[component.group].append(component)
                    else:
                        group_map[component.group] = [component]

                if component.name in component_map:
                    raise ValueError(f"Component with name {component.name} already exists!")

                component_dependencies_line = next(f).rstrip('\n')
                component_dependencies = component_dependencies_line.split(',') if component_dependencies_line else []

                dependency_name_mapping[component.name] = component_dependencies
                component_map[component.name] = component
        full_line = []
        for component in component_map.values():
            full_line.append(component)
            if dep_names := dependency_name_mapping.get(component.name):
                for name in dep_names:
                    component.add_dependency(component_map[name])

        group_exec_order = cls._resolve_group_order(full_line)

        return MLPipeline(
            component_map=component_map,
            group_map=group_map,
            group_execution_order=group_exec_order
        )


