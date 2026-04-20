// mines.js
const numRows = 8;
const numCols = 8;
const numMines = 10;

const minefield =
    document.getElementById(
        "minefield"
    );
let board = [];
let cellMines = [];
let gameOver = false;
let victory = false;
let tilesToReveal = numRows * numCols - numMines;

function initializeBoard() {
    for (let i = 0; i < numRows; i++) {
        board[i] = [];
        for ( let j = 0; j < numCols; j++ ) {
            board[i][j] = {
                isMine: false,
                revealed: false,
                flagged: false,
                count: 0,
            };
        }
    }
    gameOver = false;
    victory = false;

    // Place mines randomly
    let minesPlaced = 0;
    while (minesPlaced < numMines) {
        const row = Math.floor(Math.random() * numRows);
        const col = Math.floor(Math.random() * numCols);
        const cell = document.createElement( "div" );
        
        if (!board[row][col].isMine) {
            board[row][col].isMine = true;
            minesPlaced++;
            cellMines.push(board[row][col]);
        }
    }

    // Calculate counts
    for (let i = 0; i < numRows; i++) {
        for ( let j = 0; j < numCols; j++ ) {
            if (!board[i][j].isMine) {
                let count = 0;
                for ( let dx = -1; dx <= 1; dx++ ) {
                    for ( let dy = -1; dy <= 1; dy++ ) {
                        const ni = i + dx;
                        const nj = j + dy;
                        if ( ni >= 0 && ni < numRows && nj >= 0 && nj < numCols && board[ni][nj].isMine ) {
                            count++;
                        }
                    }
                }
                board[i][j].count = count;
            }
        }
    }
}

function revealCell(row, col) {
    if ( row < 0 || row >= numRows || col < 0 || col >= numCols || board[row][col].revealed || board[row][col].flagged) {
        return;
    }

    board[row][col].revealed = true;
    
    console.log(tilesToReveal)
    if (board[row][col].isMine) {
        // Handle game over
        alert("Game Over! You stepped on a mine.");
        gameOver = true;
       

    } else if (tilesToReveal == 0) {
        alert("Congrats, you've won!")
        victory = true;
        gameOver = true;
    } else if ( board[row][col].count === 0 ) {
        // If cell has no mines nearby,
        // Reveal adjacent cells
        for ( let dx = -1; dx <= 1; dx++ ) {
            for ( let dy = -1; dy <= 1; dy++ ) {
                revealCell( row + dx, col + dy );
            }
        }
    }
    tilesToReveal--;
    renderBoard();
}

function toggleCell(row, col) {
    if ( row < 0 || row >= numRows || col < 0 || col >= numCols || board[row][col].revealed ) {
        return;
    }
    if (gameOver) {
        return;
    }
    board[row][col].flagged = !board[row][col].flagged;
    renderBoard();
}

function renderBoard() {
    minefield.innerHTML = "";
  
    for (let i = 0; i < numRows; i++) {
        for ( let j = 0; j < numCols; j++ ) {
            const cell = document.createElement( "div" );
            cell.className = "cell";
            if (board[i][j].flagged) {
                cell.classList.add("flagged");
                cell.textContent = "\u{1F6A9}";
            } else {
                if (cell.classList.contains("flagged")) {
                    cell.classList.remove("flagged");
                    cell.textContent = "";
                }
            }
            if ( board[i][j].revealed ) {
                cell.classList.add("revealed");

                if ( board[i][j].isMine ) { // the game over, you clicked a mine
                    cell.classList.add( "mine" );
                    cell.textContent = "\u{1F4A3}";
                    victory = false;
                    //gameOver = true;

                } else if ( board[i][j].count > 0 ) {
                    cell.textContent = board[i][j].count;
                }
            }
            if (!gameOver) {
                cell.addEventListener("click", () => {
                    if (gameOver) return;
                    revealCell(i, j)
                });
                cell.addEventListener("contextmenu", (event) => {
                    if (gameOver) return;
                    event.preventDefault();
                    toggleCell(i, j);
                });
            }
            if (victory) {
                cell.removeEventListener("click", () => revealCell(i, j))
            }
            minefield.appendChild(cell);   
        }
        minefield.appendChild(
            document.createElement("br")
        );
    }
    
    if (tilesToReveal == 0) {
        victory = true;
        gameOver = true;
        
        alert("congratulations, you won!");
    }
    if (gameOver) {
        endGame(victory);
    }
}

function getCSRFToken() {
    return document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        .split("=")[1];
}

function endGame(viko) {
    //alert("endgame test");
    fetch("/save-mines-result/", { method: "POST", headers: {"Content-Type": "application/json", "X-CSRFToken": getCSRFToken()},
    body: JSON.stringify({victory: viko}) } ).then(response => response.json()).then(data => console.log(data));
    //alert("TEST")
}

initializeBoard();
renderBoard();