from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, Admin, Event, Participant
from forms import LoginForm, EventForm, RegistrationForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login = LoginManager(app)
login.login_view = 'login'

@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))

# --- User Routes ---

@app.route('/')
@app.route('/index')
def index():
    events = Event.query.filter(Event.date >= datetime.today().date()).order_by(Event.date.asc()).all()
    return render_template('index.html', title='Home', events=events)

@app.route('/event/<int:id>')
def event_detail(id):
    event = Event.query.get_or_404(id)
    return render_template('event_detail.html', title=event.name, event=event)

@app.route('/register/<int:event_id>', methods=['GET', 'POST'])
def register(event_id):
    event = Event.query.get_or_404(event_id)
    form = RegistrationForm()
    if form.validate_on_submit():
        participant = Participant(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            event_id=event.id
        )
        db.session.add(participant)
        db.session.commit()
        flash(f'Thank you for registering for {event.name}!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form, event=event)

# --- Admin Routes ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('admin_dashboard'))
    return render_template('login.html', title='Admin Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    total_events = Event.query.count()
    total_participants = Participant.query.count()
    
    # Most popular event logic (simple count)
    most_popular_event = db.session.query(Event).join(Participant).group_by(Event.id).order_by(db.func.count(Participant.id).desc()).first()
    
    events = Event.query.all()
    return render_template('admin/dashboard.html', title='Admin Dashboard', 
                           total_events=total_events, 
                           total_participants=total_participants,
                           most_popular_event=most_popular_event,
                           events=events)

@app.route('/admin/event/add', methods=['GET', 'POST'])
@login_required
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            name=form.name.data,
            date=form.date.data,
            location=form.location.data,
            description=form.description.data,
            registered_students=form.registered_students.data
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/event_form.html', title='Add Event', form=form)

@app.route('/admin/event/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    event = Event.query.get_or_404(id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.name = form.name.data
        event.date = form.date.data
        event.location = form.location.data
        event.description = form.description.data
        event.registered_students = form.registered_students.data
        db.session.commit()
        flash('Event updated successfully!')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/event_form.html', title='Edit Event', form=form)

@app.route('/admin/event/delete/<int:id>', methods=['POST'])
@login_required
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted.')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/event/<int:id>/participants')
@login_required
def view_participants(id):
    event = Event.query.get_or_404(id)
    participants = event.participants.all()
    return render_template('admin/participants.html', title=f'Participants for {event.name}', 
                           event=event, participants=participants)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Seed admin if none exists
        if Admin.query.count() == 0:
            admin = Admin(username='admin')
            admin.set_password('password')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
