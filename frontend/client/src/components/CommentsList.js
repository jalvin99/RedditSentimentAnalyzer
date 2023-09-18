import React, { useState, useEffect, useRef } from 'react';
import { useWebSocket } from '../WebSocketContext';
import axios from 'axios';

const CommentsList = () => {
  const [comments, setComments] = useState([]);
  const [sortBy, setSortBy] = useState("sentiment_score");
  const [timeRange, setTimeRange] = useState("today");
  const [keyword, setKeyword] = useState(""); 
  const [offset, setOffset] = useState(0);
  const [forceUpdate, setForceUpdate] = useState(false);

  const { subreddit } = useWebSocket();
  const listContainerRef = useRef(null);

  const [inputValue, setInputValue] = useState("");
  const [inputSortBy, setInputSortBy] = useState("sentiment_score");
  const [inputTimeRange, setInputTimeRange] = useState("today");

  //need to refactor later, shouldn't be fetching data inside a use effect
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_AXIOS_URL}comments`, {
          params: {
            subreddit: subreddit,
            sort_by: sortBy,
            time_range: timeRange,
            keyword: keyword,
            offset: offset,
            limit: 10
          }
        });

        setComments(prevComments => [...prevComments, ...response.data.comments]);
      } catch (error) {
        console.error("An error occurred while fetching data: ", error);
      }
    };
  
    fetchData();
  }, [subreddit, forceUpdate]);
  
  const handleSearch = () => {
    setComments([]); // clear existing comments
    setTimeRange(inputTimeRange);
    setSortBy(inputSortBy);
    setKeyword(inputValue);
    setOffset(0);
    setForceUpdate(prev => !prev);
  };

  useEffect(() => {
    const currentRef = listContainerRef.current;

    //fetch more data if user has scrolled far enough that remaining comments fill less than
    //the the height of the window (plus tolerance)
    function handleScroll() {
      const { scrollHeight, scrollTop, clientHeight } = listContainerRef.current;
      const tolerance = 5;
      if (scrollHeight - scrollTop <= clientHeight + tolerance) {
        setOffset(prevOffset => prevOffset + 10);
        setForceUpdate(prev => !prev);
      }
    }
    currentRef.addEventListener('scroll', handleScroll);

    return () => {
      currentRef.removeEventListener('scroll', handleScroll);
    };
  }, []);

  useEffect(() => {
    handleSearch();
  }, [subreddit]);

  return (
    <div>
      <div className="filter-controls">
        <span>Comments with the highest </span>
        <select onChange={e => setInputSortBy(e.target.value)} value={inputSortBy}>
          <option value="sentiment_score">Overall Positivity</option>
          <option value="joy">Joy</option>
          <option value="anger">Anger</option>
          <option value="fear">Fear</option>
          <option value="disgust">Disgust</option>
          <option value="surprise">Surprise</option>
          <option value="sadness">Sadness</option>
          <option value="trust">Trust</option>
          <option value="anticip">Anticipation</option>
        </select>
        <span> in the last </span>
        <select onChange={e => setInputTimeRange(e.target.value)} value={inputTimeRange}>
          <option value="today">Day</option>
          <option value="this_week">Week</option>
          <option value="this_month">Month</option>
          <option value="this_year">Year</option>
        </select>
        <span> containing the word </span>
        <input type="text" value={inputValue} placeholder="Enter keyword" onChange={e => setInputValue(e.target.value)} />
        <button onClick={handleSearch}>Search</button>
      </div>
      <ul className="commentsList" ref={listContainerRef}>
        {comments.map((comment, index) => (
          <li key={index}>{comment.author_name}: {comment.content} - 
          <a href={`https://www.reddit.com${comment.permalink}`} target="_blank" rel="noopener noreferrer">
          {comment.permalink}
        </a></li>
        ))}
      </ul>
    </div>
  );
};

export default CommentsList;