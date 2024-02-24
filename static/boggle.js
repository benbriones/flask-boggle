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
  console.log("data", data)
  console.log("data.result=", data.result)
  // $message.html(data.result);
}

$form.on('submit', handleFormSubmit);

start();