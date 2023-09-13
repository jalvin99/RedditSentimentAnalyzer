import psycopg2
from psycopg2 import sql

# Initialize the database connection
conn = psycopg2.connect(
    dbname="postgres",  # Update with your DB name
    user="postgres",
    password="llamas8243",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

from datetime import datetime

def write_to_db(comment):
    # Convert the Unix timestamp to a PostgreSQL-compatible timestamp
    comment_timestamp = datetime.fromtimestamp(comment['timestamp']).strftime('%Y-%m-%d %H:%M:%S')

    insert_query = sql.SQL(
        "INSERT INTO reddit_comments (id, name, author, body, subreddit, upvotes, downvotes, over_18, timestamp, permalink, sentiment_score, anger, anticip, disgust, fear, joy, negative, positive, sadness, surprise, trust) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )

    cursor.execute(insert_query, (
        comment['id'], comment['name'], comment['author'], comment['body'],
        comment['subreddit'], comment['upvotes'], comment['downvotes'],
        comment['over_18'], comment_timestamp['comment_timestamp'], comment['permalink'],
        comment['sentiment_score'], comment['anger'], comment['anticip'],
        comment['disgust'], comment['fear'], comment['joy'], comment['negative'],
        comment['positive'], comment['sadness'], comment['surprise'], comment['trust']
    ))

    conn.commit()

if __name__ == "__main__":
    from fetch_comments import fetch_comments  # Make sure fetch_comments.py is in the same directory
    subreddit_list = ['all']
    for comment in fetch_comments(subreddit_list):
        write_to_db(comment)
