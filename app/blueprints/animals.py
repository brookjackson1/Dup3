from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db

animals = Blueprint('animals', __name__)

@animals.route('/', methods=['GET', 'POST'])
def show_animals():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new animal
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        breed = request.form['breed']
        age = request.form['age']
        gender = request.form['gender']
        size = request.form['size']
        color = request.form['color']
        description = request.form['description']
        medical_notes = request.form['medical_notes']
        arrival_date = request.form['arrival_date']

        # Insert the new animal into the database
        cursor.execute('''INSERT INTO animals (name, species, breed, age, gender, size, color, description, medical_notes, arrival_date)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                       (name, species, breed, age, gender, size, color, description, medical_notes, arrival_date))
        db.commit()

        flash('New animal added successfully!', 'success')
        return redirect(url_for('animals.show_animals'))

    # Handle GET request to display all animals
    cursor.execute('SELECT * FROM animals ORDER BY arrival_date DESC')
    all_animals = cursor.fetchall()
    return render_template('animals.html', all_animals=all_animals)

@animals.route('/update_animal/<int:animal_id>', methods=['POST'])
def update_animal(animal_id):
    db = get_db()
    cursor = db.cursor()

    # Update the animal's details
    name = request.form['name']
    species = request.form['species']
    breed = request.form['breed']
    age = request.form['age']
    gender = request.form['gender']
    size = request.form['size']
    color = request.form['color']
    description = request.form['description']
    adoption_status = request.form['adoption_status']
    medical_notes = request.form['medical_notes']
    arrival_date = request.form['arrival_date']

    cursor.execute('''UPDATE animals SET name = %s, species = %s, breed = %s, age = %s, gender = %s,
                     size = %s, color = %s, description = %s, adoption_status = %s, medical_notes = %s,
                     arrival_date = %s WHERE animal_id = %s''',
                   (name, species, breed, age, gender, size, color, description, adoption_status, medical_notes, arrival_date, animal_id))
    db.commit()

    flash('Animal updated successfully!', 'success')
    return redirect(url_for('animals.show_animals'))

@animals.route('/update_status/<int:animal_id>', methods=['POST'])
def update_status(animal_id):
    db = get_db()
    cursor = db.cursor()

    # Update only the adoption status
    adoption_status = request.form['adoption_status']

    cursor.execute('UPDATE animals SET adoption_status = %s WHERE animal_id = %s',
                   (adoption_status, animal_id))
    db.commit()

    flash('Adoption status updated successfully!', 'success')
    return redirect(url_for('animals.show_animals'))

@animals.route('/delete_animal/<int:animal_id>', methods=['POST'])
def delete_animal(animal_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the animal
    cursor.execute('DELETE FROM animals WHERE animal_id = %s', (animal_id,))
    db.commit()

    flash('Animal deleted successfully!', 'danger')
    return redirect(url_for('animals.show_animals'))

@animals.route('/available')
def show_available():
    db = get_db()
    cursor = db.cursor()

    # Show only available animals
    cursor.execute("SELECT * FROM animals WHERE adoption_status = 'Available' ORDER BY arrival_date DESC")
    available_animals = cursor.fetchall()
    return render_template('animals.html', all_animals=available_animals, filter_type='Available Animals')

@animals.route('/adopt')
def adopt_page():
    db = get_db()
    cursor = db.cursor()

    # Show available animals in a public-friendly format
    cursor.execute("SELECT * FROM animals WHERE adoption_status = 'Available' ORDER BY species, name")
    available_animals = cursor.fetchall()
    return render_template('animals_showcase.html', all_animals=available_animals)

@animals.route('/meet/<int:animal_id>')
def meet_animal(animal_id):
    db = get_db()
    cursor = db.cursor()

    # Get specific animal details
    cursor.execute("SELECT * FROM animals WHERE animal_id = %s", (animal_id,))
    animal = cursor.fetchone()

    if not animal:
        flash('Animal not found.', 'error')
        return redirect(url_for('animals.adopt_page'))

    return render_template('meet_animal.html', animal=animal)