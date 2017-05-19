#### chess.py
chess.py is small, text-based chess game

#### History

chess.py was written during freetime between December 2013 and January 2014, but was abandoned near-completion of terminal-based gameplay. In May 2017 (4 years and 4 months later), development resumed.

#### Requirements
Currently, [python3](http://www.python.org/getit/) is the only dependancy, so the game *should* also run on Windows and MacOS X.

Chess pieces are represented with the standard [unicode characters](http://en.wikipedia.org/wiki/Chess_symbols_in_Unicode)

In the future I will add a graphical user interface (likely using the 'pygame' library)

(The game is currently completely terminal/command-line based. At the moment, the player selects pieces by typing the coordinates (eg. 'e2' followed by 'e4' to play the famous "King's Pawn" opening move).)

#### Features
Currently, only the chess piece movement/attack mechanics are complete:
- [x] Pawn
- [x] Rook
- [x] Knight
- [x] Bishop
- [x] King
- [x] Queen
- [] Advanced piece mechanics (Pawn promotion and King/Rook "castling")
- [x] Main game logic: Turn-based basic playable game mechanics
- [] Game ending logic: Check/checkmate detection
- [] Graphical user interface with move selection through mouse clicks (and highlighting legal moves of selected piece)
- [] Computer player with AI communicating to seperate server using JSON messages

## Screenshots

![Unicode characters are pretty cool](docs/images/chesspyTerminalScreenshot.png "chess.py screenshot")
