# app.py — Community Connect: Volunteer Matching Platform

from flask import (Flask, render_template, redirect, url_for,
                   request, session, flash)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from functools import wraps
from models import db, User, Project, Application

# ---------------------------------------------------------------------------
# App factory / configuration
# ---------------------------------------------------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cc-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables on first run
with app.app_context():
    db.create_all()

# ---------------------------------------------------------------------------
# Auth decorators
# ---------------------------------------------------------------------------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def volunteer_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'volunteer':
            flash('Access restricted to volunteers.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated


def organizer_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'organizer':
            flash('Access restricted to organizers.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

# ---------------------------------------------------------------------------
# Public routes
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    """Landing page with platform statistics."""
    total_projects = Project.query.count()
    total_volunteers = User.query.filter_by(role='volunteer').count()
    total_applications = Application.query.count()
    accepted = Application.query.filter_by(status='Accepted').count()
    recent_projects = Project.query.order_by(Project.id.desc()).limit(6).all()
    return render_template('index.html',
                           total_projects=total_projects,
                           total_volunteers=total_volunteers,
                           total_applications=total_applications,
                           accepted=accepted,
                           recent_projects=recent_projects)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        phone    = request.form.get('phone', '').strip()
        role     = request.form.get('role', 'volunteer')

        # Basic validation
        if not all([name, email, password]):
            flash('Name, email, and password are required.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('An account with that email already exists.', 'warning')
            return render_template('register.html')

        if role not in ('volunteer', 'organizer'):
            flash('Invalid role selected.', 'danger')
            return render_template('register.html')

        hashed_pw = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed_pw,
                    phone=phone, role=role)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['role'] = user.role
            flash(f'Welcome back, {user.name}!', 'success')
            if user.role == 'organizer':
                return redirect(url_for('organizer_dashboard'))
            return redirect(url_for('volunteer_dashboard'))

        flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# ---------------------------------------------------------------------------
# Volunteer routes
# ---------------------------------------------------------------------------

@app.route('/volunteer_dashboard')
@login_required
@volunteer_required
def volunteer_dashboard():
    user = User.query.get(session['user_id'])
    applied_ids = [a.project_id for a in user.applications]
    total_applied = len(applied_ids)
    accepted_count = Application.query.filter_by(
        volunteer_id=user.id, status='Accepted').count()
    pending_count = Application.query.filter_by(
        volunteer_id=user.id, status='Pending').count()
    recent_apps = (Application.query
                   .filter_by(volunteer_id=user.id)
                   .order_by(Application.applied_date.desc())
                   .limit(5).all())
    return render_template('volunteer_dashboard.html',
                           user=user,
                           total_applied=total_applied,
                           accepted_count=accepted_count,
                           pending_count=pending_count,
                           recent_apps=recent_apps)


@app.route('/projects')
@login_required
@volunteer_required
def projects():
    search   = request.args.get('search', '').strip()
    location = request.args.get('location', '').strip()

    query = Project.query
    if search:
        query = query.filter(Project.title.ilike(f'%{search}%'))
    if location:
        query = query.filter(Project.location.ilike(f'%{location}%'))

    all_projects = query.order_by(Project.id.desc()).all()
    applied_ids = [a.project_id for a in
                   Application.query.filter_by(volunteer_id=session['user_id']).all()]

    locations = db.session.query(Project.location).distinct().all()
    locations = [l[0] for l in locations if l[0]]

    return render_template('projects.html',
                           projects=all_projects,
                           applied_ids=applied_ids,
                           search=search,
                           location=location,
                           locations=locations)

@app.route('/apply/<int:project_id>', methods=['POST'])
@login_required
@volunteer_required
def apply(project_id):

    print("========== APPLY CLICKED ==========")
    print("Project ID:", project_id)
    print("Volunteer ID:", session['user_id'])

    project = Project.query.get_or_404(project_id)

    existing = Application.query.filter_by(
        volunteer_id=session['user_id'],
        project_id=project_id
    ).first()

    print("Existing Application:", existing)

    if existing:
        flash('You have already applied to this project.', 'warning')
    else:
        app_obj = Application(
            volunteer_id=session['user_id'],
            project_id=project_id,
            status='Pending'
        )

        db.session.add(app_obj)
        db.session.commit()

        print("APPLICATION SAVED SUCCESSFULLY")

        flash(f'Applied to "{project.title}" successfully!', 'success')

    return redirect(url_for('projects'))

@app.route('/applications')
@login_required
@volunteer_required
def applications():
    user_apps = (Application.query
                 .filter_by(volunteer_id=session['user_id'])
                 .order_by(Application.applied_date.desc()).all())
    return render_template('applications.html', applications=user_apps)

# ---------------------------------------------------------------------------
# Organizer routes
# ---------------------------------------------------------------------------

@app.route('/organizer_dashboard')
@login_required
@organizer_required
def organizer_dashboard():
    user = User.query.get(session['user_id'])
    my_projects = Project.query.filter_by(organizer_id=user.id).all()
    total_projects = len(my_projects)
    total_applicants = sum(len(p.applications) for p in my_projects)
    accepted_count = sum(
        1 for p in my_projects
        for a in p.applications if a.status == 'Accepted')
    pending_count = sum(
        1 for p in my_projects
        for a in p.applications if a.status == 'Pending')

    return render_template('organizer_dashboard.html',
                           user=user,
                           projects=my_projects,
                           total_projects=total_projects,
                           total_applicants=total_applicants,
                           accepted_count=accepted_count,
                           pending_count=pending_count)


@app.route('/add_project', methods=['GET', 'POST'])
@login_required
@organizer_required
def add_project():
    project_to_edit = None
    edit_id = request.args.get('edit')

    if edit_id:
        project_to_edit = Project.query.get_or_404(int(edit_id))
        if project_to_edit.organizer_id != session['user_id']:
            flash('Unauthorized.', 'danger')
            return redirect(url_for('organizer_dashboard'))

    if request.method == 'POST':
        title       = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        skills      = request.form.get('skills', '').strip()
        location    = request.form.get('location', '').strip()
        start_str   = request.form.get('start_date', '')
        end_str     = request.form.get('end_date', '')
        pid         = request.form.get('project_id')

        if not all([title, description]):
            flash('Title and description are required.', 'danger')
            return render_template('add_project.html', project=project_to_edit)

        start_date = datetime.strptime(start_str, '%Y-%m-%d').date() if start_str else None
        end_date   = datetime.strptime(end_str,   '%Y-%m-%d').date() if end_str   else None

        if pid:  # editing existing
            proj = Project.query.get_or_404(int(pid))
            if proj.organizer_id != session['user_id']:
                flash('Unauthorized.', 'danger')
                return redirect(url_for('organizer_dashboard'))
            proj.title = title
            proj.description = description
            proj.skills = skills
            proj.location = location
            proj.start_date = start_date
            proj.end_date = end_date
            db.session.commit()
            flash('Project updated successfully.', 'success')
        else:
            proj = Project(title=title, description=description,
                           skills=skills, location=location,
                           start_date=start_date, end_date=end_date,
                           organizer_id=session['user_id'])
            db.session.add(proj)
            db.session.commit()
            flash('Project created successfully!', 'success')

        return redirect(url_for('organizer_dashboard'))

    return render_template('add_project.html', project=project_to_edit)


@app.route('/delete_project/<int:project_id>', methods=['POST'])
@login_required
@organizer_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.organizer_id != session['user_id']:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('organizer_dashboard'))
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted.', 'info')
    return redirect(url_for('organizer_dashboard'))


@app.route('/view_applicants/<int:project_id>')
@login_required
@organizer_required
def view_applicants(project_id):
    project = Project.query.get_or_404(project_id)
    if project.organizer_id != session['user_id']:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('organizer_dashboard'))
    applicants = Application.query.filter_by(project_id=project_id).all()
    return render_template('applicants.html', project=project, applicants=applicants)


@app.route('/update_status/<int:application_id>/', methods=['POST'])
@login_required
@organizer_required
def update_status(application_id):
    application = Application.query.get_or_404(application_id)
    # Verify the organizer owns the project
    if application.project.organizer_id != session['user_id']:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('organizer_dashboard'))

    new_status = request.form.get('status')
    if new_status in ('Accepted', 'Rejected', 'Pending'):
        application.status = new_status
        db.session.commit()
        flash(f'Application status updated to {new_status}.', 'success')
    else:
        flash('Invalid status value.', 'danger')

    return redirect(url_for('view_applicants', project_id=application.project_id))

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
