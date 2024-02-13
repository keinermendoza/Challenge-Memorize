htmx.on("htmx:afterRequest", (e) => {
    if (Array.from(e.target.classList).includes("form-card")) {
        if (e.detail.successful) {
            e.target.reset()
            e.target.question.focus()
        }
    }
})


htmx.on("htmx:afterRequest", (e) => {
    if (Array.from(e.target.classList).includes("flashcard-create")) {
        if (e.detail.successful) {
            document.querySelector(".delete-on-create-flashcard").remove()
        }
    }
})

htmx.on("htmx:afterRequest", (e) => {
    if (Array.from(e.target.classList).includes("form-category")) {
        if (e.detail.successful) {
            e.target.name.value = ""
        }
    }
})


htmx.on("htmx:afterRequest", (e) => {
    if (Array.from(e.target.classList).includes("flashcard-edit")) {
        if (e.detail.successful) {
            if(e.detail.target.id == "flashcard-edit-container") {
                showEditModal()
            }
        }
    }
})

// CREATING CARD
// https://www.reddit.com/r/htmx/comments/10hu6wp/how_to_know_which_event_was_triggered/
htmx.on("htmx:afterRequest", (e) => {

     if (Array.from(e.target.classList).includes("btn-delete-card")) {
        if (e.detail.successful) {
            const card = document.querySelector(e.target.dataset.parent)
            card.classList.add("deleted-card-animation")

            // it's necesary delete the parent element
            // TODO change gap in ul by mb in the li. for  
            card.onanimationend = (e) => card.remove()
        }
  
    } 
});