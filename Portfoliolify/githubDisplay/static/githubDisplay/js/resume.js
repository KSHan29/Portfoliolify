// document.addEventListener("DOMContentLoaded", function () {
//   document
//     .getElementById("resume-form")
//     .addEventListener("submit", function (event) {
//       event.preventDefault();

//       const form = event.target;
//       const formData = new FormData(form);
//       const fileSelected = document.getElementById("file-selected");

//       const csrftoken = getCookie("csrftoken"); // Get CSRF token from cookies

//       fetch("/upload/", {
//         method: "POST",
//         headers: {
//           "X-CSRFToken": csrftoken, // Include CSRF token in the request header
//         },
//         body: formData,
//       })
//         .then((response) => response.json())
//         .then((data) => {
//           if (data.error) {
//             fileSelected.textContent = data.error;
//           } else {
//             displaySummary(data.summary);
//           }
//         })
//         .catch((error) => {
//           console.error("Error:", error);
//           fileSelected.textContent =
//             "An error occurred while uploading your resume.";
//         });
//     });

document.getElementById("resume").addEventListener("change", function (event) {
  const input = event.target;
  const fileName =
    input.files.length > 0 ? input.files[0].name : "No file selected";
  document.getElementById("file-selected").textContent = fileName;
});

//   function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== "") {
//       const cookies = document.cookie.split(";");
//       for (let i = 0; i < cookies.length; i++) {
//         const cookie = cookies[i].trim();
//         if (cookie.substring(0, name.length + 1) === name + "=") {
//           cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//           break;
//         }
//       }
//     }
//     return cookieValue;
//   }

//   function displaySummary(summary) {
//     const messageDiv = document.getElementById("message");
//     messageDiv.innerHTML = `
//             <h2>Summary</h2>
//             <p>${summary}</p>
//         `;
//   }
// });
