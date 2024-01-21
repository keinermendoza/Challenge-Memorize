// toogle the open state in card acordeon
function toggleAnswerVisiblity(btn) {
    btn.parentElement.nextElementSibling.classList.toggle('is-open')
    if (btn.parentElement.nextElementSibling.classList.contains('is-open')) {
        btn.innerHTML = 'Hide Answer'
    } else {
        btn.innerHTML = 'Show Answer'
    }
}

// DELETE FLASHCARD

function removeFlashcard(btn) {
    const card = btn.parentElement.parentElement.parentElement.parentElement // li element
    console.log(card)
    card.classList.add("deleted-card-animation")
    // card.onanimationend = (e) => e.target.remove()
}


// MODAL
function showEditModal() {
    document.getElementById('flashcard-edit-container').showModal()
}

function closeEditModal() {
    document.getElementById('flashcard-edit-container').close()
}

// clean errors from a particular form
document.addEventListener('DOMContentLoaded', () => {
    document.body.addEventListener("clean_errors", (e) => {
        e.target.querySelectorAll('.error-message').forEach(error => error.remove())
    })
})

function selectAll(checkboxAll) {
    document.querySelectorAll('.category-checkbox').forEach(checkbox => checkbox.checked = checkboxAll.checked) //.check = checkboxAll.check 
}