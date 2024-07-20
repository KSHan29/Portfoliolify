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

function sendMessage(link) {
  var message = $("#user-input").val();
  if (message.trim() === "") {
    return;
  }
  $("#messages").append(
    "<div class='text-messages'><strong>You:</strong> " + message + "</div>"
  );
  $("#user-input").val("");
  const username = document.getElementById("username").value;

  $("#loading-spinner").show();
  $("#input-button").hide();
  console.log(`/${link}${username}/`);
  $.post(`/${link}${username}/`, {
    message: message,
    csrfmiddlewaretoken: csrftoken,
  })
    .done(function (data) {
      if (data.error) {
        console.error(data.error);
        $("#messages").append(
          "<div class='text-messages'><strong>Error:</strong> " +
            data.error +
            "</div>"
        );
      } else {
        $("#messages").append(
          "<div class='text-messages'><strong>ChatGPT:</strong> " +
            data.message +
            "</div>"
        );
      }
    })
    .fail(function (jqXHR, textStatus, errorThrown) {
      console.error("Request failed: " + textStatus + ", " + errorThrown);
      $("#messages").append(
        "<div class='text-messages'><strong>Error:</strong> " +
          textStatus +
          "</div>"
      );
    })
    .always(function () {
      $("#loading-spinner").hide();
      $("#input-button").show();
    });
}
const url = document.getElementById("url").value;
console.log(url);
const inputButton = document.getElementById("input-button");
const inputBox = document.getElementById("user-input");
inputBox.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    e.preventDefault();
    sendMessage(url);
  }
});

inputButton.addEventListener("click", () => sendMessage(url));
