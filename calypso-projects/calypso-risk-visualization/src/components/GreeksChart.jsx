import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import './GreeksChart.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const GreeksChart = ({ data }) => {
  if (!data || data.length === 0) {
    return <div className="greeks-chart">No data available</div>;
  }

  const chartData = {
    labels: data.map(d => d.instrument || d.book),
    datasets: [
      {
        label: 'Delta',
        data: data.map(d => d.delta || 0),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
      },
      {
        label: 'Gamma',
        data: data.map(d => d.gamma || 0),
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
      },
      {
        label: 'Vega',
        data: data.map(d => d.vega || 0),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      },
      {
        label: 'Theta',
        data: data.map(d => d.theta || 0),
        backgroundColor: 'rgba(255, 206, 86, 0.6)',
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Greeks by Instrument'
      }
    },
    scales: {
      y: {
        beginAtZero: true
      }
    }
  };

  return (
    <div className="greeks-chart">
      <h3>Greeks Visualization</h3>
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default GreeksChart;



