from bad_code import do_complex_math

def test_do_complex_math_normal():
    assert do_complex_math(10, 2) == 5.0

def test_do_complex_math_zero():
    assert do_complex_math(10, 0) == 0
