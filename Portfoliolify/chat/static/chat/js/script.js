function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie("csrftoken");
console.log(`CSRF Token: ${csrftoken}`); // Log the CSRF token

function sendMessage() {
  console.log("called");
  var message = $("#user-input").val();
  if (message.trim() === "") {
    return;
  }
  $("#messages").append("<div><strong>You:</strong> " + message + "</div>");
  $("#user-input").val("");
  console.log("called2");
  const username = document.getElementById("username").value;
  $.post(`/chat/${username}/`, {
    message: message,
    csrfmiddlewaretoken: csrftoken,
  })
    .done(function (data) {
      if (data.error) {
        console.error(data.error);
        $("#messages").append(
          "<div><strong>Error:</strong> " + data.error + "</div>"
        );
      } else {
        $("#messages").append(
          "<div><strong>ChatGPT:</strong> " + data.message + "</div>"
        );
      }
    })
    .fail(function (jqXHR, textStatus, errorThrown) {
      console.error("Request failed: " + textStatus + ", " + errorThrown);
      $("#messages").append(
        "<div><strong>Error:</strong> " + textStatus + "</div>"
      );
    });
  console.log("called3");
}
