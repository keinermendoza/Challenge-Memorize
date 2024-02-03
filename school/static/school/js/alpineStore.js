htmx.on("htmx:afterRequest", (e) => {
    if (Array.from(e.target.classList).includes("form-card")) {
        if (e.detail.successful) {
            e.target.reset()
            e.target.question.focus()
        }
    }
})


// CONFIRMATION DELETING CARD
// document.addEventListener("htmx:confirm", function(e) {
//     if (Array.from(e.target.classList).includes('delete-card'))  { 
//         e.preventDefault()
  
//       // Mostrar un cuadro de diálogo personalizado con Swal
//       Swal.fire({
//         title: "Please Confirm deletion",
//         text: `${e.detail.question}`
//       }).then(function(result) {
//         if (result.isConfirmed) {
//             const event = new CustomEvent("delete-note");
//             e.target.dispatchEvent(event)
//             e.detail.issueRequest(true); // this continue the request

//         } 
//       });
//     }
// });



// CREATING CARD
// https://www.reddit.com/r/htmx/comments/10hu6wp/how_to_know_which_event_was_triggered/
htmx.on("htmx:afterRequest", (e) => {
    // if (Array.from(e.target.classList).includes("form-notes")) {
    //     if (e.detail.successful) {
    //         e.target.note.value = ''
    //         const event = new CustomEvent("upp-note-counter");
    //         e.target.dispatchEvent(event)

    //         Swal.fire({
    //             icon: "success",
    //             title: "Note Created",
    //             showConfirmButton: false,
    //             timer: 1500
    //         });

    //     } else {

    //         console.log(e)
    //         console.log(e.target)

    //         Swal.fire({
    //             icon: "error",
    //             title: "Oops...",
    //             text: e.detail.xhr.responseText,
    //             showConfirmButton: false,
    //             timer: 2500
    //         });

    //     }
    // } 
    // // EDITING NOTE
    // else if (Array.from(e.target.classList).includes("form-edit-notes")) {
    //     if (e.detail.successful) {
    //         e.target.note.value = ''
    //         const event = new CustomEvent("set-editing-false");
    //         e.target.dispatchEvent(event)

    //         Swal.fire({
    //             icon: "success",
    //             title: "Note Updated",
    //             showConfirmButton: false,
    //             timer: 1500
    //         });

    //     } else {

    //     console.log(e)
    //     console.log(e.target)

    //     Swal.fire({
    //         icon: "error",
    //         title: "Oops...",
    //         text: e.detail.xhr.responseText,
    //         showConfirmButton: false,
    //         timer: 2500
    //       });

    //     }
    // }

    // DELETE CARD ANIMATION AND MESSAGE 
     if (Array.from(e.target.classList).includes("btn-delete-card")) {
        if (e.detail.successful) {
            const card = e.target.parentElement.parentElement
            console.log(e.target.parentElement)
            card.classList.add("deleted-card-animation")

            // it's necesary delete the parent element
            // TODO change gap in ul by mb in the li. for  
            card.onanimationend = (e) => e.target.parentElement.parentElement.remove()
        }
        //     Swal.fire({
        //         icon: "success",
        //         title: "Note Updated",
        //         showConfirmButton: false,
        //         timer: 1500
        //     });

        // } else {

        // console.log(e)
        // console.log(e.target)

        // Swal.fire({
        //     icon: "error",
        //     title: "Oops...",
        //     text: e.detail.xhr.responseText,
        //     showConfirmButton: false,
        //     timer: 2500
        //   });

        // }
    } 
});