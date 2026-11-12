import os
from app import db

def test_database_flow():
    # Use a temporary database path in tests so real data is never touched
    test_path = 'data/test_workouts.db'
    if os.path.exists(test_path):
        os.remove(test_path)
        
    # Test add_session and list_sessions
    db.add_session('squat', 20, 60, path=test_path)
    sessions = db.list_sessions(path=test_path)
    assert len(sessions) == 1
    assert sessions[0]['exercise'] == 'squat'
    assert sessions[0]['reps'] == 20
    
    # Test get_stats on an empty/populated database
    stats = db.get_stats(path=test_path)
    assert stats['total_reps'] == 20
    
    if os.path.exists(test_path):
        os.remove(test_path)