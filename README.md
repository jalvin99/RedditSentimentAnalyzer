# Reddit Sentiment Analysis Application
## Project Overview

This project is a streaming data pipline that fetches live comments from Reddit's 'r/all' subreddit using the Python Reddit API Wrapper. It performs sentiment analysis on each comment's body text using the NLTK library and emotion analysis using NRCLex. The resulting scores are appended to the comment data and written to a PostgreSQL table. Users can view a moving average of any subreddit's sentiment and emotion scores in the React frontend through various charting components. Users can also specify a particular keyword and emotion to view a list of comments ranked by that emotion. This project takes advantage of containerization using Docker.

# Table of Contents
- [Project Overview](#project-overview)
- [Table of Contents](#table-of-contents)
- [Architecture](#architecture)
- [Installation and Setup](#installation-and-setup)
- [Improvements](#improvements)
- [Acknowledgements](#acknowledgements)

# Architecture

![reddit_sentiment_analysis_pipeline_architecture](https://github.com/jalvin99/RedditSentimentAnalyzer/blob/master/images/RedditSentimentAnalyzer_drawio.png?raw=true)

The above diagram illustrates the architecture of the streaming data pipeline. 

All applications are containerized into **Docker** containers.

1. **Data Ingestion :** A Python script called *fetch_comments* connects to the Reddit API using credentials provided in a `prawconfig.env` file. It takes a stream of received comments and performs sentiment analysis and emotion analysis using the NLTK and NRCLex libraries. The comment along with its new sentiment and emotion scores are converted into JSON form. [PRAW](https://praw.readthedocs.io/en/stable/) python library is used for interacting with Reddit API. A containerized Python application called *write_to_database* uses *fetch_comments* to obtain the stream of processed reddit comments in JSON form and injects the fields into a **PostgreSQL** table.

2. **Processed Data Storage :** A simple **PostgreSQL** table called reddit_comments holds all the original data initially received in *fetch_comments* along with 11 new fields - sentiment_score, anger, anticip, disgust, fear, joy, negative, positive, sadness, surprise, and trust.

3. **Backend API :** A containerized Python application called *main.py* sets up **FastAPI** endpoints for the frontend to obtain sentiment and emotion data for comments.
   Two endpoints are provided:
    - A **WebSocket** endpoint takes a specified subreddit in the url. On 1 second intervals, it calculates the average sentiment score and emotion scores of all comments written to the PostgreSQL table over the last 60 seconds. It returns this data in JSON form.
    - A HTTP GET endpoint that takes a variety of fields in the url, including subreddit, keyword, time range and others. The endpoint function returns a list of dictionaries containing all comments filtered by those fields. This is converted into JSON by FastAPI.

5. **Data Visualization :** A **React** frontend provides a variety of components for visualizing real-time sentiment and emotion data for reddit comments. ApexCharts is used to render several different times of charts, including line chart, area chart, and spider chart. Data normalization has to be performed for the area chart to provide a % breakdown of each emotion. 

These three charts display the moving average of all comments in the specified subreddit in terms of sentiment and emotion scores over the last 60 seconds.

A comments list component allows users to find all comments posted in a particular subreddit over a specified period of time that contain a given keyword.

![reddit_sentiment_analysis_demo](https://github.com/jalvin99/RedditSentimentAnalyzer/blob/master/images/demoapp.gif?raw=true)

# Installation and Setup
## System Requirements
- [Docker Engine](https://www.docker.com/)

The project was tested with the following local system configuration:
- Docker Engine: 24.0.6
- OS: Windows 11
- RAM: 8 GB
- CPU cores: 4
- Graphics card: NVIDIA GeForce RTX 3050

To setup the project locally, first you will have to add .env files for setting up and accessing the database as well as enabling connection to the Reddit API. Instructions for doing so are provided in the three .env.template files in the backend/ directory. 

For prawconfig.env, you'll need to obtain Reddit Developer credentials by creating an application at https://www.reddit.com/prefs/apps/.

Once your .env files are ready, simply navigate in your terminal to the root directory RedditSentimentAnalyzer/ and run `docker-compose build` to create the **Docker** images and then `docker-compose up` to create the containers. The application can then be accessed at http://localhost:3000.

# Improvements
- Design patterns: There are several less-than-optimal design patterns that were used for the sake of getting this project up quickly and easy testing. For example, the FastAPI backend doesnt use any model classes or ORM Mapping and instead uses large SQL queries to directly inject data into the database. Data is also being passed directly rather than being wrapped in a response entity. This was for the sake of speedy development so that all data could easily be viewed in console output.

- Testing: There is zero testing currently in this project, unit, integration, or otherwise. I test everything thoroughly at work but should probably still maintain good habits when it comes to side projects. However, this is mostly a toy project that I wanted to get up and running ASAP.

# Acknowledgements
1. [nama1arpit Reddit Streaming Data Pipeline Project](https://github.com/nama1arpit/reddit-streaming-pipeline)
2. Libraries - [NRCLex](https://pypi.org/project/NRCLex/), [NLTK](https://www.nltk.org/), [PRAW](https://praw.readthedocs.io/en/stable/)
