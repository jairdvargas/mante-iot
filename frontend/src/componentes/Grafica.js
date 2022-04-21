import React from 'react';
import { Line } from 'react-chartjs-2';
import Card from 'react-bootstrap/Card';

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
  } from 'chart.js';
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);


const Grafica = ({nombreTagHist, ejeYTagHist, ejeXTagHist}) => {
  let labels=[];
  labels=ejeXTagHist;
  const options = {
    responsive: true,
    plugins: {
      title: {
        display: false,
        text: 'Variable: ' + nombreTagHist,
      },
      legend: {
        display:false,
      },
    },
  };
  const data = {
    labels,
    datasets: [
      {
        label: nombreTagHist,
        data: ejeYTagHist,
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
    ],
  };
  
  return (
    <Card style={{ width: '50rem', height: '30rem' }}>
        <Card.Header>{nombreTagHist}</Card.Header>
        <Card.Body>
        <Line options={options} data={data} /> 
        </Card.Body>
    </Card>
  );
};

export default Grafica;