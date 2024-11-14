from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from models import db, Event
from functools import wraps
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Simple decorator to require login for protected routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):  # Check if user is logged in
            flash('You must be logged in to view this page.', 'danger')
            return redirect(url_for('login'))  # Redirect to login page if not logged in
        return f(*args, **kwargs)
    return decorated_function

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == app.config['ADMIN_USERNAME'] and password == app.config['ADMIN_PASSWORD']:
            session['logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('event_page'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

# Route for events page (protected)
@app.route('/events')
@login_required
def event_page():
    events = Event.query.all()  # Retrieve all events from the database
    return render_template('events.html', events=events)

# Route for add_event page (protected)
@app.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image = request.files['image']

        # Check if an image was uploaded
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Save event to the database
            new_event = Event(title=title, description=description, image_filename=filename)
            db.session.add(new_event)
            db.session.commit()

            flash('Event added successfully!', 'success')
            return redirect(url_for('event_page'))
        else:
            flash('Invalid image file format. Please upload PNG, JPG, or JPEG images.', 'danger')
    return render_template('add_event.html')

# Function to check if the file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Clear the session
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
