class Challenger {
    constructor(container, data, answered, correct, wrong, csrftoken) {
		this.container = container;        
		this.data = data;
        this.csrftoken = csrftoken
        this.btnWrong;
		this.btnCorrect;


        this.answered = answered
        this.correct = correct
        this.wrong = wrong

        this.question = 0;
        
        this.render;
        this.createBtns();
        this.jsConfetti;
        this.clickWrong;
        this.clickCorrect;
    }

    putRequest(userResponse) {
        fetch(this.data[this.question].url, {
            method: 'PUT',
            body: JSON.stringify({'correct' : userResponse}),
            headers: {"X-CSRFToken":this.csrftoken},
        }).then(res => console.log(res.status))
    }


    clickWrong() {
        this.jsConfetti.addConfetti({
            emojis: ['💩'],
            emojiSize: 60,
            confettiNumber: 1,
          })

        this.putRequest(false)
        this.wrong.push(this.data[this.question].id)
        this.answered.push(this.data[this.question].id)
        this.checkState()
    }

    clickCorrect() {
        this.jsConfetti.addConfetti()
        this.putRequest(true)
        this.correct.push(this.data[this.question].id)
        this.answered.push(this.data[this.question].id)
        this.checkState()
    }

    checkState() {
        if (this.answered.length < this.data.length) {     
            this.nextTurn()
        } else {
            this.end()
        }
    }

    nextTurn() {
        if (this.answered.includes(this.data[this.question].id)) {
            ++this.question
            this.checkState()
        } else {
            this.render()
        }
    }

    end() {
        this.jsConfetti.addConfetti({
            emojis: ['💎'],
            emojiSize: 30,
            confettiNumber: 70,
          })

        this.render()
        this.btnCorrect.style.display = 'none'
        this.btnWrong.style.display = 'none'
        
    }

    createBtns() {
        this.jsConfetti = new JSConfetti()

        this.btnWrong = document.createElement('button')
        this.btnCorrect = document.createElement('button')
        
        this.btnWrong.innerHTML = 'Wrong'
        this.btnCorrect.innerHTML = 'Correct'

        this.btnWrong.className = 'rounded bg-green-500 text-black py-1 px-2 transition-colors border-2 border-amber-300 hover:bg-green-600 active:scale-95' 
        this.btnCorrect.className = 'rounded bg-green-500 text-black py-1 px-2 transition-colors border-2 border-amber-300 hover:bg-green-600 active:scale-95'


        this.btnCorrect.onclick = () => this.clickCorrect()
        this.btnWrong.onclick = () => this.clickWrong()
    }

    render() {
        // clean the container before next render
        this.container.innerHTML = ''

        // create container for header counters
		const headerCounters = document.createElement('div')
        headerCounters.className = "flex justify-between"


        // render new card
		const cardContainer = document.createElement('div')
        cardContainer.innerHTML = `

        <div>
            <div class="text-sm sm:text-lg sm:font-semibold m-3 py-2 px-4 bg-darkbody flex justify-between gap-3 mb-3">
                <span class="text-center">
                    Correct: ${this.correct.length}

                </span>            

                <span class="text-center">
                    Wrong: ${this.wrong.length}
                </span>
                
                <span class="text-center">
                    Answered: ${this.answered.length}/${this.data.length}
                </span>

            </div>

            <article class="mx-3">
                <div class="mb-3 flex justify-between">
                    <span class="text-sm rounded px-2 py-1 bg-darkbody">
                        ${this.data[this.question].category.toUpperCase()}
                        
                    </span>
                    <span class="text-sm rounded px-2 py-1 bg-darkbody">
                        ${this.data[this.question].level}
                    </span>
                </div>

                <h3 class="mb-3 text-xl font-semibold">
                    ${this.data[this.question].question}
                </h3>
            
            
                <div class="text-end">
                    <button onclick="toggleAnswerVisiblity(this)" class="rounded bg-green-500 text-black py-1 px-2 transition-colors border-2 border-amber-300 hover:bg-green-600 active:scale-95">Show</button>
                </div>

                <div class="answer-acordeon">
                    <div class="answer" >
                        <p>${this.data[this.question].answer}</p>
                    </div>
                </div>
            </article>

            
        </div>



         
        `
        // create html container for buttons
        const buttonContainer = document.createElement('div')
        buttonContainer.className = "flex justify-between mt-3 py-4 px-3 bg-teal-700"
        buttonContainer.append(this.btnCorrect, this.btnWrong)
        
        // insert card and buttons in the container
        this.container.append(cardContainer, buttonContainer)
	}    
}