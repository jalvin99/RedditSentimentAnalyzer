import React, { useState, useEffect } from 'react';
import ApexCharts from 'react-apexcharts';
import SocketHandler from './SocketHandler';

const SentimentChart = () => {
  const [series, setSeries] = useState([
    {
      name: 'Sentiment',
      data: []
    }
  ]);

  const [timeStamps, setTimeStamps] = useState([]);

  const onSubredditChange = () => {
    setSeries([
      {
        name: 'Sentiment',
        data: []
      }
    ]);
    setTimeStamps([]);
  };

  const onDataReceived = (newData) => {
    const currentTime = new Date().toLocaleTimeString();
    
    setSeries(prevSeries => {
      let newSeries = [...prevSeries];
      newSeries[0].data = [...newSeries[0].data, newData.real_time_data.average_sentiment];
      
      if(newSeries[0].data.length > 20){
        newSeries[0].data.shift();
      }
      return newSeries;
    });

    //keep the view within 20 timestamps worth of time
    setTimeStamps(prevTimeStamps => {
      const newTimeStamps = [...prevTimeStamps, currentTime];
      if (newTimeStamps.length > 20) {
        newTimeStamps.shift();
      }
      return newTimeStamps;
    });
  };

  const options = {
    chart: {
      type: 'line',
      height: 300,
      background: '#1e1e1e',
      foreColor: '#cfcfcf',
      toolbar: {
        show: false
      }
    },
    xaxis: {
      categories: timeStamps,
      labels: {
        style: {
          colors: '#cfcfcf'
        }
      }
    },
    yaxis: {
      labels: {
        formatter: (value) => {
          return parseFloat(value).toFixed(3);
        },
        style: {
          colors: '#cfcfcf'
        }
      }
    },
    grid: {
      borderColor: '#444'
    },
    stroke: {
      curve: 'smooth',
    },
    title: {
      text: 'Overall Positivity',
      align: 'center',
      style: {
        color: '#f1f1f1'
      }
    },
    colors: ['#00E396', '#008FFB', '#FEB019', '#FF4560', '#775DD0']
  };

  return (
    <>
      <SocketHandler onDataReceived={onDataReceived} onSubredditChange={onSubredditChange} />
      <ApexCharts options={options} series={series} type='line' height={350} />
    </>
  );
};

export default SentimentChart;
