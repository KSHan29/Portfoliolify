var socket = io();

// Display incoming messages
socket.on('message', function(data) {
    var messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML += '<p><strong>' + data.username + ': </strong>' + data.message + '</p>';
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Scroll to bottom
});

// Send message
document.getElementById('send-button').addEventListener('click', function() {
    var messageInput = document.getElementById('message-input');
    var message = messageInput.value.trim();
    if (message !== '') {
        socket.emit('message', { message: message });
        messageInput.value = '';
    }
});

// Enter key sends message
document.getElementById('message-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        document.getElementById('send-button').click();
    }
});
