from collections import defaultdict
from dataclasses import dataclass, field
from itertools import permutations
from typing import Dict, Set


@dataclass
class RuleSet:
    dependencies: Dict[str, Set[str]] = field(default_factory=lambda: defaultdict(set))
    reversed_dependencies: Dict[str, Set[str]] = field(
        default_factory=lambda: defaultdict(set)
    )
    conflicts: Dict[str, Set[str]] = field(default_factory=lambda: defaultdict(set))

    @classmethod
    def new_rule_set(cls) -> "RuleSet":
        return RuleSet()

    def add_dep(self, opt1: str, opt2: str) -> "RuleSet":
        for dep in set([opt1] + list(self.reversed_dependencies[opt1])):
            # Add deps by transitivity
            self.dependencies[dep] |= self.dependencies[opt2]
            self.dependencies[dep].add(opt2)
            # Build reversed mapping (depending on)
            self.reversed_dependencies[opt2] |= self.dependencies[dep]
            self.reversed_dependencies[opt2].add(dep)

        return self

    def add_conflict(self, opt1: str, opt2: str) -> "RuleSet":
        for key1, key2 in permutations((opt1, opt2)):
            # Add conflict
            self.conflicts[key1].add(key2)

        return self

    def is_coherent(self) -> bool:
        return all(
            [
                self.reversed_dependencies[opt].isdisjoint(self.conflicts[opt])
                for opt in self.dependencies.keys()
            ]
        )
