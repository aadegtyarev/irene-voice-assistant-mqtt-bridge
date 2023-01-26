trackMqtt("irine-voice-assistant/command", function(message){
  msg = JSON.parse(message.value)
  log.info("device: {} | action: {}".format(msg['device'], msg['action']))

   publish("irine-voice-assistant/say", JSON.stringify({ phrase: "Готово" }), 2, false);
});
