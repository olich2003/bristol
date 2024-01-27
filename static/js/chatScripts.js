
chatAreaScrollDown();


document.getElementById("btn_send_msg").onclick = sendMessegeProccess;


//clears the placeholder text ion the chatbox
//this function is set to run when the users brings focus to the chatbox, by clicking on it
function placeHolder() {
  document.getElementById("chatbox").placeholder = "";
}

function sendMessegeProccess() {
    var msg_text = $('#chatbox').val();

    if (msg_text.length != 0) {
        $.ajax({
            url: '/chat_api',          /* Куда пойдет запрос */
            method: 'post',             /* Метод передачи (post или get) */
            dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
            data: {
                msg: msg_text,
                token: ($('#msg_token').val())},     /* Параметры передаваемые в запросе. */
            success: function(data){   /* функция которая будет выполнена после успешного запроса.  */
                console.log(data);            /* В переменной data содержится ответ от /chat_api */
            }
        });
    } 
    $('#chatbox').val("");
    requestAvailableMessage();
}


function requestAvailableMessage() {
  $.ajax({
      url: '/chat_api', 
      method: 'get',  
      dataType: 'json',         
      data: {
          user_current_last_msg_id: getCookie('last_msg_id'),
          token: ($('#msg_token').val())},     
      success: function(data){ 
          // Прийти должен массив сообщений. Формат:  [2, 'Name Surname', 'message text', '18:23 08.10']
        for (var i = data.length - 1; i >= 0; i--) {
          $("#msg_box").append(
            $('<p>', {class:"item_msg"})
              .append($('<span><a href="{{url_for("user_page", user_id='+data[i][0]+')}}" style="color:'+data[i][4]+';">'+data[i][1]+'</a>:</span> '))
              .append($('<span> '+data[i][2]+'</span>'))
              .append($('<span class="msg_time"><em>'+data[i][3]+'</em></span>'))
          )
        }
        if (data.length > 0) {
          $("#small_down_icon").css("width", "64px");
        }            
      }
  });
}


function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

function chatAreaScrollDown() {
  var b = document.getElementById("msg_box");
  b.scrollTop = b.scrollHeight;
  $("#small_down_icon").css("width", "0px");
}

var intervalId = window.setInterval(function(){
    requestAvailableMessage();
    console.log("1")
}, 5000);



var b = document.getElementById("msg_box");
var i = document.getElementById("small_down_icon");

b.onscroll = function() {
  console.log(this.scrollTop + " " + this.scrollHeight);
  $("#small_down_icon").css("width", "64px");
  if (this.scrollHeight - this.scrollTop === this.clientHeight) {
        $("#small_down_icon").css("width", "0px");
    }
};



i.onclick = chatAreaScrollDown;