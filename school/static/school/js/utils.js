document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.toogle-answer')
    .forEach(btn => {
        
        btn.onclick = (e) => {
            const  el = e.target
            console.log(el.nextElementSibling)
        }
    })
    
})