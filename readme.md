# Minimum Cost Network Flow Solver

This project implements a minimum cost network flow solver in Python using IBM CPLEX. It is intended for Computer Science and Engineering (CSE) students and professionals interested in optimization, operations research, and network flow algorithms.

---

## Problem Statement
Given a directed network with node balances (supplies/demands) and edge costs, determine the flow on each edge that satisfies all node balances and minimizes the total cost.

---

## Mathematical Formulation
The problem is modeled as a linear program:

Minimize:  
![minimize](https://latex.codecogs.com/svg.image?\sum_{(i,j)\in%20E}c_{ij}x_{ij})

Subject to:  
![constraint1](https://latex.codecogs.com/svg.image?\sum_{j:(j,i)\in%20E}x_{ji}-\sum_{j:(i,j)\in%20E}x_{ij}=-b_i\quad\forall%20i\in%20N)  
![constraint2](https://latex.codecogs.com/svg.image?x_{ij}\geq0\quad\forall(i,j)\in%20E)

---

## Installation

1. **Python**: Install from [python.org](https://www.python.org/downloads/) if not already available.
2. **IBM CPLEX**: Download and install IBM CPLEX Optimization Studio (academic version available for students).
3. **CPLEX Python API**: Install via pip:
   ```sh
   pip install cplex
   ```
   If you encounter permissions issues:
   ```sh
   pip install --user cplex
   ```

---

## Usage

1. Place `app.py` in your working directory.
2. Edit the network definition in `app.py` as needed (node balances, edges, costs).
3. Run the solver:
   ```sh
   python app.py
   ```
4. The program outputs the solution status, total minimum cost, and the flow on each edge.

---

## Example Output
```
Solution Status: Optimal
Total Minimum Cost: 840.0

Flow Assignment:
  1  4 : 40.0 units (cost/unit: 2, total: 80.0)
  3  7 : 30.0 units (cost/unit: 7, total: 210.0)
  4  5 : 50.0 units (cost/unit: 6, total: 300.0)
  5  3 : 50.0 units (cost/unit: 5, total: 250.0)
```

---

## Code Structure
- `NetworkFlow` class: Encapsulates the network, edge list, node balances, and CPLEX model construction/solution.
- `Solution` class: Stores the solution status, total cost, and edge flows.
- Main block: Defines a sample network, solves it, and prints results.

---

## Customization
- To solve a different instance, modify the node balances and edge list in `app.py`.
- The code can be extended to support edge capacities, integer flows, or other constraints as needed.

---

## References
- IBM CPLEX Documentation: https://www.ibm.com/docs/en/icos
- Network Flow Theory: Ahuja, Magnanti, Orlin, "Network Flows: Theory, Algorithms, and Applications"
