import React, { createContext, useContext, useEffect, useState } from 'react';

const WebSocketContext = createContext({
    socket: null,
    setSubreddit: () => {},
    subreddit: null
  });

export const useWebSocket = () => {
  return useContext(WebSocketContext);
};

//closes and reestablishes websocket with new subreddit after each subreddit change
//this might not be the best way to do this? might refactor later
export const WebSocketProvider = ({ children }) => {
  const [socket, setSocket] = useState(null);
  const [subreddit, setSubreddit] = useState('askreddit');

  useEffect(() => {

    if (socket) {
        socket.close();
        console.log('WebSocket closed due to subreddit change.');
      }

      
    console.log('WebSocket URL:', `${process.env.REACT_APP_WS_URL}${subreddit}`);

    const ws = new WebSocket(`${process.env.REACT_APP_WS_URL}${subreddit}`);


    ws.addEventListener('open', () => {
      console.log('WebSocket opened');
    });

    ws.addEventListener('close', (event) => {
      console.log('WebSocket close event', event);
    });

    /*
    ws.addEventListener('message', (message) => {
      console.log('WebSocket message', message);
    });
    */

    ws.addEventListener('error', (error) => {
      console.error('WebSocket Error:', error);
    });

    setSocket(ws);

    return () => {
      ws.close();
      console.log('WebSocket closed');
    };
  }, [subreddit]);

  return (
    <WebSocketContext.Provider value={{ socket, setSubreddit, subreddit }}>
      {children}
    </WebSocketContext.Provider>
  );
};