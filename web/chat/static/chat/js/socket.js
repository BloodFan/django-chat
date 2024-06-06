const chatSocket = new ReconnectingWebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log('receive message', data)
    if ( data.action === 'send_message') {
        addMessage(data)
        console.log(window.location.host)
    }
    else if ( data.action === 'chat_created' ) {
        const element = document.querySelector(`[data-chat-id="${data.chat_id}"]`);
        if (!element){
          addChatToList(data.init_user.full_name)
          const full_name = data.init_user.full_name
          alert(`Пользователь ${full_name} Создал с вами чат!`)
        }
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};


function sendMessage (e) {
    const message = $("#messageField").val();
    const chatId = $('.chat-history').attr('data-chatId')
    if (!validateMessage(message)) return
    if (chatId === undefined) return
    const data = {'command': 'sendMessage', 'data': {'content': message, 'chatId': chatId}}
    chatSocket.send(JSON.stringify(data))
    $("#messageField").val("") // после отправления текст сообщения удаляется
    console.log(message, chatId)

    const element = document.getElementById("messageField");
    element.scrollIntoView(true);
}

function startWriteMessage (e) {
    const chatId = $('.chat-history').attr('data-chatId')
    if (e.originalEvent.inputType === 'insertText' || e.originalEvent.inputType === 'deleteContentBackward') {
        const data = {
            'command': 'startWriteMessage',
            'data': {'message': 'User write message','chatId': chatId}
        }
        chatSocket.send(JSON.stringify(data))
    }
}

function addMessage(data) {
    const chatMessages = $('#chatMessages')
    data['created_at'] = new Date(data['created_at']) // обход JSON, str -> date
    var template = getTemplate (data)
    chatMessages.append(template)
}

function  debounce(func,delay) {
  var timer = 0
  return function (e) {
    console.log(e)
    if (Date.now() - timer > delay) {
      func(e);
    }
    timer = Date.now()
  }
}
