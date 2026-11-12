from app.angles import calculate_angle

def test_right_angle():
    assert round(calculate_angle((0,1),(0,0),(1,0))) == 90

def test_straight_line():
    assert round(calculate_angle((-1, 0), (0, 0), (1, 0))) == 180