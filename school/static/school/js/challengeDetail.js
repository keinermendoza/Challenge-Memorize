document.addEventListener('DOMContentLoaded', () => {
    data = [
        {   
            id:0,
            question: 'what lenguage is the best',
            answer:'my first title',
            category:'python',
        },
        {
            id:1,
            question: 'number and name',
            answer:'my second title',
            category:'javascript',
        },
        {
            id:2,
            question: 'is this platzi',
            answer:'that is ok',
            category:'php',
        },
        {
            id:3,
            question: 'name and number',
            answer:'my fourth title',
            category:'python',
        },
    ]

    const container = document.getElementById('challenge-detail')

    const challeng = new Challenger(container, data)
    challeng.render()

})