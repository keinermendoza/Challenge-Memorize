// toogle the open state in card acordeon
function toggleAnswerVisiblity(btn) {
    btn.parentElement.nextElementSibling.classList.toggle('is-open')
    if (btn.parentElement.nextElementSibling.classList.contains('is-open')) {
        btn.innerHTML = 'Hide'
    } else {
        btn.innerHTML = 'Show'
    }
}

// DELETE MESSAGE
function deleteparent(btn) {
    document.querySelector(btn.dataset.parent).remove()
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

// CHALLENGE CREATE SELECT ALL
function selectAll(checkboxLabel) {
    const checkboxAll = checkboxLabel.querySelector(checkboxLabel.dataset.checkbox)
    document.querySelectorAll('.category-checkbox').forEach(checkbox => checkbox.checked = checkboxAll.checked) //.check = checkboxAll.check 
}