from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mca-taskmanager-secret-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ── Model ──────────────────────────────────────────────────────────────────────
class Task(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority    = db.Column(db.String(20), default='Medium')   # Low / Medium / High
    status      = db.Column(db.String(20), default='Pending')  # Pending / In Progress / Done
    due_date    = db.Column(db.String(20), nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.title}>'

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    filter_status   = request.args.get('status', 'All')
    filter_priority = request.args.get('priority', 'All')

    query = Task.query
    if filter_status != 'All':
        query = query.filter_by(status=filter_status)
    if filter_priority != 'All':
        query = query.filter_by(priority=filter_priority)

    tasks = query.order_by(Task.created_at.desc()).all()
    total     = Task.query.count()
    pending   = Task.query.filter_by(status='Pending').count()
    progress  = Task.query.filter_by(status='In Progress').count()
    done      = Task.query.filter_by(status='Done').count()

    return render_template('index.html',
                           tasks=tasks,
                           total=total, pending=pending,
                           progress=progress, done=done,
                           filter_status=filter_status,
                           filter_priority=filter_priority)


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title       = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        priority    = request.form.get('priority', 'Medium')
        due_date    = request.form.get('due_date', '')

        if not title:
            flash('Task title is required!', 'danger')
            return redirect(url_for('add_task'))

        task = Task(title=title, description=description,
                    priority=priority, due_date=due_date)
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_task.html')


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == 'POST':
        task.title       = request.form.get('title', '').strip()
        task.description = request.form.get('description', '').strip()
        task.priority    = request.form.get('priority', 'Medium')
        task.status      = request.form.get('status', 'Pending')
        task.due_date    = request.form.get('due_date', '')

        if not task.title:
            flash('Task title is required!', 'danger')
            return redirect(url_for('edit_task', task_id=task_id))

        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_task.html', task=task)


@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'info')
    return redirect(url_for('index'))


@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_status(task_id):
    task = Task.query.get_or_404(task_id)
    cycle = {'Pending': 'In Progress', 'In Progress': 'Done', 'Done': 'Pending'}
    task.status = cycle.get(task.status, 'Pending')
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/health')
def health():
    return {'status': 'healthy'}, 200


# ── Init DB & Run ──────────────────────────────────────────────────────────────
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Seed sample tasks on first run
        if Task.query.count() == 0:
            samples = [
                Task(title='Set up Flask project',       priority='High',   status='Done',        description='Initialize Flask app with SQLAlchemy', due_date='2024-12-01'),
                Task(title='Design database schema',     priority='High',   status='Done',        description='Create Task model with all required fields', due_date='2024-12-02'),
                Task(title='Build HTML templates',       priority='Medium', status='In Progress', description='Create base, index, add and edit templates', due_date='2024-12-10'),
                Task(title='Add filter functionality',   priority='Medium', status='Pending',     description='Allow filtering tasks by status and priority', due_date='2024-12-15'),
                Task(title='Write project report',       priority='Low',    status='Pending',     description='Document all modules and architecture', due_date='2024-12-20'),
                Task(title='Containerize with Docker',   priority='High',   status='Pending',     description='Create Dockerfile and test container locally', due_date='2024-12-18'),
            ]
            db.session.bulk_save_objects(samples)
            db.session.commit()
    app.run(host='0.0.0.0', port=5000, debug=True)
