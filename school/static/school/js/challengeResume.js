document.addEventListener('DOMContentLoaded', () => {

  // QUESTIONS BY CATEGORY CHART
  const questionSetData = JSON.parse(document.getElementById('questions_data').textContent)
  const ctx = document.getElementById('questions-by-category');

  let data = {
    // UPERCASING
    labels: questionSetData.detail.map(detail => (detail.category).charAt(0).toUpperCase() + (detail.category).slice(1)),
    datasets: [
      {
        label: 'Answered',
        data: questionSetData.detail.map(detail => detail.answered),
        backgroundColor: 'rgb(54, 162, 235)',
      },
      {
        label: 'Correct',
        data: questionSetData.detail.map(detail => detail.correct),
        backgroundColor: '#00ff00',
      },
    ]
  };

  let config = {
    type: 'bar',
    data: data,
    options: {
      plugins: {
        title: {
          display: false,
          text: 'Questions By Category'
        },
      },
      responsive: true,
    }
  }
  new Chart(ctx, config);

  // GENERAL RESULTS
  const outro = document.getElementById('general-results')

  data = {
    // UPERCASING
    labels: Object.keys(questionSetData.general).map(str => str.charAt(0).toUpperCase() + str.slice(1))
    ,
    datasets: [
      {
        label: 'Flashcards',
        data: Object.values(questionSetData.general),
        backgroundColor: [
          'rgb(255, 205, 86)',
          '#00ff00',
          'rgb(255, 99, 132)',
        ],
      }
    ]
  };

  config = {
    type: 'doughnut',
    data: data,
    options: {
      plugins: {
        title: {
          display: false,
          text: 'General Results'
        },
      },
      responsive: true,
    }
  }

  new Chart(outro, config);

})