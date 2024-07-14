document.getElementById("resume").addEventListener("change", function (event) {
  const input = event.target;
  const fileName =
    input.files.length > 0 ? input.files[0].name : "No file selected";
  document.getElementById("file-selected").textContent = fileName;
});

document
  .getElementById("resume-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    fetch("/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.text())
      .then((data) => {
        document.getElementById("message").textContent = data;
      })
      .catch((error) => {
        console.error("Error:", error);
        document.getElementById("message").textContent =
          "An error occurred while uploading your resume.";
      });
  });
