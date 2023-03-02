// toogle the open state in card acordeon
function toggleAnswerVisiblity(btn) {
    btn.nextElementSibling.classList.toggle('is-open')
    if (btn.nextElementSibling.classList.contains('is-open')) {
        btn.innerHTML = 'Hide Answer'
    } else {
        btn.innerHTML = 'Show Answer'
    }
}