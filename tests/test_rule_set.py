from option_manager.rule_set import RuleSet


def test_transitivity_deps():
    rs = (
        RuleSet.new_rule_set()
        .add_dep("A", "B")
        .add_dep("B", "C")
        .add_dep("C", "D")
        .add_dep("D", "E")
    )

    assert rs.dependencies["A"] == {"B", "C", "D", "E"}
    assert rs.dependencies["B"] == {"C", "D", "E"}
    assert rs.dependencies["E"] == set()


def test_conflicts():
    rs = (
        RuleSet.new_rule_set()
        .add_conflict("B", "C")
        .add_conflict("C", "D")
        .add_conflict("D", "E")
    )

    assert rs.conflicts["A"] == set()
    assert rs.conflicts["B"] == {"C"}
    assert rs.conflicts["C"] == {"B", "D"}
    assert rs.conflicts["E"] == {"D"}


def test_is_coherant():
    rs = (
        RuleSet.new_rule_set()
        .add_dep("A", "B")
        .add_dep("B", "C")
        .add_conflict("C", "D")
    )

    assert rs.is_coherent()


def test_is_not_coherant():
    rs = (
        RuleSet.new_rule_set()
        .add_dep("A", "B")
        .add_dep("B", "C")
        .add_conflict("A", "C")
    )

    assert not rs.is_coherent()
