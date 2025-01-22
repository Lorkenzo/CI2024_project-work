import numpy as np
from evaluation import compute_FX
from dataclasses import dataclass

rng = np.random.Generator(np.random.PCG64(42))

@dataclass
class Individual:
    genome: list
    fitness: tuple

def compute_unary_weights(unary_operators,j,x,y):
    """
    Compute unary operators weights depending on functions dominion and relation between input and output
    """
    W = {op: 0 for op in unary_operators}

    # Funzioni di dominio
    def is_valid_tan(x,curr):
        return np.abs(np.cos(x)) > 1e-9 and curr != -1

    def is_valid_log(x,curr):
        return x > 0 and curr != -1

    def is_valid_sqrt(x,curr):
        return x >= 0 and curr != -1
    
    def is_valid_reciprocal(x,curr):
        return x !=0 and curr != -1

    def is_valid_arcsin_arccos(x,curr):
        return -1 <= x <= 1 and curr != -1

    for i in range(x.shape[1]):  # Per ogni riga di x
        curr_x = x[j, i]
        curr_y = y[i]

        for op in unary_operators:
            if op == "sin" or op == "cos":
                if np.abs(curr_y) > 100:
                    W[op] += 2
                elif -1 <= curr_y <= 1:
                    W[op] += 3 
                else:
                    W[op] += 2

            elif op == "tan":
                if is_valid_tan(curr_x, W[op]):
                    if np.abs(curr_y) > 100:
                        W[op] += 3 
                    else:
                        W[op] += 2
                else:
                    W[op] = -1
                                
            elif op == "exp":
                if curr_y < 0 and curr_x<0:
                    W[op] +=1 
                elif np.abs(curr_y) > 100 * np.abs(curr_x):
                    W[op] += 3 
                else:
                    W[op] += 2

            elif op == "log":
                if is_valid_log(curr_x, W[op]):
                    if curr_x < 1 and curr_y < 0:
                        W[op] += 3 
                    elif curr_y < curr_x:
                        W[op] += 2 
                    else:
                        W[op] += 1
                else:
                    W[op] = -1

            elif op == "arcsin" or op == "arccos":
                if is_valid_arcsin_arccos(curr_x, W[op]):
                    if -np.pi/2 <= curr_y <= np.pi/2:
                        W[op] += 3
                    else:
                        W[op] += 1
                else:
                    W[op] = -1

            elif op == "arctan":
                if -np.pi/2 <= curr_y <= np.pi/2:
                    W[op] += 3 
                else:
                    W[op] += 2

            elif op == "sqrt":
                if is_valid_sqrt(curr_x, W[op]):
                    if curr_y <= curr_x:
                        W[op] += 3  # lower input
                    else:
                        W[op] += 1
                else:
                    W[op] = -1
            elif op == "abs":
                if curr_y >0 and curr_x <0: 
                    W[op] += 2
                else:
                    W[op] += 1
            elif op == "reciprocal":
                if is_valid_reciprocal(curr_x, W[op]):
                    if  0< np.abs(curr_x) < 1 and np.abs(curr_y) > 1:
                        W[op] += 3  # lower input
                    else:
                        W[op] += 1
                else:
                    W[op] = -1

    # Normalize weights
    WArray = [W[op] if W[op] != -1 else 0 for op in unary_operators]
    
    tot_sum = np.sum(WArray)
    if tot_sum > 0: 
        WArray = [float(w / tot_sum) for w in WArray]

    return WArray

def mutation_unary_coeff(op,curr_coeff,reset=False):
    '''Adapt the unary coefficient according to the unary operator'''
    eps = 1e-9
    
    if op == "sin" or op == "cos" or op == "tan":  
        return round(rng.choice(rng.uniform(-np.pi/2 + eps,np.pi/2,100),1)[0],4)

    elif op == "exp" or op == "log" or op == "arctan" or op == "sqrt" or op == "abs" or op == "sqrt" or op == "":
        return curr_coeff*1.1 if not reset else 1

    elif op == "arcsin" or op == "arccos":  
        return round(rng.choice(rng.uniform(-1 + eps,1,100),1)[0],4)
    
    else:
        return 1
    
def tune_constant(index,term, curr_fitness, blocks, x, y, PROBLEM_SIZE):
        '''Fine-tune a costant during the genetic algorithm'''
        mutation_factor = 1.5
        improve = True
        decrease = False
        count = 0
        while improve and count<10:

            blocks[index][term] = blocks[index][term]*mutation_factor if not decrease else blocks[index][term]/mutation_factor  # Modify costant
            new_genome = [elem for block in blocks for elem in block]
            new_mse, _, right_sign, count, _ = compute_FX(new_genome, x, y,PROBLEM_SIZE)
            new_fitness = (right_sign, -new_mse, count)
            # Aggiorna la soluzione migliore
            if new_fitness > curr_fitness:
                curr_fitness = new_fitness
                
                mutation_factor*=0.96
            else:
                blocks[index][term] = blocks[index][term] / mutation_factor if not decrease else  blocks[index][term] * mutation_factor # revert change
                if not decrease:
                    decrease = True
                else: 
                    improve = False

            count+=1
        
        if round(blocks[index][term]) != 0 :
            blocks[index][term] = round(blocks[index][term],4)
        return blocks[index][term]

def convert_formula(F):
    """
    Convert the formula to string
    """
    formula = [F[i*5:(i+1)*5] for i in range(len(F)//5)]

    terms = []
    
    for term in formula:
        coeff = float(term[0])
        unary_op = term[1]
        var_cost = float(term[2])
        var_name = term[3]
        binary_op = term[4]

        # Costruisci il termine con operazione unaria se presente
        var_expression = f"{var_cost} * x[{var_name.split('_')[1]}]"
        if unary_op:
            var_expression = f"np.{unary_op}({var_expression})"

        # Combina con il coefficiente
        term_expression = f"({coeff} * {var_expression})"
        terms.append((term_expression, binary_op))

    # Combina i termini con gli operatori binari, rispettando l'ordine e le parentesi
    formula = terms[0][0]
    for i in range(1, len(terms)):
        term_expression, binary_op = terms[i]
        if terms[0][1] == "-" and i == 1:
            formula = f"(-{formula} {binary_op} {term_expression})"
        else:
            formula = f"({formula} {binary_op} {term_expression})"

    return formula
