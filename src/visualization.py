from graphviz import Digraph
from IPython.display import Image, display
import numpy as np
from graphviz import Digraph

def create_formula_graph(F):
    """
    Crea una rappresentazione ad albero per una formula simbolica.
    Rispecchia l'ordine dei calcoli effettivi, combinando i termini uno alla volta
    tramite gli operatori binari.
    """
    if not F or len(F) % 5 != 0:
        raise ValueError("Il vettore F deve essere non vuoto e un multiplo di 5.")

    graph = Digraph(format='png')
    graph.attr(rankdir='TB')  # Layout top-to-bottom (albero)

    num_terms = len(F) // 5

    # Crea i nodi per i termini
    term_nodes = []
    for i in range(num_terms):
        coeff = round(float(F[5 * i]),4) if round(float(F[5 * i]),4) != 0 else float(F[5 * i])
        unary_op = F[1 + 5 * i]
        var_cost = round(float(F[2 + 5 * i]),4) if round(float(F[2 + 5 * i]),4) != 0  else float(F[5 * i])
        column = F[3 + 5 * i]

        # Nodi specifici del termine
        coeff_node = f"{i}_coeff"
        mul_node = f"{i}_mul"
        unary_node = f"{i}_unary"
        var_node = f"{i}_var"
        
        graph.node(coeff_node, label=f"{coeff}" if i !=0 else f"{F[4 + 5 * i]} {coeff}", shape="box")
        graph.node(mul_node, label="*", shape="circle")
        graph.node(unary_node, label=f"{unary_op}", shape="circle")
        graph.node(var_node, label=f"{var_cost} {column}", shape="box")

        # Collegamenti per il termine
        graph.edge(coeff_node, mul_node)
        graph.edge(mul_node, unary_node)
        graph.edge(unary_node, var_node)

        # Salva il nodo rappresentante il termine per uso successivo
        term_nodes.append(coeff_node)

    # Crea l'albero seguendo i calcoli effettivi
 

    # Collega i termini uno alla volta tramite operatori binari
    current_node = term_nodes[0]
    for i in range(1, num_terms):
        operator = F[4 + 5 * i]  # Operatore binario corrente
        op_node = f"op_{i}"  # Nodo operatore binario

        graph.node(op_node, label=operator, shape="circle")

        if i == 1:
            graph.edge(op_node, term_nodes[i])  # Collega il termine successivo
            graph.edge(op_node, current_node)  # Collega il risultato parziale corrente
        else:
            graph.edge(op_node, term_nodes[i])  # Collega il termine successivo
            graph.edge(current_node, op_node)  # Collega il risultato parziale corrente    
        # Aggiorna il nodo corrente al risultato parziale
        current_node = op_node

    # Collega l'ultimo risultato parziale alla radice
    #graph.edge(result_node, current_node)

    return graph


if __name__ == "__main__":
    F = [
    "1.0", "identity", "2.0", "X_0", "+",
    "0.5", "log", "3.0", "X_1", "*",
    "2.0", "sin", "1.0", "X_2", "-"
    ]

    graph = create_formula_graph(F)

    # Genera l'immagine direttamente in memoria
    img = graph.pipe("png")

    # Mostra l'immagine
    display(Image(img))
