var events;
var templates;
var nick;

var $channelWindow;
var $queryWindow;
var $form;
var $prompt;

function templateFromId(id) {
  var source = $(document.getElementById(id)).html();
  return Handlebars.compile(source);
}

function scrollToBottom() {
  window.scroll(0, document.body.scrollHeight);
}

function showMessage($target, html) {
  $target.find('ul').append(html);
  scrollToBottom();
}

function showStatusMessage(content, element) {
  if (element === undefined) {
    element = $('.window.active');
  }
  showMessage(element, templates.status({content: content}));
}

function showMessages(messages, doNotRebindPrompt) {
  var longestFoilDelay = 0;
  var hasEvent = false;

  $(messages).each(function(i, message) {

    // we don't want to automatically show the prompt if there's a
    // scripted event attached to this exchange, so we will make a note
    // of if this is one or not

    if (message.event) { hasEvent = true; }
    var $target = $(document.getElementById(message.target));

    setTimeout(function() {
      if (message.event) {
        events[message.event]();
      } else {
        showMessage($target, templates[message.type](message));
      }
    }, message.delay);

    if (message.isFoil && message.delay > longestFoilDelay) {
      longestFoilDelay = message.delay;
    }
  });

  if ((!hasEvent) && (!doNotRebindPrompt)) {
    setTimeout(bindPrompt, longestFoilDelay);
  }
}

function sendMessage(clientMessage) {
  showMessage($('section.window.active'), templates.msg({
    origin: 'client',
    nick: nick,
    content: clientMessage
  }));

  $.ajax({
    type: 'POST',
    url: postMessageURL,
    data: {message: clientMessage},
    success: function(dataString) {
      var data = $.parseJSON(dataString);
      showMessages(data.messages);
      showMessages(data.parallelMessages, true);
    },
    error: function() {
      showStatusMessage('error sending message to server, please try again...');
      bindPrompt();
    }
  });
}

function bindTabs() {
  $tabs = $('#tabs li');
  $tabs.click(function(e) {
    $this = $(this);
    $tabs.removeClass('active');
    $('.window').removeClass('active');
    $window = $(document.getElementById($this.attr('data-target')));
    $window.addClass('active');

    if ($window.hasClass('enabled')) {
      bindPrompt();
    } else {
      unbindPrompt();
    }

    $this.addClass('active');
    scrollToBottom();
    $prompt.focus();
  });
}

function bindPrompt(func) {
  $form.off('submit');
  $form.submit(function(e) {
    e.preventDefault();
    var clientMessage = $prompt.val();
    if (clientMessage === '') {
      return;
    }

    $prompt.val('');
    unbindPrompt();

    if (func === undefined) {
      sendMessage(clientMessage);
    } else {
      func(clientMessage);
    }
  });
  $form.slideDown();
  $prompt.focus();
}

function unbindPrompt() {
  $form.off('submit');
  $form.submit(function(e) {
    e.preventDefault();
  });

  $form.slideUp();
}

function login() {
  showStatusMessage('enter a nickname');
  bindPrompt(function(input) {
    nick = input;

    $.ajax({
      type: 'POST',
      url: setNickURL,
      data: {nick: nick},
      success: connect,
      error: function() {
        showStatusMessage('come now, be reasonable');
        login();
      }
    });
  });
}

function connect() {
  var ms = 0;
  var messages = [
    [0, 'connecting to irc.biz.ru:6697 as ' + nick + '...'],
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
    [100, "users: [~" + foilName + "] [&NickEd90] [@colons] [@EuricaeriS] [@okänd] [+trenchfoot] [ " + nick + "]"]  // XXX use actual name of our foil
  ];
  
  $.each(messages, function(i, thing) {
    ms += thing[0];
    setTimeout(function() {
      showStatusMessage(thing[1]);
    }, ms);
  });

  setTimeout(bindPrompt, ms);
}

// XXX events must rebind the prompt manually
function getKicked() {
  showStatusMessage("kicked from " + channelName + " by " + foilName);
  $('section.enabled').removeClass('enabled');
}

function foilQuit() {
  showStatusMessage(foilName + " has quit");
  $('section.enabled').removeClass('enabled');
}

function startPartTwo() {
  $('#tabs').slideDown();
  $('section.window').removeClass('enabled');
  $('#tabs li[data-target=query]').click();
  $('section.window#query').addClass('enabled');
  bindPrompt();
}

function postPenis() {
  var ms = 5000;
  var delta = 3000;

  $.each([
    "",
    "                            -    .|||||.",
    "                                |||||||||",
    "                        -      ||||||  .",
    "                            -  ||||||   >",
    "                              ||||||| -/",
    "                         --   ||||||'(",
    "                      -       .'      \\",
    "                           .-'    | | |",
    "                          /        \\ \\ \\",
    "            --        -  |      `---:.`.\\",
    "           ____________._>           \\\\_\\\\____ ,--.__    ",
    "--    ,--\"\"           /    `-   .     |)_)    '\\     '\\  ",
    "     /  \"             |      .-'     /          \\      '\\",
    "   ,/                  \\           .'            '\\     |",
    "   | \"   \"   \"          \\         /                '\\,  /",
    "   |           \" , =_____`-.   .-'_________________,--\"\" ",
    " - |  \"    \"    /\"/'      /\\>-' ( <",
    "   \\  \"      \",/ /    -  ( <    |\\_)",
    "    \\   \",\",_/,-'        |\\_)",
    " -- -'-;.__:-'",
    ""
  ], function(i, line) {
    setTimeout(function() {
      var videoMessage = {
        content: line,
        type: 'msg',
        nick: foilName,
        origin: 'server foil'
      };
      showMessage($queryWindow, templates[videoMessage.type](videoMessage));
    }, ms);
    ms += delta;
    delta = delta * 0.8;
  });

  setTimeout(foilQuit, ms);
}

$(function() {
  $form = $('form#input');
  $prompt = $($form.find('#prompt'));
  $channelWindow = $('#channel');
  $queryWindow = $('#query');

  templates = {
    msg: templateFromId('msg'),
    status: templateFromId('status')
  };

  events = {
    kick: getKicked,
    leave: foilQuit,
    part2: startPartTwo,
    troll: postPenis
  };

  $(window).resize(scrollToBottom);
  bindTabs();
  showStatusMessage('Receiving query on irc.biz.ru:6697 from ' + foilName, $queryWindow);

  login();
});
