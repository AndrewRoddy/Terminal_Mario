# Terminal Mario

A platformer game that runs entirely in the terminal, built with Python. It features goombas, coin blocks, score, and a flag at the end.

```
  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
|                                                            |
|                                                            |
|                                                            |
|                                            ?               |
|                                                            |
|                                                            |
|                                                            |
|                                ?       # ? # ? #           |
|                                                            |
|                                                        [ ] |
|        m                                           g   | | |
|# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # |
|# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # |
Score: 3500
```

## How to Run

1. Install the required library:
   ```
   pip install pynput==1.8.1
   ```
2. Run the game:
   ```
   python platformer.py
   ```

## Controls

| Key                   | Action     |
|-----------------------|------------|
| D or Right Arrow      | Move right |
| A or Left Arrow       | Move left  |
| Space, W, or Up Arrow | Jump       |

## How the Game Works

The level is stored in `maps/1-1.csv` as a grid with 13 rows and around 200 columns. Each cell holds a single character that represents a tile:

| Symbol       | What It Is               |
|--------------|--------------------------|
| `m`          | Mario                    |
| `g`          | Goomba                   |
| `#`          | Solid block              |
| `?`          | Question block           |
| `$`          | Flag                     |
| `[ ]`        | Pipe                     |


## By me \:)
Not affiliated with Nintendo