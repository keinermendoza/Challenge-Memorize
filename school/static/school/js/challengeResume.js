document.addEventListener('DOMContentLoaded', () => {


    const data = JSON.parse(document.getElementById('questions_data').textContent)
    // const asnwered = data.filter(question => question.answered)
    
    // const answered_id = asnwered.map(question => question.id)
    // const correct_id = asnwered.filter(question => question.correct).map(question => question.id)
    // const wrong_id = asnwered.filter(question => !question.correct).map(question => question.id)
    
    // constl csrftoken = getCookie('csrftoken');

    // const container = document.getElementById('challenge-detail')

    // const challeng = new Challenger(container, data, answered_id, correct_id, wrong_id, csrftoken)
    
    // this method check the state of the responses and start the game
    // challeng.checkState()


  const ctx = document.getElementById('myChart');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: [data.detail.map(detail => detail.category)],
      datasets: [
        {
            label: 'Questions Answered',
            data: [data.detail.map(detail => detail.answered)],
            borderWidth: 1
        },
        {
            label: 'Correct Answered',
            data: [data.detail.map(detail => detail.correct)],
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

  // const outro = document.getElementById('outro')

  // const data = {
  //   labels: [
  //     'Red',
  //     'Blue',
  //     'Yellow'
  //   ],
  //   datasets: [{
  //     label: 'My First Dataset',
  //     data: [300, 50, 100],
  //     backgroundColor: [
  //       'rgb(255, 99, 132)',
  //       'rgb(54, 162, 235)',
  //       'rgb(255, 205, 86)'
  //     ],
  //     hoverOffset: 4
  //   }]
  // };

  // const config = {
  //   type: 'doughnut',
  //   data: data,
  // };

  // new Chart(outro, config)
})