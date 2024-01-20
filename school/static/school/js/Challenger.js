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
		console.log('wrong')
        this.putRequest(false)
        this.wrong.push(this.data[this.question].id)
        this.answered.push(this.data[this.question].id)
        this.checkState()
    }

    clickCorrect() {
		console.log('correct')
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
        this.render()
        console.log('THE END')
        this.btnCorrect.style.display = 'none'
        this.btnWrong.style.display = 'none'
        
    }

    createBtns() {
        this.btnWrong = document.createElement('button')
        this.btnCorrect = document.createElement('button')
        
        this.btnWrong.innerHTML = 'Wrong'
        this.btnCorrect.innerHTML = 'Correct'

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
            <div class="text-sm sm:text-lg sm:font-semibold py-2 px-1 bg-darkbody flex justify-around gap-3 mb-3">
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

            <article class="">
                <div class="mb-3 flex justify-between">
                    <span class="text-sm rounded px-2 py-1 bg-darkbody">
                        ${this.data[this.question].category}
                        
                    </span>
                    <span class="text-sm rounded px-2 py-1 bg-darkbody">
                        ${this.data[this.question].level}
                    </span>
                </div>

                <h3 class="mb-3 text-xl font-semibold">
                    ${this.data[this.question].question}
                </h3>
            
            
                <div class="text-end">
                    <button onclick="toggleAnswerVisiblity(this)" class="p-3 bg-blue-500">Show Answer</button>
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
        buttonContainer.className = "flex justify-between"
        buttonContainer.append(this.btnCorrect, this.btnWrong)
        
        // insert card and buttons in the container
        this.container.append(cardContainer, buttonContainer)
	}    
}