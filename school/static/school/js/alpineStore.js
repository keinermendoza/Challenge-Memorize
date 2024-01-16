htmx.on("htmx:afterRequest", (e) => {
    if (Array.from(e.target.classList).includes("form-card")) {
        if (e.detail.successful) {
            e.target.reset()
            e.target.question.focus()
        }
    }
})