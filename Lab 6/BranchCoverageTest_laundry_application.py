import pytest

from laundry_service import dropoff_status, extra_weight_charge, order_acceptable


@pytest.mark.parametrize(
    ("garment", "weight", "message"),
    [
        pytest.param("unknown", 5, "unknown garment type", id="unknown-garment"),
        pytest.param("regular", -1, "invalid weight", id="negative-weight"),
    ],
)
def test_extra_weight_charge_rejects_invalid_input(garment, weight, message):
    with pytest.raises(ValueError, match=f"^{message}$"):
        extra_weight_charge(garment, weight, "standard", False)


@pytest.mark.parametrize(
    ("garment", "weight", "speed", "member", "expected"),
    [
        pytest.param("regular", 7, "standard", True, 0, id="member-allowance"),
        pytest.param("delicate", 4, "standard", False, 30, id="standard-rate"),
        pytest.param("bedding", 19, "express", False, 825, id="express-surcharges"),
        pytest.param("regular", 15, "standard", False, 300, id="at-surcharge-threshold"),
        pytest.param("regular", 16, "standard", False, 495, id="standard-surcharge"),
        pytest.param("bedding", 9, "express", True, 50, id="member-bedding-excluded"),
    ],
)
def test_extra_weight_charge(garment, weight, speed, member, expected):
    assert extra_weight_charge(garment, weight, speed, member) == expected


@pytest.mark.parametrize(
    ("weight", "items", "delicate", "expected"),
    [
        pytest.param(10, 5, True, True, id="delicate-item-limit"),
        pytest.param(10, 6, True, False, id="over-delicate-item-limit"),
        pytest.param(25, 41, False, False, id="over-regular-item-limit"),
        pytest.param(26, 20, False, False, id="overweight"),
        pytest.param(25, 40, False, True, id="regular-limits"),
    ],
)
def test_order_acceptable(weight, items, delicate, expected):
    assert order_acceptable(weight, items, delicate) is expected


@pytest.mark.parametrize(
    ("minutes", "bedding", "express", "expected"),
    [
        pytest.param(120, True, True, "accepted", id="at-express-bedding-cutoff"),
        pytest.param(119, True, True, "late", id="below-express-bedding-cutoff"),
        pytest.param(90, True, False, "accepted", id="at-standard-bedding-cutoff"),
        pytest.param(90, False, True, "accepted", id="at-express-cutoff"),
        pytest.param(60, False, False, "accepted", id="at-standard-cutoff"),
        pytest.param(40, False, False, "late", id="at-late-window-start"),
        pytest.param(39, False, False, "rejected", id="below-late-window"),
    ],
)
def test_dropoff_status(minutes, bedding, express, expected):
    assert dropoff_status(minutes, bedding, express) == expected
