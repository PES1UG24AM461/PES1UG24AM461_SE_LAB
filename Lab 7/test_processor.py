from hypothesis import example, given, settings, strategies as st

from processor import parse_order, payable_charge, weight_average


@settings(report_multiple_bugs=False)
@given(st.text() | st.none())
def test_parse_order_no_crash(value):
    parse_order(value)


@settings(report_multiple_bugs=False)
@given(st.text() | st.none())
def test_weight_average_no_crash(value):
    weight_average(value)


@settings(report_multiple_bugs=False)
@given(st.text() | st.none())
def test_payable_charge_no_crash(value):
    payable_charge(value)


@given(st.integers(0, 10_000))
def test_parse_order_valid(weight):
    assert parse_order(f"  regular wash :{weight}") == ("Regular Wash", float(weight))


@given(st.lists(st.integers(0, 10_000), min_size=1))
def test_weight_average_valid(weights):
    assert weight_average(", ".join(map(str, weights))) == sum(weights) // len(weights)


@given(st.integers(0, 10_000), st.integers(0, 15_000))
def test_payable_charge_valid(charge, discount):
    assert payable_charge(f"{charge}|{discount}") == max(charge * 1.18 - discount, 0)


@given(st.sampled_from(["regular:", ":6", "regular:nan", "regular:-1", "regular:inf"]))
def test_invalid_orders(value):
    assert parse_order(value) is None


@given(st.sampled_from(["3,,8", ",", "3,-1,8", "3.5,8", "3, ", None]))
def test_invalid_weights(value):
    assert weight_average(value) is None


@given(st.sampled_from(["300|", "300|inf", "1.7e308|0", "300|-40", "-300|0", "nan|40"]))
@example("300|40|10")
def test_invalid_charges(value):
    assert payable_charge(value) is None
