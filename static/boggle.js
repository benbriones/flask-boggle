"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  const response = await fetch(`/api/new-game`, {
    method: "POST",
  });
  const gameData = await response.json();

  gameId = gameData.gameId;
  let board = gameData.board;

  displayBoard(board);
}

/** Display board */

/**Fills board with random letters */
function displayBoard(board) {
  $table.empty();

  const $tBody = $('<tbody>');

  for (let row of board) {
    let $row = $('<tr>');
    for (let cell of row) {
      let $cell = $(`<td>${cell}</td>`);
      $row.append($cell);
    }
    $tBody.append($row);
  }
  $table.append($tBody);
}


/**Tests if submitted word is valid and on board, if it is it appends word to
 * top left list, if not it shows a message in top right */
async function handleFormSubmit(evt) {

  evt.preventDefault()
  const word = $wordInput.val();
  console.log("word is =", word);

  const response = await fetch("/api/score-word", {
    method: "POST",
    body: JSON.stringify({"gameId": gameId,"word": word}),
    headers: {"content-type": "application/json"}
  });

  const data = await response.json();
  handleWord(word, data.result)
}

/**Takes a word and message, if word is valid it appends to top right, if not
 * message is displayed in top left */
function handleWord(word, msg) {
  if (msg === "ok") {
    $playedWords.append(`<li> ${word} </li>`);
    $message.html("");
  } else {
    $message.html(msg);
  }
}

$form.on('submit', handleFormSubmit);

start();