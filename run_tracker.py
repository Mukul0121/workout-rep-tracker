import argparse
from app.tracker import run

parser = argparse.ArgumentParser()
parser.add_argument('--exercise', default='squat', choices=['squat', 'curl', 'pushup'])
parser.add_argument('--side', default='LEFT', choices=['LEFT', 'RIGHT'])
args = parser.parse_args()
print('Reps counted:', run(args.exercise, args.side))