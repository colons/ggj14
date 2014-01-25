var events;
var templates;

var $channelWindow;
var $form;
var $prompt;

function templateFromId(id) {
  var source = $(document.getElementById(id)).html();
  return Handlebars.compile(source);
}

function showMessage(html) {
  $channelWindow.append(html);
  scrollToBottom();
}

function scrollToBottom() {
  window.scroll(0, document.body.scrollHeight);
}

function showStatusMessage(content) {
  showMessage(templates.status({content: content}));
}

function bindPrompt() {
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
    unbindPrompt();

    $.ajax({
      type: 'POST',
      url: postMessageURL,
      data: {message: clientMessage},
      success: function(dataString) {
        var data = $.parseJSON(dataString);
        var longestDelay = 0;
        var hasEvent = false;

        $(data.messages).each(function(i, message) {
          // we don't want to automatically show the prompt if there's an event
          // attached to this exchange, so we will make a note of if this is
          // one or not
          if (message.event) {
            hasEvent = true;
          }

          setTimeout(function() {
            if (message.event) {
              events[message.event]();
            } else {
              showMessage(templates[message.type](message));
            }
          }, message.delay);

          if (message.delay > longestDelay) {
            longestDelay = message.delay;
          }
        });

        if (!hasEvent) {
          setTimeout(bindPrompt, longestDelay);
        }
      },
      error: function() {
        // XXX do something better here
        alert('THERE WAS AN ERROR sorry i will handle this better in future');
      }
    });

    $form.focus();
  });

  $form.slideDown();
  $prompt.focus();
}

function unbindPrompt() {
  $form.submit(function(e) {
    e.preventDefault();
  });

  $form.slideUp();
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
    [900, "joined " + channelName],
    [50, "channel topic is: ヽ(`Д´)ノ"],
    [100, "users: [~" + foilName + "] [&nicked90] [@colons] [@EuricaeriS] [@okand] [+trenchfoot] [ you]"]  // XXX use actual name of our foil
  ];
  
  $.each(messages, function(i, thing) {
    ms += thing[0];
    setTimeout(function() {
      showMessage(templates.status({content: thing[1]}));
    }, ms);
  });

  setTimeout(bindPrompt, ms);
}

// XXX events must rebind the prompt manually
function getKicked() {
  showStatusMessage("kicked from " + channelName + " by " + foilName);
}

function foilQuit() {
  showStatusMessage(foilName + " has quit");
}

$(function() {
  $form = $('form#input');
  $prompt = $($form.find('#prompt'));
  $channelWindow = $('#channel ul');

  templates = {
    msg: templateFromId('msg'),
    status: templateFromId('status')
  };

  events = {
    kick: getKicked,
    leave: foilQuit
  };

  $(window).resize(scrollToBottom);

  connect();
});
