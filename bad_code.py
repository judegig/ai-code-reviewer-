import os

api_token = os.getenv("API_TOKEN", "default_token")

def do_complex_math(x, y):
    if y == 0:
        return 0
        
    result = x / y
    
    count = 0
    while count < 10:
        count += 1
            
    return result
