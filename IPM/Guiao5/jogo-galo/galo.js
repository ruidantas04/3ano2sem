document.addEventListener("DOMContentLoaded", function () {
    const board = document.getElementById("game-board");
    const resetBtn = document.getElementById("reset-btn");
    const statusText = document.getElementById("game-status");

    let cells = ["", "", "", "", "", "", "", "", ""];
    let currentPlayer = "X";
    let gameActive = true;

    // Combinações vencedoras
    const winningConditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], 
        [0, 3, 6], [1, 4, 7], [2, 5, 8], 
        [0, 4, 8], [2, 4, 6]             
    ];

    // Cria o tabuleiro
    function createBoard() {
        board.innerHTML = ""; // Limpa o tabuleiro
        cells.forEach((cell, index) => {
            const cellDiv = document.createElement("div");
            cellDiv.classList.add("cell");
            cellDiv.dataset.index = index;
            cellDiv.textContent = cell;
            cellDiv.addEventListener("click", handleCellClick);
            board.appendChild(cellDiv);
        });
        statusText.textContent = `Vez do jogador: ${currentPlayer}`;
        statusText.style.color = "black"; 
    }

    function handleCellClick(event) {
        const index = event.target.dataset.index;

        if (cells[index] !== "" ) {
            alert("Célula já preenchida!");
            return;
        }
        if (!gameActive){
           alert("Jogo Terminado!Reinicie o Jogo!");
           return;
        }

        cells[index] = currentPlayer;
        event.target.textContent = currentPlayer;

        checkWinner();
        if (gameActive) {
            togglePlayer();
        }
    }

    // Alterna entre X e O
    function togglePlayer() {
        currentPlayer = currentPlayer === "X" ? "O" : "X";
        statusText.textContent = `Vez do jogador: ${currentPlayer}`;
    }

    // Verifica se há um vencedor
    function checkWinner() {
        let roundWon = false;

        for (let condition of winningConditions) {
            let [a, b, c] = condition;
            if (cells[a] && cells[a] === cells[b] && cells[a] === cells[c]) {
                roundWon = true;
                break;
            }
        }

        if (roundWon) {
            statusText.textContent = `🏆 Jogo Terminado! Jogador ${currentPlayer} venceu! 🎉`;
            statusText.style.color = "green";
            gameActive = false;
            return;
        }

        if (!cells.includes("")) {
            statusText.textContent = "⚖️ Jogo Terminado! Empate!";
            statusText.style.color = "orange";
            gameActive = false;
            return;
        }
    }
    function resetGame() {
        cells = ["", "", "", "", "", "", "", "", ""];
        currentPlayer = "X";
        gameActive = true;
        createBoard();
        statusText.textContent = "Novo Jogo! Vez do jogador: X";
        statusText.style.color = "black";
    }

    resetBtn.addEventListener("click", resetGame);

    createBoard();
});
