import React from 'react';
import './App.css';
import SentimentLineChart from './components/SentimentChart';
import EmotionAreaChart from './components/EmotionAreaChart';
import EmotionSpiderChart from './components/EmotionSpiderChart';
import CommentsList from './components/CommentsList';
import SearchBar from './components/SearchBar';
import { WebSocketProvider } from './WebSocketContext';

function App() {
  return (
    <WebSocketProvider>
      <SearchBar />
      <div className="main-container">
        <div className="container">
          <div className="top-chart">
            <div className="chart">
              <SentimentLineChart />
            </div>
          </div>
          <div className="bottom-charts">
            <div className="chart">
              <EmotionAreaChart />
            </div>
            <div className="chart">
              <EmotionSpiderChart />
            </div>
          </div>
        </div>
        <div className="list-container">
          <CommentsList />
        </div>
      </div>
    </WebSocketProvider>
  );
}

export default App;