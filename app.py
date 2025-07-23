import cplex
from collections import namedtuple, defaultdict

class Edge:
    def __init__(self, from_node, to_node, cost):
        self.from_node = from_node
        self.to_node = to_node
        self.cost = cost

class Solution:
    def __init__(self):
        self.solved = False
        self.total_cost = None
        self.status = None
        self.flows = dict()  

class NetworkFlow:
    def __init__(self, n):
        self.num_nodes = n
        self.balances = [0.0] * n  
        self.edges = []

    def set_balance(self, node, b):
        if node < 1 or node > self.num_nodes:
            raise IndexError(f"Node out of range: {node}")
        self.balances[node - 1] = b

    def add_edge(self, from_node, to_node, cost):
        if from_node < 1 or from_node > self.num_nodes or to_node < 1 or to_node > self.num_nodes:
            raise IndexError(f"Invalid node in edge: {from_node}->{to_node}")
        self.edges.append(Edge(from_node, to_node, cost))

    def get_num_nodes(self):
        return self.num_nodes

    def get_balance(self, node):
        if node < 1 or node > self.num_nodes:
            return 0.0
        return self.balances[node - 1]

    def get_edges(self):
        return self.edges

    def is_balanced(self):
        return abs(sum(self.balances)) < 1e-5

    def validate(self):
        if not self.is_balanced():
            return "Supply and demand are not balanced."
        for e in self.edges:
            if e.from_node < 1 or e.from_node > self.num_nodes or e.to_node < 1 or e.to_node > self.num_nodes:
                return f"Invalid edge: {e.from_node}->{e.to_node}"
        return "valid"

    def solve(self):
        sol = Solution()
        try:
            cpx = cplex.Cplex()
            cpx.set_log_stream(None)
            cpx.set_error_stream(None)
            cpx.set_warning_stream(None)
            cpx.set_results_stream(None)
            # Variables: one per edge
            edge_vars = []
            var_names = []
            costs = []
            for idx, e in enumerate(self.edges):
                name = f"x_{e.from_node}_{e.to_node}"
                var_names.append(name)
                costs.append(e.cost)
                edge_vars.append((e.from_node, e.to_node))
            cpx.variables.add(obj=costs, lb=[0.0]*len(costs), names=var_names)
            # Constraints: flow conservation for each node
            for node in range(1, self.num_nodes+1):
                row = [[], []]  # indices, coefficients
                for idx, (from_n, to_n) in enumerate(edge_vars):
                    if to_n == node:
                        row[0].append(idx)
                        row[1].append(1.0)
                    if from_n == node:
                        row[0].append(idx)
                        row[1].append(-1.0)
                rhs = -self.get_balance(node)
                cpx.linear_constraints.add(
                    lin_expr=[cplex.SparsePair(ind=row[0], val=row[1])],
                    senses=["E"],
                    rhs=[rhs],
                    names=[f"node_{node}_balance"]
                )
            cpx.objective.set_sense(cpx.objective.sense.minimize)
            cpx.parameters.lpmethod.set(cpx.parameters.lpmethod.values.primal)
            cpx.solve()
            status = cpx.solution.get_status()
            if status in [cpx.solution.status.optimal, cpx.solution.status.optimal_tolerance]:
                sol.solved = True
                sol.total_cost = cpx.solution.get_objective_value()
                sol.status = "Optimal"
                x = cpx.solution.get_values()
                for idx, val in enumerate(x):
                    if val > 1e-6:
                        sol.flows[edge_vars[idx]] = val
            else:
                sol.status = cpx.solution.get_status_string()
        except Exception as ex:
            sol.status = f"Exception: {ex}"
        return sol

if __name__ == "__main__":
    net = NetworkFlow(7)
    # Set balances (1-indexed)
    net.set_balance(1, 40)
    net.set_balance(3, -20)
    net.set_balance(4, 10)
    net.set_balance(7, -30)
    # Add edges
    net.add_edge(1, 2, 5)
    net.add_edge(1, 4, 2)
    net.add_edge(1, 6, 8)
    net.add_edge(2, 3, 10)
    net.add_edge(3, 1, 3)
    net.add_edge(3, 5, 5)
    net.add_edge(3, 7, 7)
    net.add_edge(4, 5, 6)
    net.add_edge(5, 1, 12)
    net.add_edge(5, 6, 12)
    net.add_edge(5, 3, 5)
    net.add_edge(6, 3, 9)
    net.add_edge(6, 7, 20)
    # Validate
    validation = net.validate()
    if validation != "valid":
        print(f"Validation failed: {validation}")
        exit(1)
    # Solve
    sol = net.solve()
    if sol.solved:
        print(f"Solution Status: {sol.status}")
        print(f"Total Minimum Cost: {sol.total_cost}\n")
        print("Flow Assignment:")
        for (i, j), flow in sol.flows.items():
            cost = next(e.cost for e in net.get_edges() if e.from_node == i and e.to_node == j)
            print(f"  {i}  {j} : {flow} units (cost/unit: {cost}, total: {flow*cost})")
    else:
        print(f"Failed to solve: {sol.status}")
