document.addEventListener('DOMContentLoaded', () => {

  const ctx = document.getElementById('myChart');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [
        {
            label: '# Objective',
            data: [12, 19, 3, 5, 2, 3],
            borderWidth: 1
        },
        {
            label: '# Results',
            data: [12, 9, 1, 5, 1, 3],
            borderWidth: 1
        },
    
        ]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });

  const outro = document.getElementById('outro')

  const data = {
    labels: [
      'Red',
      'Blue',
      'Yellow'
    ],
    datasets: [{
      label: 'My First Dataset',
      data: [300, 50, 100],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)'
      ],
      hoverOffset: 4
    }]
  };

  const config = {
    type: 'doughnut',
    data: data,
  };

  new Chart(outro, config)
})