from datetime import datetime, timedelta

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from databases import Database

from database import database
import logging
import asyncio
import traceback

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('databases').setLevel(logging.INFO)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()
    logging.debug("Server started and database connected")

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    logging.debug("Server shutting down and database disconnected")

async def get_db():
    yield database

async def fetch_average_sentiment(subreddit, db):
    query = '''
    SELECT AVG(sentiment_score) 
    FROM reddit_comments 
    WHERE subreddit=:subreddit AND timestamp >= current_timestamp - interval '60 seconds'
    '''
    return await db.fetch_val(query=query, values={'subreddit': subreddit}) or 0

async def fetch_average_emotions(subreddit, db):
    query = '''
    SELECT AVG(joy) as joy, AVG(sadness) as sadness, AVG(anger) as anger, 
           AVG(surprise) as surprise, AVG(fear) as fear, AVG(disgust) as disgust,
           AVG(trust) as trust, AVG(anticip) as anticipation
    FROM reddit_comments
    WHERE subreddit=:subreddit AND timestamp >= current_timestamp - interval '60 seconds'
    '''
    values = await db.fetch_one(query=query, values={'subreddit': subreddit})
    return dict(values) if values else {'joy': 0, 'sadness': 0, 'anger': 0, 'surprise': 0, 'fear': 0, 'disgust': 0, 'trust': 0, 'anticipation': 0}

#endpoint for populating CommentsList component in frontend
@app.get("/comments")
async def read_comments(subreddit: str = Query(None, alias="subreddit"),
                        sort_by: str = Query(..., alias="sort_by"),
                        time_range: str = Query(..., alias="time_range"),
                        keyword: str = Query(None, alias="keyword"),
                        offset: int = 0, limit: int = 10, db: Database = Depends(get_db)):

    valid_sort_columns = ["sentiment_score", "joy", "sadness", "anger", "surprise", "fear", "disgust", "anticip",
                          "trust"]

    #protecting against SQL injection
    if sort_by not in valid_sort_columns:
        raise HTTPException(status_code=400, detail="Invalid sort_by value")

    end_date = datetime.now()
    if time_range == "today":
        start_date = end_date - timedelta(days=1)
    elif time_range == "this_week":
        start_date = end_date - timedelta(weeks=1)
    elif time_range == "this_month":
        start_date = end_date - timedelta(weeks=4)
    elif time_range == "this_year":
        start_date = end_date - timedelta(weeks=52)
    else:
        raise HTTPException(status_code=400, detail="Invalid time_range value")

    query = f'''
    SELECT author, body, upvotes, downvotes, permalink, sentiment_score,
           anger, anticip, disgust, fear, joy, sadness, surprise, trust
    FROM reddit_comments 
    WHERE timestamp BETWEEN :start_date AND :end_date
    '''

    params = {'start_date': start_date, 'end_date': end_date, 'offset': offset, 'limit': limit}

    if subreddit:
        query += " AND subreddit = :subreddit"
        params["subreddit"] = subreddit

    if keyword:
        keyword = f"%{keyword}%"
        query += " AND body LIKE :keyword"
        params["keyword"] = keyword

    query += f" ORDER BY {sort_by} DESC OFFSET :offset LIMIT :limit;"

    comments = await db.fetch_all(query=query, values=params)

    comments_dict_list = [
        {"author_name": x["author"], "content": x["body"], "upvotes": x["upvotes"], "downvotes": x["downvotes"],
         "permalink": x["permalink"], "sentiment_score": x["sentiment_score"], "anger": x["anger"],
         "anticipation": x["anticip"],
         "disgust": x["disgust"], "fear": x["fear"], "joy": x["joy"], "sadness": x["sadness"],
         "surprise": x["surprise"],
         "trust": x["trust"]} for x in comments]

    return {"comments": comments_dict_list}

#endpoint for data used in SentimentChart, EmotionSpiderChart, and EmotionAreaChart components
@app.websocket("/ws/{subreddit}")
async def websocket_endpoint(websocket: WebSocket, subreddit: str, keyword: str = Query(None),
                             db: Database = Depends(get_db)):
    #logging.debug(f"Attempting to accept a new WebSocket connection for subreddit: {subreddit}")

    await websocket.accept()

    #logging.debug("WebSocket connection accepted.")

    try:
        while True:
            avg_sentiment_score = await fetch_average_sentiment(subreddit, db)
            avg_emotion_values = await fetch_average_emotions(subreddit, db)

            await websocket.send_json({
                "real_time_data": {
                    "average_sentiment": avg_sentiment_score,
                    **avg_emotion_values
                }
            })
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"An error occurred: {e}")
        # Print full traceback
        #traceback.print_exc()