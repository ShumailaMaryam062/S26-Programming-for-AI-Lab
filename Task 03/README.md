# Task 03: Water Jug Problem

## Overview
This task implements the **Water Jug Problem** using Depth-First Search (DFS) algorithm. The goal is to find a sequence of operations to measure exactly 2 liters of water in one of the jugs.

## Problem Statement
Given two jugs with capacities:
- **Jug 1:** 4 liters
- **Jug 2:** 3 liters

Find a sequence of operations to measure exactly **2 liters** in one of the jugs.

## State Representation
Each state is represented as `(x, y)` where:
- `x` = amount of water in Jug 1 (capacity 4 liters)
- `y` = amount of water in Jug 2 (capacity 3 liters)

## Allowed Operations
1. **Fill Jug 1:** Fill jug 1 completely from the tap
2. **Fill Jug 2:** Fill jug 2 completely from the tap
3. **Empty Jug 1:** Pour out all water from jug 1
4. **Empty Jug 2:** Pour out all water from jug 2
5. **Pour Jug 1 → Jug 2:** Pour water from jug 1 to jug 2 until either jug 1 is empty or jug 2 is full
6. **Pour Jug 2 → Jug 1:** Pour water from jug 2 to jug 1 until either jug 2 is empty or jug 1 is full

## Files
- `Waterjug.ipynb` - Jupyter notebook containing the complete solution with step-by-step explanation

## Algorithm
- **Search Strategy:** Depth-First Search (DFS)
- **Initial State:** (0, 0) - both jugs are empty
- **Goal State:** Any state where x = 2 or y = 2

## Output
The program prints:
- Each state in the solution path
- The rule/operation applied at each step
- The final solution sequence

## How to Run
1. Open `Waterjug.ipynb` in Jupyter Notebook or JupyterLab
2. Run all cells to execute the solution
3. View the step-by-step operations and the final result
