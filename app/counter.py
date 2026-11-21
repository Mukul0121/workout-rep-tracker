import time

EXERCISES = {
    'squat':    {'joints': ('HIP', 'KNEE', 'ANKLE'),       'extended': 160, 'flexed': 90},
    'curl':     {'joints': ('SHOULDER', 'ELBOW', 'WRIST'), 'extended': 160, 'flexed': 40},
    'pushup':   {'joints': ('SHOULDER', 'ELBOW', 'WRIST'), 'extended': 160, 'flexed': 90},
    'bench':    {'joints': ('SHOULDER', 'ELBOW', 'WRIST'), 'extended': 160, 'flexed': 70},
    'deadlift': {'joints': ('SHOULDER', 'HIP', 'KNEE'),    'extended': 170, 'flexed': 110},
}

class RepCounter:
    def __init__(self, exercise):
        self.cfg = EXERCISES[exercise]
        self.reps = 0
        self.state = 'extended'
        self.leave_extended_time = 0
        self.enter_flexed_time = 0
        self.rep_data = [] 
        self.total_tut = 0.0

    def update(self, angle):
        if self.state == 'extended' and angle < self.cfg['extended']:
            self.state = 'moving_to_flex'
            self.leave_extended_time = time.time()
            
        elif self.state == 'moving_to_flex' and angle < self.cfg['flexed']:
            self.state = 'flexed'
            self.enter_flexed_time = time.time()
            
        elif self.state == 'flexed' and angle > self.cfg['extended']:
            self.reps += 1
            now = time.time()
            
            t_flex = max(0, self.enter_flexed_time - self.leave_extended_time if self.leave_extended_time else 0)
            t_extend = max(0, now - self.enter_flexed_time if self.enter_flexed_time else 0)
            
            self.total_tut += (t_flex + t_extend)
            self.rep_data.append({
                'rep': self.reps,
                't_flex': round(t_flex, 1),
                't_extend': round(t_extend, 1)
            })
            
            self.state = 'extended'
            self.leave_extended_time = 0
            self.enter_flexed_time = 0