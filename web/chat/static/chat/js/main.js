$(function () {
    chatList()
    $("#sendMessage").click(sendMessage)
});

function chatList() {
    const params = new URLSearchParams(window.location.search);
    $.ajax({
        url: `/api/v1/chat/chats/?${params.toString()}`,
        type: 'get',
        success: successHandler
    })
}

function successHandler (data) {
    const results = data.results
    console.log('success', results)
    const chatList = $('#chatList')
    chatList.empty()
    const template = results.map((chat) => chatTemplate(chat)).join(``)
    chatList.append(template)
    $('.chatList').click(makeActiveChat)

}

function chatTemplate(chat){
    return `
    <li class="clearfix chatList" data-chat-id="${chat.id}" data-chat-name="${chat.name}" data-chat-user-id="${chat.user_id}" data-chat-image="${chat.image}">
        <img src="${chat.image}" alt="avatar">
        <div class="about">
            <div class="name">${chat.name}</div>
            <div class="status"> <i class="fa fa-circle offline"></i> left 7 mins ago </div>
        </div>
    </li>
    `
}

function myMessageTemplate(message) {
    date = formattedDate(message)
    return `
        <li class="clearfix">
            <div class="message-data">
                <span class="message-data-time">${date}</span>
            </div>
            <div class="message my-message">${message.content}</div>
        </li>
    `
}

function otherMessageTemplate (message) {
    image = $('#chatImage').attr('src');
    date = formattedDate(message)
    return `
    <li class="clearfix">
        <div class="message-data text-right">
            <span class="message-data-time">${date}</span>
            <img src=${image} alt="avatar">
        </div>
        <div class="message other-message float-right"> ${message.content} </div>
    </li>
    `
}

function makeActiveChat() {
  if ($(this).hasClass('active')) return
  console.log('clik', $(this).data('chat-id'))
  console.log('clik2', $(this).attr('data-chat-id'))
  const chatItem = $(this)
  const chatId = chatItem.data('chat-id')
  const chatImage = chatItem.data('chat-image')
  const chatName = chatItem.data('chat-name') // достаем имя чата
  const chatUserId = chatItem.data('chat-user-id') // достаем id user

  $('#chatName').text(chatName) // устанавливаем имя чата
  $('.chat-history').attr('data-chatId', chatId) // устанавливаем chatId
  $('.chat-history').attr('data-UserId', chatUserId) // устанавливаем chatUserId
  $('#chatImage').attr('src', chatImage)

  getChatMessages(chatId)

  $('.chatList').removeClass('active')
  chatItem.addClass('active')

  chatSelected(chatId) // если не выбран чат, поле отправки сообщений заблокировано
}


function getChatMessages(chatId) {

    $.ajax({
        url: `/api/v1/chat/messages/${chatId}`,
        type: 'get',
        success: successChatMessagesHandler
    })
}

function successChatMessagesHandler (data) {
    console.log(data)
    // const chatMessages = $('#chatMessages')
    // chatMessages.empty()
    // const template = data.map((message) => myMessageTemplate(message)).join(``)
    // console.log(template)
    // chatMessages.append(template)
    const chatMessages = $('#chatMessages')
    chatMessages.empty()
    for (let message of data){
        var template = getTemplate (message)
        chatMessages.append(template)
    }
//    $('#messageField').on('input',  debounce(startWriteMessage, 2000))
}

$("#messageField").keyup(function(e) {
    if (e.keyCode === 13) {
        sendMessage(e)
    }
});


function chatSelected (chatId) {
    if (chatId === undefined) {
        messageField.disabled = true
        messageField.placeholder = 'Выберите чат!'
    }
    else {
        messageField.disabled = false;
        messageField.placeholder = 'Введите текст здесь...'
      }
}

function formattedDate(data){
    const date = new Date(data.created_at)
    const formatter = new Intl.DateTimeFormat('en-GB', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    })
    const formattedDate = formatter.format(date);
    return formattedDate
}

function getTemplate (message){
     userId = $('.chat-history').attr('data-UserId')

    if (message.author == userId) {
        var template = myMessageTemplate(message)
    }
    else if(message.author != userId) {
        var template = otherMessageTemplate(message)
    }
    return template
}


function addChatToList(name) {
    $.ajax({
      url: `/api/v1/chat/chats/?search=${name}`,
      type: 'get',
      success: addChatToListSuccessHandler
  })
}

function addChatToListSuccessHandler (data) {
  console.log(data.results)
  const addChatTemplate = chatTemplate(data.results[0]);
  const chatList = $('#chatList')
  chatList.append(addChatTemplate);
  $('.chatList').click(makeActiveChat)
}
