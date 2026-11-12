import math

def calculate_angle(a,b,c):
    '''Return the angle in degrees at point b formed by a-b-c.
    Each point is an (x, y) tuple.'''
    radians = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    angle = abs(math.degrees(radians))
    return 360 - angle if angle > 180 else angle