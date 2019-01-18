#### chess.py
chess.py is small, text-based chess game implementing all known rules of chess (including the oft-forgotten "[en passant](https://en.wikipedia.org/wiki/En_passant)" special capture rule :-) 

![Unicode characters are pretty cool](docs/images/chesspyTerminalScreenshot.png "chess.py screenshot")

### Requirements
Currently, [python3](http://www.python.org/getit/) is the only dependency, so the game *should* also run on Windows and MacOS X.

Chess pieces are represented with the standard [unicode characters](http://en.wikipedia.org/wiki/Chess_symbols_in_Unicode)

In the future I will add a graphical user interface (likely using the 'pygame' library)

(The game is currently completely terminal/command-line based. At the moment, the player selects pieces by typing the coordinates (eg. 'e2' followed by 'e4' to play the famous "[King's Pawn](https://en.wikipedia.org/wiki/King%27s_Pawn_Game)" opening move).)

#### Completed Features
Core gameplay is complete, with all known chess mechanics implemented:
- [x] Pawn
  - [x] Promotion
  - [x] [En passant](https://en.wikipedia.org/wiki/En_passant) special capture
- [x] Knight
- [x] Bishop
- [x] King
  - [x] King/Rook Castling
- [x] Rook
- [x] Queen
- [x] Main game logic: Turn-based basic playable game mechanics
- [x] Check/checkmate detection
- Draw detection
    - [x] [Stalemate](https://en.wikipedia.org/wiki/Stalemate)
    - [x] Impossibility of checkmate ("insufficient mating material rule")
    - [x] [3-fold repetition](https://en.wikipedia.org/wiki/Threefold_repetition)
    - [x] [50-move rule](https://en.wikipedia.org/wiki/Fifty-move_rule)

#### History

chess.py was written during freetime between December 2013 and January 2014, but was abandoned near-completion of terminal-based gameplay. After a 4 year hiatus, development was resumed with the left-over gameplay mechanics (described above) being quickly implemented.

#### Roadmap

With the terminal-based chess game fully completed, it serves as a building block for future projects:

- [] Refactor terminal application into client/server architecture
  - [] Communication of each player via JSON messages send over TCP sockets
    - Needs session IDs, opponent connection status etc
    - Confirm validity of JSON messages
- [] Create a [TypeScript 'chess.ts' client](https://github.com/shasheene/chess.ts)
- [] Host chess.py on a persistent cloud server, with chess.ts as the frontend
- [] Computer player AI bot
- [] Graphical user interface (in python) with move selection through mouse clicks
- [] Create Android client (with the Flutter UI framework) and publish on app store


