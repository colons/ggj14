var templates;
var $channelWindow;

function templateFromId(id) {
  var source = $(document.getElementById(id)).html();
  return Handlebars.compile(source);
}

function showMessage(html) {
  $channelWindow.append(html);
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

    showMessage(templates.msg({
      origin: 'client',
      nick: 'you',
      content: clientMessage
    }));

    $prompt.val('');

    $.ajax({
      type: 'POST',
      url: postMessageURL,
      data: {message: clientMessage},
      success: function(dataString) {
        var data = $.parseJSON(dataString);
        $(data.messages).each(function(i, message) {
          setTimeout(function() {
            showMessage(templates.msg(message));
          }, message.delay);
        });
      },
      error: function() {
        // XXX do something better here
        alert('THERE WAS AN ERROR sorry i will handle this better in future');
      }
    });
  });

  $prompt.focus();
}

function connect() {
  var ms = 0;
  var messages = [
    [0, 'connecting to irc.biz.ru:6697...'],
    [900, '!irc.biz.ru *** Looking up your hostname...'],
    [700, '!irc.biz.ru *** Checking ident...'],
    [300, '!irc.biz.ru *** Received identd response'],
    [100, '!irc.biz.ru *** Found your hostname'],
    [500, "              _                                "],
    [10, "__      _____| | ___ ___  _ __ ___   ___       "],
    [10, "\\ \\ /\\ / / _ \\ |/ __/ _ \\| '_ ` _ \\ / _ \\      "],
    [10, " \\ V  V /  __/ | (_| (_) | | | | | |  __/_ _ _ "],
    [10, "  \\_/\\_/ \\___|_|\\___\\___/|_| |_| |_|\\___(_|_|_)"],
    [10, ""],
    [900, "joined #t('_'t)"],
    [50, "channel topic is: ヽ(`Д´)ノ"],
    [100, "users: [~phoenix420] [@Anna]"]  // XXX use actual name of our foil
  ];
  
  $.each(messages, function(i, thing) {
    ms += thing[0];
    setTimeout(function() {
      showMessage(templates.status({content: thing[1]}));
    }, ms);
  });
}

$(function() {
  $channelWindow = $('#channel ul');
  templates = {
    msg: templateFromId('msg'),
    status: templateFromId('status')
  };
  connect();
  bindPrompt();
});
