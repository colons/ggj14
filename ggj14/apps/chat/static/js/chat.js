var templates;
var $channelWindow;

function templateFromId(id) {
  var source = $(document.getElementById(id)).html();
  return Handlebars.compile(source);
}

function showMessage(message) {
  $channelWindow.append(templates.msg(message));
}

function bindClientInput() {
  var $form = $('form#input');
  var $input = $($form.find('input'));

  $form.submit(function(e) {
    e.preventDefault();

    showMessage({
      origin: 'client',
      nick: 'you',
      content: $input.val()
    });

    $input.val('');
  });
}

$(function() {
  $channelWindow = $('#channel ul');
  templates = {
    msg: templateFromId('msg')
  };
  bindClientInput();
});
