from flask import Flask, jsonify, request, render_template
from . import db
from .counter import EXERCISES

def create_app(db_path=None):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    db.init_db(db_path)

    @app.get('/')
    def dashboard():
        return render_template('index.html')

    @app.get('/api/sessions')
    def sessions():
        return jsonify(db.list_sessions(request.args.get('exercise'), db_path))

    @app.post('/api/sessions')
    def create_session():
        data = request.get_json(silent=True) or {}
        exercise, reps, duration = data.get('exercise'), data.get('reps'), data.get('duration_sec')
        if exercise not in EXERCISES or not isinstance(reps, int) or not isinstance(duration, int):
            return jsonify({'error': 'invalid input'}), 400
        if reps < 0 or duration < 0:
            return jsonify({'error': 'invalid input'}), 400
        return jsonify({'id': db.add_session(exercise, reps, duration, path=db_path)}), 201

    @app.get('/api/stats')
    def stats():
        return jsonify(db.get_stats(db_path))

    return app