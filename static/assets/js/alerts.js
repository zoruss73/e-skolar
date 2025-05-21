const messages = {
    close : {
        title: "Confirm Close",
        body: "Are you sure to close this scholarship?",
        button: "Close",
        color: "#dc3545"
    },
    open : {
        title: "Confirm Open",
        body: "Are you sure to open this scholarship?",
        button: "Open",
        color: "#059652"
    },
}

const archivedAndCloseConfirmation = (id, action) => {
    const {title : titleText, body : bodyText, button :buttonText, color : buttonColor} = messages[action]
    
    Swal.fire({
        title: titleText,
        icon: "question",
        text: bodyText,
        showCancelButton: true,
        confirmButtonText: buttonText,
        confirmButtonColor: buttonColor,
    }).then((result) => {
        if(result.isConfirmed){
            window.location.href = `/administrator/archive-scholarship/${id}/${action}/`
        }
    });
}