<template>
    <div>
      <h1>Question 1 results:</h1>
      <div id="chart-container">
        <canvas id="pie-chart"></canvas>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import Chart from 'chart.js/auto';
  
  export default {
    name: 'PieChart',
    setup() {
      const chart = ref(null);
  
      onMounted(() => {
        fetch('http://127.0.0.1:5000/api/radio_data')
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            const colorCounts = {};
            data.forEach(color => {
              colorCounts[color] = (colorCounts[color] || 0) + 1;
            });
  
            const labels = Object.keys(colorCounts);
            const values = Object.values(colorCounts);
  
            const backgroundColors = ['red', 'blue', 'green', 'purple', 'yellow']; // Add more colors as needed
            
            const ctx = document.getElementById('pie-chart').getContext('2d');
            chart.value = new Chart(ctx, {
              type: 'pie',
              data: {
                labels: labels,
                datasets: [{
                  data: values,
                  backgroundColor: backgroundColors
                }]
              },
              options: {
                responsive: true,
                maintainAspectRatio: false
              }
            });
          })
          .catch(error => {
            console.error('Error fetching radio data:', error);
          });
      });
  
      return {
        chart
      };
    }
  };
  </script>
  
  <style>
  #chart-container {
  width: 400px; /* Set the width of the container */
  height: 400px; /* Set the height of the container */
}
  </style>
  