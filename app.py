from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projector_data.db'
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Add a secret key for flash messages
db = SQLAlchemy(app)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projector_id = db.Column(db.String(50), nullable=False)
    teacher_id = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

@app.route('/')
def home():
    try:
        bookings = Booking.query.all()
        return render_template('home.html', bookings=bookings)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        if request.method == 'POST':
            projector_id = request.form.get('projector_id')
            teacher_id = request.form.get('teacher_id')
            date = request.form.get('date')
            phone = request.form.get('phone')

            new_booking = Booking(projector_id=projector_id, teacher_id=teacher_id, date=date, phone=phone)
            db.session.add(new_booking)
            db.session.commit()

            # Fetch all bookings from the database to display on the same page
            bookings = Booking.query.all()

            return render_template('home.html', bookings=bookings)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return render_template('home.html')

@app.route('/return_projector', methods=['POST'])
def return_projector():
    try:
        if request.method == 'POST':
            return_teacher_id = request.form.get('return_teacher_id')

            # Find and remove the booking from the database based on the teacher ID
            booking_to_remove = Booking.query.filter_by(teacher_id=return_teacher_id).first()
            if booking_to_remove:
                db.session.delete(booking_to_remove)
                db.session.commit()

            # Fetch all bookings from the database to display on the same page
            bookings = Booking.query.all()

            return render_template('home.html', bookings=bookings)
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return render_template('home.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
