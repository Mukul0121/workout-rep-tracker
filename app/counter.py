EXERCISES = {
    'squat':  {'joints': ('HIP', 'KNEE', 'ANKLE'),       'extended': 160, 'flexed': 90},
    'curl':   {'joints': ('SHOULDER', 'ELBOW', 'WRIST'), 'extended': 160, 'flexed': 40},
    'pushup': {'joints': ('SHOULDER', 'ELBOW', 'WRIST'), 'extended': 160, 'flexed': 90},
}

class RepCounter:
    def __init__(self, exercise):
        if exercise not in EXERCISES:
            raise ValueError(f'Unknown exercise: {exercise}')
        self.cfg = EXERCISES[exercise]
        self.reps = 0
        self.stage = None  # None, 'extended' or 'flexed'

    def update(self, angle):
        '''Feed one angle reading; return the current rep count.'''
        if angle > self.cfg['extended']:
            if self.stage == 'flexed':
                self.reps += 1
            self.stage = 'extended'
        elif angle < self.cfg['flexed']:
            self.stage = 'flexed'
        return self.reps