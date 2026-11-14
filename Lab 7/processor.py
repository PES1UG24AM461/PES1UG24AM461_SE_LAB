import math


def parse_order(text):
    """Return the normalized garment and weight, or None for invalid input."""
    if not isinstance(text, str):
        return None
    try:
        garment, raw_weight = text.split(":")
        weight = float(raw_weight)
    except ValueError:
        return None

    garment = garment.strip()
    if not garment or not math.isfinite(weight) or weight < 0:
        return None
    return garment.title(), weight


def weight_average(weights_csv):
    """Return the floor average of nonnegative integer weights, or None."""
    if not isinstance(weights_csv, str):
        return None
    try:
        weights = [int(value) for value in weights_csv.split(",")]
    except ValueError:
        return None
    if any(weight < 0 for weight in weights):
        return None
    return sum(weights) // len(weights)


def payable_charge(text):
    """Return the charge after tax and discount, or None for invalid input."""
    if not isinstance(text, str):
        return None
    try:
        charge, discount = map(float, text.split("|"))
    except ValueError:
        return None
    if not math.isfinite(charge) or not math.isfinite(discount):
        return None
    if charge < 0 or discount < 0:
        return None

    total = charge * 1.18 - discount
    if not math.isfinite(total):
        return None
    return max(total, 0)


def main():
    print("==== Running parse_order ====")
    try:
        result = parse_order(input("Enter garment:weight in kg (e.g. regular:6): "))
        if result is None:
            print("Invalid order. Enter a garment and a finite, nonnegative weight.")
        else:
            print("Garment and Weight:", result)

        print("\n==== Running weight_average ====")
        result = weight_average(input("Enter garment weights as CSV (e.g. 3,5,8): "))
        if result is None:
            print("Invalid weights. Enter comma-separated nonnegative integers.")
        else:
            print("Average Weight:", result)

        print("\n==== Running payable_charge ====")
        result = payable_charge(input("Enter charge|discount (e.g. 300|40): "))
        if result is None:
            print("Invalid charge or discount. Enter finite, nonnegative values.")
        else:
            print("Payable Charge:", result)
    except EOFError:
        print("\nInput ended.")


if __name__ == "__main__":
    main()
