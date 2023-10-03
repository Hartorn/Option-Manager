from option_manager.options import OptionSet
from option_manager.rule_set import RuleSet


def test_toggle_transitvity():
    rs = (
        RuleSet.new_rule_set()
        .add_dep("A", "B")
        .add_dep("B", "C")
        .add_dep("C", "D")
        .add_dep("D", "E")
    )
    os = OptionSet.new(rs)
    os.toggle("A")
    assert "ABCDE" == os.string_slice()


def test_toggle_conflict():
    rs = (
        RuleSet.new_rule_set()
        .add_dep("A", "B")
        .add_dep("B", "C")
        .add_conflict("C", "D")
        .add_conflict("D", "E")
    )
    os = OptionSet.new(rs)
    os.toggle("A")
    assert "ABC" == os.string_slice()
    print(os.rule_set.reversed_dependencies["C"])
    os.toggle("D").toggle("E")
    assert "E" == os.string_slice()
