from dataclasses import dataclass, field
from typing import Set

from option_manager.rule_set import RuleSet


@dataclass
class OptionSet:
    rule_set: RuleSet
    asked_options: Set[str] = field(default_factory=set)
    activated_options: Set[str] = field(default_factory=set)

    @classmethod
    def new(cls, rules: RuleSet) -> "OptionSet":
        if not rules.is_coherent():
            raise ValueError("Cannot create an option set with incoherant ruleset")
        return OptionSet(rules)

    def toggle(self, option: str) -> "OptionSet":
        if option in self.asked_options:
            self.asked_options.remove(option)
            self.asked_options -= self.rule_set.reversed_dependencies[option]
            self.activated_options.remove(option)
            self.activated_options -= self.rule_set.reversed_dependencies[option]
        else:
            self.asked_options.add(option)
            for dep in set([option] + list(self.rule_set.dependencies[option])):
                self.activated_options -= self.rule_set.conflicts[dep]
                self.asked_options -= self.rule_set.conflicts[dep]
                for conflict in self.rule_set.conflicts[dep]:
                    self.activated_options -= self.rule_set.reversed_dependencies[
                        conflict
                    ]
                    self.asked_options -= self.rule_set.reversed_dependencies[conflict]

            self.activated_options.add(option)
            self.activated_options |= self.rule_set.dependencies[option]
        return self

    def string_slice(self) -> str:
        return "".join(sorted(self.activated_options))
