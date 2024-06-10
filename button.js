const messageInput = document.getElementById('message');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', function() {
  const message = messageInput.value;
  // Send the message to the Flask app using AJAX
  fetch('/submit', {
    method: 'POST',
    body: JSON.stringify({ message: message }),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(data => {
    // Update the chat messages with the response from the Flask app
    const chatMessages = document.getElementById('chat-messages');
    const chatMessagesHTML = data.messages.map(message => {
      return `<li class="${message.type}">${message.text}</li>`
    }).join('');
    chatMessages.innerHTML = chatMessagesHTML;
  })
  .catch(error => {
    console.error('Error:', error);
  });

  messageInput.value = '';
});
