import gurobipy as gp
from gurobipy import GRB


def test_addGenConstrIndicator():
    """
    if op1 != op2:
         # Create binary variables to enforce the relative order
        y1 = model.addVar(vtype=GRB.BINARY, name=f"y1_{op1}_{op2}_{d}")
        y2 = model.addVar(vtype=GRB.BINARY, name=f"y2_{op2}_{op1}_{d}")

        # Ensure non-overlapping based on the order using indicator constraints
        model.addGenConstrIndicator(y1, True, start[op2] >= finish[op1])
        model.addGenConstrIndicator(y2, True, finish[op2] <= start[op1])

        # Ensure that one of the orderings holds
        model.addConstr(y1 + y2 == x[op1, d] * x[op2, d], name=f"order_{op1}_{op2}_{d}")
    """
    # Create a new Gurobi model
    model = gp.Model("test_addGenConstrIndicator")

    # Add binary variables
    x1 = model.addVar(vtype=GRB.BINARY, name="x1")
    x2 = model.addVar(vtype=GRB.BINARY, name="x2")

    # Add continuous variable
    y = model.addVar(vtype=GRB.CONTINUOUS, name="y", lb=10, ub=500)

    # Set objective (for demonstration purposes, let's maximize y)
    model.setObjective(y, GRB.MAXIMIZE)

    # Add indicator constraints
    # When x1 is 1, y should be <= 10
    model.addGenConstrIndicator(x1, True, y <= 10)
    # When x1 is 0, y should be >= 100
    model.addGenConstrIndicator(x1, False, y >= 100)

    # When x2 is 1, y should be <= 20
    model.addGenConstrIndicator(x2, True, y <= 20)
    model.addGenConstrIndicator(x2, False, y <= 200)

    # Also add a constraint to link x1 and x2 (for demonstration purposes)
    model.addConstr(x1 + x2 <= 1, "linking_constraint")

    # Optimize the model
    model.optimize()

    # Print the results
    if model.status == GRB.OPTIMAL:
        print("Optimal solution found:")
        for v in model.getVars():
            print(f"{v.VarName} = {v.X}")
    else:
        print(f"Optimization ended with status {model.status}")


# x5 = and(x1, x3, x4)
# model.addGenConstrAnd(x5, [x1, x3, x4], "andconstr")

# overloaded forms
# model.addConstr(x5 == and_([x1, x3, x4]), "andconstr")
# model.addConstr(x5 == and_(x1, x3, x4), "andconstr")

def test_if_else():
    model = gp.Model("test_addGenConstrIndicator")
    y = model.addVar(ub=50000, vtype=GRB.CONTINUOUS, name="y")
    b = model.addVar(vtype=GRB.BINARY, name="b")
    w1 = model.addVar(vtype=GRB.CONTINUOUS, name="w1", lb=999, ub=1000)
    w2 = model.addVar(vtype=GRB.CONTINUOUS, name="w2", lb=500, ub=2000)
    # if b==1, then y = w1
    model.addConstr((b == 1) >> (y == w1), name="indicator_constr1")
    model.addConstr((b == 0) >> (y == w2), name="indicator_constr2")
    model.setObjective(y, GRB.MAXIMIZE)
    model.optimize()
    # Print the results
    if model.status == GRB.OPTIMAL:
        print("Optimal solution found:")
        for v in model.getVars():
            print(f"{v.VarName} = {v.X}")
