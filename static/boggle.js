class BoggleGame {
    /* make a new game at this DOM id */
  
    constructor(secs = 60) {
  
        this.words = new Set();
  
        // Initializing the score to be 0
        this.score = 0;

        // Setting the TIMER for the game

        this.secs = secs; // game length
        this.showTimer();
        // every 1 sec, we decrement the timer by 1 which is done in function "tick()"
        this.timer = setInterval(this.tick.bind(this), 1000);

        // we use bind(this) as we bind the "this keyword" to this class "BoggleGame"
        $(".add-word").on("submit", this.handleSubmit.bind(this));
    }
  
    /* show word in list of words class */
  
    showWord(word) {
      $(".words").append($("<li>", { text: word }));
    }
  
    /* show a status message */

    showMessage(msg, cls) {
        $(".msg")
        .text(msg)
        .removeClass()
        .addClass(`msg ${cls}`);
    }

    /* show score in html */

    showScore() {
        $(".score").text(this.score);
    }
    
    /* handle submission of word: if unique and valid, score & show */
  
    async handleSubmit(e) {
        e.preventDefault();
        
        // Getting the word user entered from the form
        let word = $(".word").val();
        console.log(word)

        if (!word) return;
    
        if (this.words.has(word)) {
            this.showMessage(`Already found ${word}`, "err");
            return;
        }
    
        // check server for validity
        // Sending a GET REQUEST to "/check-word" ROUTE to "app.py" and pass in the "word" got from the FORM entered by user as params, so that we can retrive it in app.py using "request.args"
        const res = await axios.get("/check-word", { params: { word: word }});
        if (res.data.result === "not-word") {
            this.showMessage(`${word} is not a valid English word`, "err");
        } else if (res.data.result === "not-on-board") {
            this.showMessage(`${word} is not a valid word on this board`, "err");
        } else {
            this.showWord(word);

            // If valid word then its added to the set "words", so that we can keep track whether the word was reentered or not
            this.words.add(word);

            // Now storing the score to the length of the valid word user created each time if the "word" is VALID and calling the function "showScore()" to display score on the DOM

            this.score += word.length;
            this.showScore();


            this.showMessage(`Added: ${word}`, "ok");
        }
    
        $(".word").val("");
    }
  
    /* Update timer in DOM */
  
    showTimer() {
        $(".timer").text(this.secs);
    }
  
    /* Tick: handle a second passing in game */
  
    async tick() {
        this.secs -= 1;
        this.showTimer();
    
        if (this.secs === 0) {
            clearInterval(this.timer);
            await this.scoreGame();
        }
    }
  
    /* end of game: score and update message. */
  
    async scoreGame() {

        $(".add-word").hide();

        // Sending a POST Request to "/post-score" route in "app.py" when the game timer ends
        const resp = await axios.post("/post-score", { score: this.score });
        if (resp.data.brokeRecord) {
            this.showMessage(`New record: ${this.score}`, "ok");
        } else {
            this.showMessage(`Final score: ${this.score}`, "ok");
        }
    }
  }