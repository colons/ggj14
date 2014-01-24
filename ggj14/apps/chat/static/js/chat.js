var templates;
var $channelWindow;

function templateFromId(id) {
  var source = $(document.getElementById(id)).html();
  return Handlebars.compile(source);
}

function showMessage(message) {
  $channelWindow.append(templates.msg(message));
  window.scroll(0, $('body').height() + $(window).height());
}

function bindPrompt() {
  var $form = $('form#input');
  var $prompt = $($form.find('#prompt'));

  $form.submit(function(e) {
    e.preventDefault();

    showMessage({
      origin: 'client',
      nick: 'you',
      content: $prompt.val()
    });

    $prompt.val('');

    $.ajax({
      type: 'POST',
      url: postMessageURL,
      data: {message: $prompt.val()},
      success: function(dataString) {
        var data = $.parseJSON(dataString);
        setTimeout(function() {
          console.log(data.message);
          showMessage(data.message);
        }, data.delay);
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
