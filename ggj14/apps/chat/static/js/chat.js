var templates;
var $channelWindow;

function templateFromId(id) {
  var source = $(document.getElementById(id)).html();
  return Handlebars.compile(source);
}

function showMessage(message) {
  $channelWindow.append(templates.msg(message));
  window.scroll(0, document.body.scrollHeight);
}

function bindPrompt() {
  var $form = $('form#input');
  var $prompt = $($form.find('#prompt'));

  $form.submit(function(e) {
    e.preventDefault();
    var clientMessage = $prompt.val();
    if (clientMessage === '') {
      return;
    }

    showMessage({
      origin: 'client',
      nick: 'you',
      content: clientMessage
    });

    $prompt.val('');

    $.ajax({
      type: 'POST',
      url: postMessageURL,
      data: {message: clientMessage},
      success: function(dataString) {
        var data = $.parseJSON(dataString);
        $(data.messages).each(function(i, message) {
          setTimeout(function() {
            showMessage(message);
          }, message.delay);
        });
      },
      error: function() {
        // XXX do something
      }
    });
  });

  $prompt.focus();
}

$(function() {
  $channelWindow = $('#channel ul');
  templates = {
    msg: templateFromId('msg')
  };
  bindPrompt();
});
