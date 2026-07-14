import os

def calculate_division(numerator, denominator):
    """
    Divides the numerator by the denominator.
    Raises ZeroDivisionError if the denominator is 0.
    """
    if denominator == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return numerator / denominator
