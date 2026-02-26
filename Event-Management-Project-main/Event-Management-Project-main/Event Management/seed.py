from app import app, db
from models import Admin, Event, Participant
from datetime import datetime, timedelta

def seed_db():
    with app.app_context():
        # Drop and create all tables
        db.drop_all()
        db.create_all()

        # Add Admin
        admin = Admin(username='admin')
        admin.set_password('password')
        db.session.add(admin)

        # Add Events
        events = [
            Event(
                id=1,
                name='AI & Machine Learning Workshop',
                date=datetime.today().date() + timedelta(days=5),
                location='Computer Lab A',
                description='Introduction to AI concepts, hands-on ML projects for beginners.',
                registered_students=75
            ),
            Event(
                id=2,
                name='3D Modeling & Animation Workshop',
                date=datetime.today().date() + timedelta(days=7),
                location='Design Lab B',
                description='Learn the basics of 3D modeling, rendering, and animation using Blender.',
                registered_students=60
            ),
            Event(
                id=3,
                name='Cybersecurity Awareness Seminar',
                date=datetime.today().date() + timedelta(days=3),
                location='Lecture Hall 1',
                description='Understand cybersecurity threats, safe practices, and hands-on ethical hacking demo.',
                registered_students=90
            ),
            Event(
                id=4,
                name='Robotics Workshop',
                date=datetime.today().date() + timedelta(days=10),
                location='Robotics Lab',
                description='Build and program simple robots using Arduino and sensors.',
                registered_students=50
            )
        ]
        db.session.add_all(events)
        db.session.commit()

        # Add some participants to the first event
        event1 = Event.query.get(1)
        participants = [
            Participant(name='Alice Johnson', email='alice@example.com', phone='1234567890', event_id=event1.id),
            Participant(name='Bob Smith', email='bob@example.com', phone='0987654321', event_id=event1.id)
        ]
        db.session.add_all(participants)
        db.session.commit()

        print("Database seeded with CollegeTech events successfully!")

if __name__ == '__main__':
    seed_db()
