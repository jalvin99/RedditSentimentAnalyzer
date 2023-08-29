-- Table for individual comments
CREATE TABLE comments (
  uuid UUID PRIMARY KEY,
  id TEXT,
  name TEXT,
  author TEXT,
  body TEXT,
  subreddit TEXT,
  upvotes INT,
  downvotes INT,
  over_18 BOOLEAN,
  timestamp FLOAT,
  permalink TEXT,
  sentiment_score FLOAT,
  VADER_neg FLOAT,
  VADER_neu FLOAT,
  VADER_pos FLOAT,
  NRC_anger FLOAT,
  NRC_anticipation FLOAT,
  NRC_disgust FLOAT,
  NRC_fear FLOAT,
  NRC_joy FLOAT,
  NRC_sadness FLOAT,
  NRC_surprise FLOAT,
  NRC_trust FLOAT
);

-- Table for subreddit average sentiment
CREATE TABLE subreddit_sentiment_avg (
  uuid UUID PRIMARY KEY,
  subreddit TEXT,
  sentiment_score_avg FLOAT,
  VADER_neg_avg FLOAT,
  VADER_neu_avg FLOAT,
  VADER_pos_avg FLOAT,
  NRC_anger_avg FLOAT,
  NRC_anticipation_avg FLOAT,
  NRC_disgust_avg FLOAT,
  NRC_fear_avg FLOAT,
  NRC_joy_avg FLOAT,
  NRC_sadness_avg FLOAT,
  NRC_surprise_avg FLOAT,
  NRC_trust_avg FLOAT
);
