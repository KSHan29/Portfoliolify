document.addEventListener("DOMContentLoaded", () => {
  fetch("/api/projects")
    .then((response) => response.json())
    .then((data) => {
      const projectsDiv = document.getElementById("projects");
      data.projects.forEach((project) => {
        const projectDiv = document.createElement("div");
        projectDiv.className = "project";
        projectDiv.innerHTML = `
                    <h2>${project.name}</h2>
                    <p>${project.description}</p>
                    <a href="${project.html_url}" target="_blank">View on GitHub</a>
                `;
        projectsDiv.appendChild(projectDiv);
      });
    });
});
