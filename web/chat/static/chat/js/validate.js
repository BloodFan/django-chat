function validateMessage(message) {
  // let messageField = document.getElementById('messageField') ПОЧЕМУ необьявленная переменная работает???
  switch (true) {
    case message.includes('нехорошее слово'):
      messageField.placeholder = 'НЕ РУГАЙТЕСЬ!'
      messageField.value = ''
      return false
    case message === '':
      messageField.placeholder = 'ВВЕДИТЕ СООБЩЕНИЕ!'
      return false
    default:
      return true
  }
}
