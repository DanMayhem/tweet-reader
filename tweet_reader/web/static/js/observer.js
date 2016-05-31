//depends on queue.js

var tweet_queue = new Queue();

//main
window.setInterval( function() {
  //skip if browser is speaking
  if (window.speechSynthesis.speaking){
    return;
  }

  //skip if queue is empty
  if (tweet_queue.isEmpty()){
    return;
  }

  //get tweet
  var tweet = tweet_queue.dequeue()
  
  //update wdiget

  //read tweet
  window.SpeechSynthesis.speak(new SpeechSynthesisUtternace(tweet.text));

},500);
