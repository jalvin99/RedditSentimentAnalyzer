CREATE TABLE reddit_comments (
    comment_pk SERIAL PRIMARY KEY,
    id TEXT,
    name TEXT,
    author TEXT,
    body TEXT,
    subreddit TEXT,
    upvotes INTEGER,
    downvotes INTEGER,
    over_18 BOOLEAN,
    permalink TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ingest_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sentiment_score FLOAT,
    anger FLOAT,
    anticip FLOAT,
    disgust FLOAT,
    fear FLOAT,
    joy FLOAT,
    negative FLOAT,
    positive FLOAT,
    sadness FLOAT,
    surprise FLOAT,
    trust FLOAT
);