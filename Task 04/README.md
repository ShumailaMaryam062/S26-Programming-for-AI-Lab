# Task 04: N-Queens Problem Solver

## Overview
This task implements the **N-Queens Problem** solver with dynamic `n` value. It finds all possible solutions to place `n` queens on an `n×n` chessboard such that no two queens attack each other.

## Problem Statement
Place `n` queens on an `n×n` chessboard such that:
- No two queens are in the same row
- No two queens are in the same column
- No two queens attack each other diagonally

## Solution Approach
- **Algorithm:** Backtracking with constraint satisfaction
- **Time Complexity:** O(n!) in the worst case
- **Space Complexity:** O(n) for the solution board

## Features
- **Dynamic n:** Solve the N-Queens problem for any board size
- **Multiple Solutions:** Finds all possible configurations
- **Board Display:** Visual representation of queen placements using the 'Q' character

## Files
- `NQueen.ipynb` - Jupyter notebook containing the complete solution

## Algorithm Details
### Backtracking Process
1. Place queens row by row, starting from row 0
2. For each row, try placing a queen in each column
3. Check if the placement is safe (no conflicts with previously placed queens)
4. If safe, move to the next row
5. If unsafe, backtrack and try the next column
6. If all queens are placed successfully, store the solution
7. Backtrack to find other solutions

### Safety Check
For each position, check:
- **Row conflicts:** No queen in columns of previous rows
- **Diagonal conflicts:** No queen on upper-left and upper-right diagonals

## How to Run
1. Open `NQueen.ipynb` in Jupyter Notebook or JupyterLab
2. Run all cells to execute the solver
3. Modify the `n` variable to solve for different board sizes
4. View all solutions and their visual board representations

## Example
For n=4, the solver will find all 2 solutions where 4 queens can be placed on a 4×4 board without attacking each other.
