const archivedAndCloseConfirmation = (id, action) => {
    console.log(action)
    let action_result = action === "archive";
    let close = "Are you sure to close this scholarship?";
    let archive = "Are you sure to archive this scholarship"
    Swal.fire({
        title: action_result ? "Confirm Archive" : "Confirm Close",
        icon: "question",
        text: action_result ? archive : close,
        showCancelButton: true,
        confirmButtonText: action_result ? "Archive" : "Close",
        confirmButtonColor: '#dc3545',
    }).then((result) => {
        if (result.isConfirmed){
            window.location.href = `/administrator/archive-scholarship/${id}/${action}/`
        }
    });
}