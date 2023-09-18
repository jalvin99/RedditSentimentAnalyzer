import { useEffect } from 'react';
import { useWebSocket } from '../WebSocketContext';

const SocketHandler = ({ onDataReceived, onSubredditChange }) => {
  const { socket, subreddit } = useWebSocket();

  useEffect(() => {
    if (socket) {
      const messageHandler = (event) => {
        const data = JSON.parse(event.data);
        if (data && data.real_time_data && 'average_sentiment' in data.real_time_data) {
          onDataReceived(data);
        }
      };

      socket.addEventListener('message', messageHandler);

      return () => {
        socket.removeEventListener('message', messageHandler);
      };
    }
  }, [socket, onDataReceived]);

  useEffect(() => {
    if (subreddit && onSubredditChange) {
      onSubredditChange();
    }
  }, [subreddit]);

  return null;
};

export default SocketHandler;
