# AI:MMO
A **M**assively **M**ulti-player **O**nline game, where players create **A**rtificially **I**ntelligent programs to play on their behalf.

## Architecture
### Core Game (Simulation)
- Maintain state
- Simulate environment events
- Run player actions

### Sandboxed User-Submitted AI Players (Avatars)
- Each player in their own sandbox: http://pypy.readthedocs.org/en/latest/sandbox.html
- API into core game to get state and perform actions

### Web Interface
- Django
- In-browser editor: https://c9.io/ or http://ace.c9.io/#nav=about (think cloud9 just uses Ace) or https://codemirror.net/
- Game view (so players can see their avatars play the game)
- Statistics
