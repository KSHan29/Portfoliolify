document.addEventListener("DOMContentLoaded", function () {
  const projects = document.querySelectorAll(".project");
  projects.forEach(function (project) {
    const checkbox = project.querySelector(".hidden-checkbox");
    console.log(checkbox.checked);
    if (checkbox.checked) {
      project.classList.add("selected");
    }
    project.addEventListener("click", function () {
      checkbox.checked = !checkbox.checked;
      project.classList.toggle("selected", checkbox.checked);
    });
  });
});
