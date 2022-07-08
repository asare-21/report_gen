function selectStation(reportId) {
    const report = fmModels.find(e => e.pk == reportId)
    const reportPopUp = document.getElementById("staticBackdrop")
    const title = document.getElementById("staticBackdropLabel")
    const body = document.querySelector(".staticBody")
    const object = document.createElement('object')
    // object.data = `/static/files/${e.pk}.pdf`
    object.data = `/static/files/Northumbria London Campus - Your Conditional Offer.pdf`
    object.type = "application/pdf"
    object.classList = "modal-content"
    object.height = 800

    body.appendChild(object)

    title.textContent = report.fields.name_of_station
    let myModal = new bootstrap.Modal(
        document.getElementById("staticBackdrop"),
        {}
    );

    myModal.show();
}

document.querySelectorAll(".station").forEach(report_card => {
    report_card.addEventListener("click", (e) => {
        const reportId = e.target.parentElement.id
        selectStation(reportId)
    })
})