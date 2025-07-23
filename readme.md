# Minimum Cost Network Flow Solver

This project implements a minimum cost network flow solver in Python using IBM CPLEX. 

---

Objective:
    Find the flow on each edge of a directed network that meets all supply and demand requirements at each node, while minimizing the total cost.

Optimization Problem:

Goal:
    Minimize the total cost of flow:
        Add up (cost per unit × flow) for every edge in the network.

    For every edge from node i to node j (written as (i, j) in E):
        Total Cost = c_ij × x_ij
        where:
            • c_ij = cost per unit flow on edge (i, j)
            • x_ij = amount of flow on edge (i, j)

Subject to the following constraints:

1. Flow Conservation at Each Node:
    For every node i in the network:
        (Total incoming flow) – (Total outgoing flow) = –b_i

    - If b_i is positive, node i is a supply node (it provides flow).
    - If b_i is negative, node i is a demand node (it requires flow).

2. Non-Negative Flow on Edges:
    The flow on every edge must be zero or positive (no negative flows).

Definitions:
    x_ij: Flow on edge from node i to node j
    c_ij: Cost per unit flow on edge (i, j)
    b_i: Net supply/demand at node i (positive for supply, negative for demand)

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

## Output of the given problem
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
