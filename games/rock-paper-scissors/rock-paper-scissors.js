const humanScoreTracker = document.querySelector("#Your-Score");
const computerScoreTracker = document.querySelector("#Computer-Score");
const finalResult = document.querySelector("#Final-Result");
const result = document.querySelector("#Result");
const buttons = document.querySelectorAll("#Choice-Buttons button");

let humanScore = 0;
let computerScore = 0;

function setResult(text, state) {
  const hasText = text && text.trim().length > 0;
  result.textContent = hasText ? text : "";
  if (hasText) {
    result.dataset.state = "filled";
    result.removeAttribute("aria-label");
  } else {
    result.dataset.state = "empty";
    result.setAttribute("aria-label", "Make your choice");
  }
  result.classList.toggle("win", state === "win");
  result.classList.toggle("lose", state === "lose");
}

buttons.forEach((button) => {
  button.addEventListener("click", () => {
    if (humanScore < 5 && computerScore < 5) {
      const computerSelection = getComputerChoice();
      const humanSelection = button.id;
      const roundResult = playRound(humanSelection, computerSelection);
      const scoreAdjustment = changeScore(roundResult, humanSelection, computerSelection);

      if (scoreAdjustment === "win") {
        humanScore += 1;
      } else if (scoreAdjustment === "lose") {
        computerScore += 1;
      }

      setResult(roundResult, scoreAdjustment);
      humanScoreTracker.textContent = "Your Score: " + humanScore;
      computerScoreTracker.textContent = "Computer Score: " + computerScore;
    }

    if (humanScore === 5) {
      finalResult.textContent = "You Win! Congratulations!";
      setResult("You Win! 🎉", "win");
    } else if (computerScore === 5) {
      finalResult.textContent = "You Lose! Bummer...";
      setResult("You Lose! 💥", "lose");
    }

    if ((humanScore === 5 || computerScore === 5) && !document.querySelector(".Restart")) {
      restart();
    }
  });
});

function restart() {
  const restartBtn = document.createElement("button");
  const container = document.querySelector("#Result-Section");
  restartBtn.classList.add("Restart");
  restartBtn.textContent = "Restart";
  container.appendChild(restartBtn);

  restartBtn.addEventListener("click", () => {
    humanScore = 0;
    computerScore = 0;
    humanScoreTracker.textContent = "";
    computerScoreTracker.textContent = "";
    finalResult.textContent = "";
    setResult("");
    restartBtn.remove();
  });
}

function getComputerChoice() {
  const n = Math.floor(Math.random() * 3);
  return n === 0 ? "Rock" : n === 1 ? "Paper" : "Scissors";
}

function playRound(humanSelection, computerSelection) {
  if (
    (humanSelection === "Rock" && computerSelection === "Scissors") ||
    (humanSelection === "Paper" && computerSelection === "Rock") ||
    (humanSelection === "Scissors" && computerSelection === "Paper")
  ) {
    return `You win! ${humanSelection} beats ${computerSelection}.`;
  } else if (
    (humanSelection === "Rock" && computerSelection === "Paper") ||
    (humanSelection === "Paper" && computerSelection === "Scissors") ||
    (humanSelection === "Scissors" && computerSelection === "Rock")
  ) {
    return `You lose! ${computerSelection} beats ${humanSelection}.`;
  } else if (humanSelection === "Undefined") {
    return "Please choose an option.";
  } else if (humanSelection === computerSelection) {
    return `You both chose ${humanSelection}. Try Again!`;
  } else {
    return "Your choice is invalid. Try again.";
  }
}

function changeScore(roundResult, humanSelection, computerSelection) {
  if (roundResult === `You win! ${humanSelection} beats ${computerSelection}.`) {
    return "win";
  } else if (roundResult === `You lose! ${computerSelection} beats ${humanSelection}.`) {
    return "lose";
  } else {
    return "no change";
  }
}