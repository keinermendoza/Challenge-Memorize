document.addEventListener('DOMContentLoaded', () => {


    const data = JSON.parse(document.getElementById('questions_data').textContent)
    const asnwered = data.filter(question => question.answered)
    
    const answered_id = asnwered.map(question => question.id)
    const correct_id = asnwered.filter(question => question.correct).map(question => question.id)
    const wrong_id = asnwered.filter(question => !question.correct).map(question => question.id)
    
    const csrftoken = getCookie('csrftoken');

    const container = document.getElementById('challenge-detail')

    const challeng = new Challenger(container, data, answered_id, correct_id, wrong_id, csrftoken)
    
    // this method check the state of the responses and start the game
    challeng.checkState()

})