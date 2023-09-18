import React, { useState } from 'react';
import { useWebSocket } from '../WebSocketContext';

const SearchBar = () => {
  const [tempSubreddit, setTempSubreddit] = useState('askreddit');
  const { setSubreddit } = useWebSocket();

  const handleTempSubredditChange = (e) => {
    const newValue = e.target.value;
    const valueAfterR = newValue.split('r/')[1] || ''; // 'r/' always in text field to indicate subreddit
    setTempSubreddit(valueAfterR);
  };

  //db is holding the subreddit field for all comments as lowercase, so we need to search using lowercase
  const handleSearchClick = () => {
    const lowerCaseSubreddit = tempSubreddit.toLowerCase();
    setSubreddit(lowerCaseSubreddit);
  };

  return (
    <div className="search-bar">
      <div className="website-title">
      HowsRedditFeeling?
      </div>
      <div className="search-input">
      <input
        type="text"
        value={`r/${tempSubreddit}`}
        placeholder="Enter subreddit"
        onChange={handleTempSubredditChange}
      />
      <button onClick={handleSearchClick} className="search-button">
        Search
      </button>
      </div>
      <div className="empty-div"></div>
    </div>
  );
};

export default SearchBar;