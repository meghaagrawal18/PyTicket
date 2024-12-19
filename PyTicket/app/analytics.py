import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from app.db_config import get_connection


class MovieTicketAnalytics:
    def __init__(self):
        self.conn = get_connection()
        self.reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
        os.makedirs(self.reports_dir, exist_ok=True)

    def load_data(self):
        """
        Load movie and booking data into Pandas DataFrames
        """
        # Load Movies Data
        movies_query = "SELECT * FROM movie"
        movies_df = pd.read_sql(movies_query, self.conn)

        # Load Bookings Data
        bookings_query = """
        SELECT b.*, m.title, m.genre, m.price as movie_price
        FROM bookings b
        JOIN movie m ON b.movie_id = m.id
        """
        bookings_df = pd.read_sql(bookings_query, self.conn)

        return movies_df, bookings_df

    def generate_analytics_data(self):
        """
        Generate analytics data for template rendering
        """
        # Load data
        movies_df, bookings_df = self.load_data()

        # Total Revenue
        total_revenue = bookings_df['total_price'].sum()

        # Most Booked Movies
        most_booked_movies = bookings_df.groupby('title')['seats'].sum().nlargest(5)

        # Peak Booking Times
        bookings_df['booking_hour'] = pd.to_datetime(bookings_df['booking_time']).dt.hour
        peak_booking_times = bookings_df.groupby('booking_hour')['seats'].sum()

        # Revenue Trends
        bookings_df['booking_date'] = pd.to_datetime(bookings_df['booking_time']).dt.date
        revenue_trends = bookings_df.groupby('booking_date')['total_price'].sum()

        # Visualization
        plt.figure(figsize=(15, 5))

        # Most Booked Movies Bar Chart
        plt.subplot(1, 3, 1)
        most_booked_movies.plot(kind='bar', ax=plt.gca())
        plt.title('Top Booked Movies')
        plt.xlabel('Movie Title')
        plt.ylabel('Total Seats')
        plt.xticks(rotation=45, ha='right')

        # Peak Booking Times Bar Chart
        plt.subplot(1, 3, 2)
        peak_booking_times.plot(kind='bar', ax=plt.gca())
        plt.title('Peak Booking Hours')
        plt.xlabel('Hour of Day')
        plt.ylabel('Total Seats Booked')

        # Revenue Trends Line Chart
        plt.subplot(1, 3, 3)
        revenue_trends.plot(kind='line', marker='o', ax=plt.gca())
        plt.title('Daily Revenue Trends')
        plt.xlabel('Date')
        plt.ylabel('Total Revenue')
        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()

        # Save plot
        plot_path = os.path.join(self.reports_dir, 'analytics_dashboard.png')
        plt.savefig(plot_path)
        plt.close()

        return {
            'total_revenue': total_revenue,
            'most_booked_movies': most_booked_movies.to_dict(),
            'peak_booking_times': peak_booking_times.to_dict(),
            'revenue_trends': revenue_trends.to_dict(),
            'plot_path': plot_path
        }