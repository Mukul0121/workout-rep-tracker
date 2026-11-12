from app.counter import RepCounter

def test_counts_one_full_rep():
    c = RepCounter('squat')
    for angle in [170, 120, 80, 120, 170]:
        c.update(angle)
    assert c.reps == 1

def test_half_rep_not_counted():
    c = RepCounter('squat')
    for angle in [170, 120, 100, 120, 170]:
        c.update(angle)
    assert c.reps == 0