function showPopup(message) {
    const modal = document.getElementById("myModal");
    const modalMessage = document.getElementById("modalMessage");
    modalMessage.textContent = message;
    modal.style.display = "block";
}
function closeModal() {
    const modal = document.getElementById("myModal");
    modal.style.display = "none";
    const downloadButton = document.getElementById("downloadButton");
    downloadButton.style.display = "block";
}
function downloadFile() {
    console.log("downloadFile");
    const downloadFile = document.getElementById("downloadFile");
    const downloadButton = document.getElementById("downloadButton");
    downloadButton.style.display = "block";
    downloadFile.style.display = "block";
    const fileValue = downloadFile.value;             
    const link = document.createElement('a');
    link.href = `/static/${fileValue}`;
    link.download = `${fileValue}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
}
// Close the modal when the user clicks anywhere outside of the modal
// window.onclick = function(event) {
//     const modal = document.getElementById("myModal");
//     if (event.target == modal) {
//         modal.style.display = "none";
//     }
// }

//  GENERAR PROYECTO

function changeBtnObtn (){
    const downloadButton = document.getElementById("downloadButton");
    downloadButton.style.display = "none";
}

// async function startTask() {
//     const downloadButton = document.getElementById("downloadButton");
//     const loadingMessage = document.getElementById("loadingMessage");
//     downloadButton.style.display = "none";
//     loadingMessage.style.display = "block";
//     const response = await fetch('/obt_reporte');
//     const data = await response.text(); //
//     document.body.innerHTML = data; 
//     showPopup("Generado el reporte de la fecha actual"); // Show the modal with the result
//     downloadButton.style.display = "block";
//     loadingMessage.style.display = "none";
// }


/// 
document.addEventListener('DOMContentLoaded', function() {
    const currentDate = new Date(); // Get the current date
    const currentDateString = currentDate.toISOString().split('T')[0]; // Format as yyyy-mm-dd
    document.getElementById('dateInput').value = currentDateString; // Set the current date in the input
});
