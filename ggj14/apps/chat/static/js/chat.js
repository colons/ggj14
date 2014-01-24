var templates;
var $channelWindow;

function templateFromId(id) {
  var source = $(document.getElementById(id)).html();
  return Handlebars.compile(source);
}

$(function() {
  "use strict";

  templates = {
    msg: templateFromId('msg')
  };

  $channelWindow = $('#channel ul');

  var context = {
    origin: 'client',
    content: 'what',
    nick: 'you'
  };

  console.log(context);
  console.log(templates.msg(context));
  $channelWindow.append(templates.msg(context));
});
