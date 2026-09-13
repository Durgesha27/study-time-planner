from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study_planner.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(120), default='Alex')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    sessions = db.relationship('StudySession', backref='user', lazy=True, cascade='all, delete-orphan')
    goals = db.relationship('Goal', backref='user', lazy=True, cascade='all, delete-orphan')
    progress = db.relationship('Progress', backref='user', lazy=True, cascade='all, delete-orphan')

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    sessions = db.relationship('StudySession', backref='subject', lazy=True)
    goals = db.relationship('Goal', backref='subject', lazy=True)

class StudySession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    day = db.Column(db.String(10), nullable=False)
    start_time = db.Column(db.String(5), nullable=False)
    end_time = db.Column(db.String(5), nullable=False)
    session_type = db.Column(db.String(20), default='Focus')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    target_hours = db.Column(db.Float, default=12)
    completed_hours = db.Column(db.Float, default=0)
    is_completed = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    study_hours = db.Column(db.Float, default=0)
    focus_score = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def before_request():
    if 'user_id' in session:
        session.permanent = True
        app.permanent_session_lifetime = timedelta(days=7)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        name = data.get('name', 'Alex')
        
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'error': 'Email already exists'}), 400
        
        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            name=name
        )
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        session['username'] = user.username

        return jsonify({'success': True}), 200
    
    return render_template('loginsignup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return jsonify({'success': True}), 200
        
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    
    return render_template('loginsignup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    user = User.query.get(session['user_id'])
    today = datetime.utcnow().strftime('%A').lower()
    
    today_sessions = StudySession.query.filter_by(
        user_id=session['user_id'],
        day=today
    ).all()
    
    week_start = datetime.utcnow() - timedelta(days=datetime.utcnow().weekday())
    week_progress = db.session.query(db.func.sum(Progress.study_hours)).filter(
        Progress.user_id == session['user_id'],
        Progress.date >= week_start
    ).scalar() or 0
    
    goals = Goal.query.filter_by(user_id=session['user_id']).all()
    completed_goals = sum(1 for g in goals if g.is_completed)
    
    return render_template('home.html', 
                         user=user, 
                         today_sessions=today_sessions,
                         week_progress=week_progress,
                         completed_goals=completed_goals,
                         total_goals=len(goals))

@app.route('/schedule')
@login_required
def schedule():
    user = User.query.get(session['user_id'])
    subjects = Subject.query.filter_by(user_id=session['user_id']).all()
    sessions = StudySession.query.filter_by(user_id=session['user_id']).all()
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    schedule_data = {day.lower(): [] for day in days}
    
    for s in sessions:
        schedule_data[s.day].append(s)
    
    return render_template('schedule.html', 
                         user=user,
                         subjects=subjects,
                         schedule=schedule_data,
                         days=days)

@app.route('/progress')
@login_required
def progress_page():
    user = User.query.get(session['user_id'])
    week_start = datetime.utcnow() - timedelta(days=datetime.utcnow().weekday())
    
    weekly_stats = {}
    for i in range(7):
        date = week_start + timedelta(days=i)
        day_progress = Progress.query.filter(
            Progress.user_id == session['user_id'],
            Progress.date >= date,
            Progress.date < date + timedelta(days=1)
        ).first()
        weekly_stats[date.strftime('%a')] = day_progress.study_hours if day_progress else 0
    
    return render_template('progress.html', user=user, weekly_stats=weekly_stats)

@app.route('/goals')
@login_required
def goals_page():
    user = User.query.get(session['user_id'])
    subjects = Subject.query.filter_by(user_id=session['user_id']).all()
    goals = Goal.query.filter_by(user_id=session['user_id']).all()
    
    return render_template('goals.html', user=user, subjects=subjects, goals=goals)

@app.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    subjects = Subject.query.filter_by(user_id=session['user_id']).all()
    
    return render_template('profile.html', user=user, subjects=subjects)

@app.route('/api/user/update', methods=['POST'])
@login_required
def update_user():
    data = request.get_json()
    user = User.query.get(session['user_id'])
    
    if 'name' in data:
        user.name = data['name']
    
    db.session.commit()
    return jsonify({'success': True, 'user': {'id': user.id, 'name': user.name}})

@app.route('/api/subjects', methods=['GET', 'POST'])
@login_required
def subjects_api():
    if request.method == 'POST':
        data = request.get_json()
        subject = Subject(
            name=data['name'],
            user_id=session['user_id']
        )
        db.session.add(subject)
        db.session.commit()
        return jsonify({'success': True, 'subject': {'id': subject.id, 'name': subject.name}})
    
    subjects = Subject.query.filter_by(user_id=session['user_id']).all()
    return jsonify({'subjects': [{'id': s.id, 'name': s.name} for s in subjects]})

@app.route('/api/subjects/<int:subject_id>', methods=['PUT', 'DELETE'])
@login_required
def subject_detail(subject_id):
    subject = Subject.query.filter_by(id=subject_id, user_id=session['user_id']).first()
    
    if not subject:
        return jsonify({'error': 'Not found'}), 404
    
    if request.method == 'PUT':
        data = request.get_json()
        subject.name = data.get('name', subject.name)
        db.session.commit()
        return jsonify({'success': True, 'subject': {'id': subject.id, 'name': subject.name}})
    
    elif request.method == 'DELETE':
        db.session.delete(subject)
        db.session.commit()
        return jsonify({'success': True})

@app.route('/api/sessions', methods=['GET', 'POST'])
@login_required
def sessions_api():
    if request.method == 'POST':
        data = request.get_json()
        session_obj = StudySession(
            user_id=session['user_id'],
            subject_id=data['subject_id'],
            title=data['title'],
            day=data['day'].lower(),
            start_time=data['start_time'],
            end_time=data['end_time'],
            session_type=data.get('type', 'Focus')
        )
        db.session.add(session_obj)
        db.session.commit()
        return jsonify({'success': True, 'session': {'id': session_obj.id}})
    
    sessions = StudySession.query.filter_by(user_id=session['user_id']).all()
    return jsonify({'sessions': [{'id': s.id, 'title': s.title, 'day': s.day} for s in sessions]})

@app.route('/api/sessions/<int:session_id>', methods=['DELETE'])
@login_required
def session_detail(session_id):
    study_session = StudySession.query.filter_by(id=session_id, user_id=session['user_id']).first()
    
    if not study_session:
        return jsonify({'error': 'Not found'}), 404
    
    db.session.delete(study_session)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/goals', methods=['GET', 'POST'])
@login_required
def goals_api():
    if request.method == 'POST':
        data = request.get_json()
        goal = Goal(
            user_id=session['user_id'],
            subject_id=data['subject_id'],
            title=data['title'],
            target_hours=data.get('target_hours', 12)
        )
        db.session.add(goal)
        db.session.commit()
        return jsonify({'success': True, 'goal': {'id': goal.id}})
    
    goals = Goal.query.filter_by(user_id=session['user_id']).all()
    return jsonify({'goals': [{'id': g.id, 'title': g.title} for g in goals]})

@app.route('/api/goals/<int:goal_id>', methods=['PUT', 'DELETE'])
@login_required
def goal_detail(goal_id):
    goal = Goal.query.filter_by(id=goal_id, user_id=session['user_id']).first()
    
    if not goal:
        return jsonify({'error': 'Not found'}), 404
    
    if request.method == 'PUT':
        data = request.get_json()
        if 'is_completed' in data:
            goal.is_completed = data['is_completed']
        db.session.commit()
        return jsonify({'success': True})
    
    elif request.method == 'DELETE':
        db.session.delete(goal)
        db.session.commit()
        return jsonify({'success': True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)