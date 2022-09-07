import dataclasses


class Component:

    def __init__(self, name: str, exec_time: int, group: str):
        self.name: str = name
        self.execution_time: int = exec_time
        self.group: str = group
        self._dependencies: list['Component'] = []
        self._in_deps: set[str] = set()  # A set containing names of dependencies for easy duplicate searches

    @property
    def dependencies(self) -> list['Component']:
        return self._dependencies

    def add_dependency(self, dep: 'Component'):
        if dep.name in self._in_deps:
            return
        self._in_deps.add(dep.name)
        self._dependencies.append(dep)

    def get_execution_line(self) -> list['Component']:
        seen = {self.name}
        line = [self]

        for component in self._dependencies:
            if component.name in seen:
                continue
            line.append(component)
            seen.add(component.name)
        for component in line[1:]:
            comp_line = component.get_execution_line()
            for dep in comp_line:
                if dep.name in seen:
                    continue
                seen.add(dep.name)
                line.append(dep)

        return line

    def __str__(self) -> str:
        return f"[{self.name} ({self.group})] {self.execution_time} {[d.name for d in self._dependencies]}"

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(str(self))


Group = list[Component]
