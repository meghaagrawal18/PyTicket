from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database connection function
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="megha@12345",
        database="movie_ticket"
    )

@app.route('/')
def home():
    # Connect to the database and fetch movie data
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, title, price, showtime, description, image_url FROM movie")
    movies = cursor.fetchall()
    connection.close()

    # Render the home page and pass movie data
    return render_template('index.html', movies=movies)

@app.route('/book-tickets/<int:movie_id>', methods=['GET', 'POST'])
def book_ticket(movie_id):
    # Fetch movie details by ID
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, title, price, showtime, description, image_url FROM movie WHERE id = %s", (movie_id,))
    movie = cursor.fetchone()
    connection.close()

    if not movie:
        return "Movie not found", 404

    if request.method == 'POST':
        # Handle ticket booking form
        name = request.form['name']
        seats = int(request.form['seats'])
        total_price = movie['price'] * seats

        # Save the booking to the database
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO bookings (movie_id, customer_name, seats, total_price) VALUES (%s, %s, %s, %s)",
            (movie_id, name, seats, total_price)
        )
        connection.commit()
        connection.close()

        # Render booking confirmation page
        return render_template('booking_confirmation.html', name=name, seats=seats, movie=movie, total_price=total_price)

    # Render book tickets page
    return render_template('book_tickets.html', movie=movie)

if __name__ == '__main__':
    app.run(debug=True)
