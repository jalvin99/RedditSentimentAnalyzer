import React, { useState, useEffect } from 'react';
import ApexCharts from 'react-apexcharts';
import SocketHandler from './SocketHandler';

//by default, apexcharts area chart just stacks the different categories of data on top of each other.
//this converts the visualization to a percentage breakdown
const normalizeData = (dataSeries) => {
  const normalizedSeries = [...dataSeries];
  const length = dataSeries[0].data.length;
  for (let i = 0; i < length; i++) {
    let sum = 0;
    for (const series of dataSeries) {
      sum += series.data[i];
    }
    for (const series of normalizedSeries) {
      if (sum === 0) {
        series.data[i] = 0;
      } else {
        series.data[i] = (dataSeries.find(s => s.name === series.name).data[i] / sum) * 100;
      }
    }
  }
  return normalizedSeries;
};

const EmotionAreaChart = () => {
  const [series, setSeries] = useState([
    { name: 'Joy', data: [] },
    { name: 'Sadness', data: [] },
    { name: 'Anger', data: [] },
    { name: 'Surprise', data: [] },
    { name: 'Fear', data: [] },
    { name: 'Disgust', data: [] },
  ]);

  const [timeStamps, setTimeStamps] = useState([]);

  const onSubredditChange = () => {
    setSeries([
      { name: 'Joy', data: [] },
      { name: 'Sadness', data: [] },
      { name: 'Anger', data: [] },
      { name: 'Surprise', data: [] },
      { name: 'Fear', data: [] },
      { name: 'Disgust', data: [] },
      { name: 'Trust', data: [] },
      { name: 'Anticipation', data: [] },
    ]);
    setTimeStamps([]);
  };

  const onDataReceived = (newData) => {
    const currentTime = new Date().toLocaleTimeString();

    setSeries(prevSeries => {
      const newSeries = prevSeries.map(s => {
        const emotion = s.name.toLowerCase();
        return {
          ...s,
          data: [...s.data, newData.real_time_data[emotion]]
        };
      });

      const normalizedSeries = normalizeData(newSeries);
      
      if (normalizedSeries[0].data.length > 20) {
        normalizedSeries.forEach(s => s.data.shift());
      }

      return normalizedSeries;
    });

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
      type: 'area',
      stacked: true,
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
      min: 0,
      max: 100,
      labels: {
        formatter: (value) => {
          return `${parseFloat(value).toFixed(2)}%`;
        },
        style: {
          colors: '#cfcfcf'
        }
      }
    },
    dataLabels: {
      enabled: false
    },
    fill: {
      type: 'solid',
      opacity: 1
    },
    title: {
      text: 'Emotion Breakdown',
      align: 'center',
      style: {
        color: '#f1f1f1'
      }
    },
    colors: ['#FFFF00', '#008FFB', '#FF4560', '#FEB019', '#775DD0', '#00E396', '#ADD8E6', '#FAF9F6']
  };

  return (
    <>
      <SocketHandler onDataReceived={onDataReceived} onSubredditChange={onSubredditChange} />
      <ApexCharts options={options} series={series} type='area' height={350} />
    </>
  );
};

export default EmotionAreaChart;