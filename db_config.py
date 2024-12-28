# import mysql.connector
#
# def get_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="megha@12345",
#         database="movie_ticket"
#     )

import mysql.connector
from mysql.connector import Error


def get_connection():
    """
    Establish a connection to the MySQL database
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='movie_ticket',
            user="root",
            password="megha@12345",
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return None


# Create tables if not exists
def init_db():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()

        # Create movie table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS movie (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            genre VARCHAR(100),
            price DECIMAL(10,2),
            showtime DATETIME
        )
        ''')

        # Create bookings table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            movie_id INT,
            customer_name VARCHAR(255),
            seats INT,
            total_price DECIMAL(10,2),
            booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (movie_id) REFERENCES movie(id)
        )
        ''')

        # Check if movies already exist
        cursor.execute("SELECT COUNT(*) FROM movie")
        movie_count = cursor.fetchone()[0]

        # Insert sample data only if no movies exist
        if movie_count == 0:
            cursor.executemany(
                "INSERT INTO movie (title, genre, price, showtime) "
                "VALUES (%s, %s, %s, %s)",
                [
                    ('Inception', 'Sci-Fi', 12.50, '2024-03-15 19:00:00'),
                    ('The Dark Knight', 'Action', 11.00, '2024-03-15 20:30:00'),
                    ('Interstellar', 'Sci-Fi', 13.00, '2024-03-16 18:45:00')
                ]
            )

        conn.commit()
        conn.close()