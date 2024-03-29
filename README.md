# EternityII
<div align="center">
<img src="images/eternity_white.png" alt="" title="", width="800">
</div>

<br>

This is the solver of pseudo EternityII. The comments in the codes are written in Japanese.

# Description
In this system, we considered EternityII as simpler one, and call it "Pseudo EternityII". Originally, EternityII is a puzzle competition which was released on 28 July 2007. Tow million dollars are put on the puzzle, but no one can solve the puzzle. EternityII puzzle is an "edge-matching puzzle" which includes 256 square puzzle pieces and places them into a 16 by 16 grid. Then players must match adjacent edges. This puzzle is too difficult and time-consuming to solve with a laptop. Therefore, I introduced the easier version named Pseudo EternityII. The requirements of Pseudo EternityII are listed below.

<br>

- The grid size is controllable.
- The kinds of inner colors are controllable.
- The pieces cannot be rotated.
- The middle piece is placed from the beginning.

<br>

In addition, to make the puzzle simpler, the grid size is set as an odd number. This is because if the grid size is an odd number, the middle piece is defined uniquely.

<br>

The main contents are divided into two types. 

<br>

1. Drawing EternityII
2. Solving EternityII 

<br>

To our knowledge, we have tried to visualize EternityII for the first time. Drawing EternityII, we can tackle the puzzle from visualizetion and catch the missed pieces qualitatively.

<br>

# Usage
## Drawing
```
$ python drawing.py [the number of the girds side] [the number of colors]
```

<br>

Arguments:  
1. The number of grids side. If you choose 3, 9 pieces are created.
2. The number of colors you can use to the puzzle.

<br>

Return:
- An answer to the puzzle (answer.png)
- A shuffled puzzle (input.png)

<br>

Note:
- If you choose too many colors, the message like "Please set the different number of colors. Anyway, we'll make the puzzle using hogehoge colors." is appeared.

<br>

## Solving
```
$ python solver.py [the number of the girds side] [the number of colors]
```

<br>

Arguments:  
1. The number of grids side. If you choose 3, 9 pieces are created.
2. The number of colors you can use to the puzzle.

<br>

Return:
- Solved pieces of the puzzle through the solver (output.png)

<br>

Standard Output:
- An accuracy rate of the edges. 

<br>

Note:
- If you choose too many colors, the message like "Please set the different number of colors. Anyway, we'll make the puzzle using hogehoge colors." is appeared.
- This solver does not do backprop. Therefore, in some cases, the accuracy rate cannot reach 100%.
