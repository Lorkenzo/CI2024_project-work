import numpy as np

UNARY_OPERATIONS = {
        "": lambda x: x,
        "sin": np.sin,
        "cos": np.cos,
        "tan":np.tan,
        "log": np.log,
        "exp": np.exp,
        "arccos": np.arccos,
        "arcsin":np.arcsin,
        "arctan":np.arctan,
        "sqrt":np.sqrt,
        "abs":np.abs,
        "reciprocal":np.reciprocal
    }

def compute_MSE(Y_pred, Y_real):
    '''Computes the mse given predicted and real labels'''
    MSE = 100*np.square(Y_real-Y_pred).sum()/len(Y_real)
    return MSE

def compute_FX(F, X, Y, PROBLEM_SIZE, champion = False):
    '''Computes the metrics of a given formula according to inputs and outputs'''
    # Number of terms
    num_terms = len(F) // 5

    # Pre-compute fixed F values
    coefficients = np.array([float(F[5 * i]) for i in range(num_terms)])
    variable_costs = np.array([float(F[2 + 5 * i]) for i in range(num_terms)])
    columns = np.array([int(F[3 + 5 * i].split("_")[1]) for i in range(num_terms)])
    operations = [F[1 + 5 * i] for i in range(num_terms)]
    operators = [F[4 + 5 * i] for i in range(num_terms)]

    # Map unary operations
    unary_funcs = [UNARY_OPERATIONS[op] for op in operations]

    # Extract the specific columns from X and apply variable costs
    X_selected = X[columns, :]  # Shape: (num_terms, num_rows)
    X_transformed = X_selected * variable_costs[:, np.newaxis]  # Broadcasting

    # Apply unary functions (broadcasting over rows)
    for i, func in enumerate(unary_funcs):
        X_transformed[i, :] = func(X_transformed[i, :])

    # Multiply by coefficients
    T = coefficients[:, np.newaxis] * X_transformed  # Shape: (num_terms, num_rows)

    # Apply the operators
    Y_pred = np.zeros(X.shape[1])
    for i, op in enumerate(operators):
        if op == "+":
            Y_pred += T[i, :]
        elif op == "-":
            Y_pred -= T[i, :]
        elif op == "*":
            Y_pred *= T[i, :]
        elif op == "/":
            Y_pred /= np.where(T[i, :] != 0, T[i, :], 1)  # Avoid division by zero

    # Metrics
    mse = compute_MSE(Y_pred, Y)
    # formulas with high complexity are demoted
    complexity = num_terms - PROBLEM_SIZE
    if not champion:
        mse *= np.pow(1.005,complexity)

    if np.any(Y_pred==0):
        mse = np.inf
        
    diff_abs = Y_pred - Y
    increase = np.mean(diff_abs) < 0
    inc_dec_factor = np.mean(diff_abs)
    right_sign = np.all((Y_pred > 0) == (Y > 0))
    count_right_sign = np.sum((Y_pred > 0) == (Y > 0))

    return mse, increase, right_sign, count_right_sign, inc_dec_factor
