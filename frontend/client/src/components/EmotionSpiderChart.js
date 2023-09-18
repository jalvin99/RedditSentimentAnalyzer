import React, { useState, useEffect } from 'react';
import ApexCharts from 'react-apexcharts';
import SocketHandler from './SocketHandler';

const EmotionSpiderChart = () => {

  const [series, setSeries] = useState([
    {
      name: "Emotions",
      data: [0, 0, 0, 0, 0, 0, 0, 0]
    }
  ]);

  const onSubredditChange = () => {
    setSeries([
      {
        name: 'Emotions',
        data: [0, 0, 0, 0, 0, 0, 0, 0]
      }
    ]);
  };

  const onDataReceived = (newData) => {
    const newEmotionData = [
      newData.real_time_data.joy,
      newData.real_time_data.sadness,
      newData.real_time_data.anger,
      newData.real_time_data.surprise,
      newData.real_time_data.fear,
      newData.real_time_data.disgust,
      newData.real_time_data.trust,
      newData.real_time_data.anticipation
    ];
    setSeries([{ name: 'Emotions', data: newEmotionData }]);
  };

  const options = {
    chart: {
        type: 'area',
        height: 300, 
        width: '100%',
        background: '#1e1e1e',
        foreColor: '#cfcfcf',
        toolbar: {
          show: false
        }
    },
    title: {
      text: 'Emotion Breakdown',
      align: 'center'
    },
    xaxis: {
      categories: ['Joy', 'Sadness', 'Anger', 'Surprise', 'Fear', 'Disgust','Trust', 'Anticipation'],
      labels: {
        style: {
          colors: '#cfcfcf'
        }
      }  
    },
    yaxis: {
        show:false,
        labels: {
          style: {
            colors: '#cfcfcf'
          }
        }
      },
    grid: {
        borderColor: '#444'
      },
      title: {
        text: 'Emotion Gravity',
        align: 'center',
        style: {
          color: '#f1f1f1'
        }
      },
    fill: {
      opacity: 0.5,
    },
    colors: ['#00E396', '#008FFB', '#FEB019', '#FF4560', '#775DD0', '#ADD8E6', '#FAF9F6'],
  };

  return (
    <>
      <SocketHandler onDataReceived={onDataReceived} onSubredditChange={onSubredditChange}/>
      <ApexCharts options={options} series={series} type="radar" />
    </>
  );

};

export default EmotionSpiderChart;
