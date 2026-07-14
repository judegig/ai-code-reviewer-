import os
api_token = os.getenv("API_TOKEN")
def calculate_division(numerator, denominator):
    if denominator == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return numerator / denominator
