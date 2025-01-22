from graphviz import Digraph
from IPython.display import Image, display
import numpy as np
from graphviz import Digraph

def create_formula_graph(F):
    """
    Creates the digraph starting from the formula generating at first the subtrees corresponding to each term,
    then it matches all the terms following the binary operators order to reproduce the formula logic.
    """
    graph = Digraph(format='png')
    graph.attr(rankdir='TB')  # Layout top-to-bottom (tree)

    num_terms = len(F) // 5

    # Generate nodes for each term
    term_nodes = []
    for i in range(num_terms):
        coeff = round(float(F[5 * i]),4) if round(float(F[5 * i]),4) != 0 else float(F[5 * i])
        unary_op = F[1 + 5 * i]
        var_cost = round(float(F[2 + 5 * i]),4) if round(float(F[2 + 5 * i]),4) != 0  else float(F[2 + 5 * i])
        column = F[3 + 5 * i]

        # Names of the nodes for each term
        coeff_node = f"{i}_coeff"
        mul_node = f"{i}_mul"
        unary_node = f"{i}_unary"
        var_node = f"{i}_var"
        
        graph.node(coeff_node, label=f"{coeff}" if i !=0 else f"{F[4 + 5 * i]} {coeff}", shape="box")
        graph.node(mul_node, label="*", shape="circle")
        graph.node(unary_node, label=f"{unary_op}", shape="circle")
        graph.node(var_node, label=f"{var_cost} {column}", shape="box")

        # links between nodes of the subtree (fixed)
        graph.edge(mul_node, coeff_node)
        graph.edge(mul_node, unary_node)
        graph.edge(unary_node, var_node)

        term_nodes.append(mul_node)

    # Link all the subtrees generated with binary operators
    current_node = term_nodes[0]
    for i in range(1, num_terms):
        operator = F[4 + 5 * i]  # Current binary op
        op_node = f"op_{i}"  # OpBin node name

        graph.node(op_node, label=operator, shape="circle")

        if i == 1:
            graph.edge(op_node, term_nodes[i])  
            graph.edge(op_node, current_node) 
        else:
            graph.edge(op_node, term_nodes[i])  
            graph.edge(current_node, op_node)   
        current_node = op_node

    return graph

# Usage Example
if __name__ == "__main__":
    F = [
    "1.0", "tan", "2.0", "X_0", "+",
    "0.5", "log", "3.0", "X_1", "*",
    "2.0", "sin", "1.0", "X_2", "-"
    ]

    graph = create_formula_graph(F)

    img = graph.pipe("png")

    display(Image(img))
