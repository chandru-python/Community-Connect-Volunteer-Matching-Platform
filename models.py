# models.py — SQLAlchemy models for Community Connect

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """Represents a registered user (volunteer or organizer)."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)   # hashed
    phone = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(20), nullable=False)         # 'volunteer' | 'organizer'

    # Relationships
    projects = db.relationship('Project', backref='organizer', lazy=True,
                               foreign_keys='Project.organizer_id')
    applications = db.relationship('Application', backref='volunteer', lazy=True,
                                   foreign_keys='Application.volunteer_id')


class Project(db.Model):
    """A volunteer project posted by an organizer."""
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.String(300), nullable=True)
    location = db.Column(db.String(150), nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    applications = db.relationship('Application', backref='project', lazy=True,
                                   cascade='all, delete-orphan')


class Application(db.Model):
    """A volunteer's application to a project."""
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')  # Pending | Accepted | Rejected
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
