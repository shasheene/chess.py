#### chess.py
chess.py is small, text-based chess game

#### Requirements
Currently, [python2](http://www.python.org/getit/) is the only dependancy, so the game *should* also run on Windows and MacOS X.

Chess pieces are represented with the standard [unicode characters](http://en.wikipedia.org/wiki/Chess_symbols_in_Unicode)

In the future I will add a graphical user interface (likely using the 'pygame' library)

(The game is currently completely terminal/command-line based. At the moment, the player selects pieces by typing the coordinates (eg. 'e2' followed by 'e4' to play the famous opening "King's Pawn" opening move).)

#### Features
Currently, only the chess piece movement/attack mechanics are complete:
- [x] Pawn
- [x] Rook
- [x] Knight
- [x] Bishop
- [] King (no castling yet)
- [x] Queen
- [] Main game logic (turn-based game with check/checkmate detection)
- [] Graphical user interface with move selection through mouse clicks (and highlighting legal moves of selected piece)
- [] Computer player with AI

## Screenshots

![Unicode characters are pretty cool](https://dl.dropboxusercontent.com/u/6634730/github/chess/chesspyTerminalScreenshot.png "chess.py screenshot")
