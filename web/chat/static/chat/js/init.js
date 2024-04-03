$(function () {
  chatInitHandler()
});

function chatInitHandler() {
  const params = new URLSearchParams(window.location.search);
  console.log(params.toString())
  $.ajax({
    url: `/api/v1/chat/init/?${params.toString()}`,
    type: 'post',
    data: {user_id: params.get('userId')},
    success: successHandler,
  })
}

function successHandler(data){
  window.location.href = "/chat/main/"
}
