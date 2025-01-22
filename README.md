# CI2024_project-work
## Project Work: Symbolic Regression
## Log
- __22/12/2024__: first understanding of the problem, how to find a proper formula? (Review of the lessons about symbolic regression and genetic algorithm)
- __23/12/2024__: I understood that using a genetic algorithm could be a good way to generate a proper formula. The first problem i faced was about individuals generation. 

    * #### Individual generation
    I realized from the start that i was not searching for the exact formula, cause it would have taken a lot of time and complex algorithm considering an huge amount of variables, beyond the high computational cost. So i searched for an easy rappresentation of the formula with fixed length terms (to avoid bloating) in order to cover the maximum possibility of problems. To create the individuals i started from the constraint that all the variables in input must be used to generate the formula (there are not useless informations). I assumed that constraint for a simple logic reason, if i start creating formulas without the given inputs i'm not searching anymore for a formula but for a random combination of constant and operands. <br>
    After all the above considerations i decided to generate the terms of the individual genome (formula) using an array of string/float composing the formula logic and order. A single term is structured in the following fixed way and order: <br><br>
    <p style="text-align:center">"constant", "unary_operator", "variable_constant", "variable", "binary_operator"<p>
    es. "1", "sin", "1", "X_0", "+"<br><br>
    Where: <br>
    - constant: works as a weight for the term, it is a random float that multiply the whole term<br>
    - unary_operator: can be either a unary operator from numpy (es.sin,cos,exp..) or an empty string <br>
    - variable_constant: is a second weight specific for the variable, useful when the unary operator is present, it allows results to converge faster weighting directly the input variable. When the unary operator is not present it works at the same way of the first constant. It starts always from 1, then it is modified during the algorithm.
    - variable: can be one of the input variables in string form.<br>
    - binary_opertor: is the binary operator that connect the term to the previous one. The first term in the array will have as a previous term implicitly zero (0), for that reason it can have only (+,-) as binary operator (works as a sign for the first term).<br><br>
    Each formula will have N terms, with N >= C, where C is the complexity of the problem given by the number of input variables. I also introduced a limit for the number of terms to avoid bloating.<br>

    * #### Evaluation 
    I realized a first basic function to compute the result of the formula starting from the array of string, to compute predictions and mse, which is the main fitness measure.

    * #### EA
    For the EA i created a first single crossover function to exchange similiar term in the formula (same x variable) and a multiple mutation function that change randomly n parameters in the formula. The algorithm is steady state.

- __24/12/2024__: I obtain first results for problem 0 (test) and 1, but i also faced first issues with problem 2. It has low input values and extremely high output values having problems to converge. 

    * #### Operators weights
    In order to favor the convergence of the algorithm, and to avoid generating individual with invalid unary operator, i created custom weights considering the input values and output values. The weight are created in a greedy way following relationship between inputs and outputs and domain of each operator. So i created an array of probability for each unary operator and for each input variable. In this way both when generating or changing individuals there are no errors anymore and the performance can improve

    * #### Mutation factor
    The first solution used in order to provide a better solution for problem 2 or other hard problems was to mutate the coefficient of the formula with an adaptive mutation factor in order to reach faster higher values. The adaptation was based on the distance between predicted and real labels.

- __25/12/2024__: I improve the weights logic in order to make the algorithm converge to a possible solution. 
    * #### Weights tuning
    The operators weights are increase or decrease every time a new child with a genome that uses them results in increasing or decreasing the fitness with respect to the parents. Now both the mutation and the crossover have multiple chances to improve the fitness (if it increase it exit immediatly from the child generation).

- __29/12/2024__: Since in the first solution the only possibility was to have a number of terms for the formula equals to C (N==C). I realized that i was simplifing too much the problem, so i inserted a method to add terms if the algorithm was not improving for a certain number of iterations. (I will change also this method later on). I also implemented a early stopping to avoid wasting time on mesas.
- __30/12/2024__: I fixed some bugs coming up when running different problems, related both to mathematical issues and logic issues.
- __4/01/2025__: I improved the EA by introducing custom selections.
    * #### Selection
    I decided to use a rank based selection both for parent selection and for survival selection. This is due to the fact that the issue with fitness based selection would have had the risk to favor too much the strongest individual. Instead i wanted to favor diversity. I' ve also added a fitness hole for the selection based on right-sign count, this metric consist in a simple count of how many predicted labels have the right sign (+,-). In this way i provided a good diversity selection.
- __11/01/2025__: Since the initial population was always too far from a good solution i introduce a new custom method to generate an initial population for the EA.
  
    * #### Initial population
    Instead of starting with a certain complexity and getting it higher during the EA i decided to create from the beginning individuals with different genome complexity, giving an upper bound for the maximum complexity and a decreasing probability to be genrated for higher complexity formulas.

    * #### Bloating
    To avoid the algorithm to choose a more complex formulas with respect to a more simpler one when the fitnesses are close i introduced a mse penalty based on the complexity. In this way bigger inidividuals are penalized.

    * #### Tournament generation
    To increase the strenght in terms of both fitness and diversity i introduced this generation step for the population. Given a number of tournaments NT and a population size PS, i generated PS*NT individuals that are going to partecipate to the tournaments. The population is sorted by fitness and again splitted in NT parts. At the same way i splitted the input data and labels into NT parts. At this point the EA is reapeted iteratively for each tournament (for few generations, 50) using a partition of the individuals and a partition of input data. In this way each partition in going to be specialized for different data and different input population, increasing extremely the diversity in a small amount of time. The winner of each tournament is going to become part of the population for the main EA loop. For the algorithm i choose NT == PS, so that i generate exactly PS winners for the main EA.

- __18/01/2025__: I met 2 collegues (s331553 and s331578) to discuss about the project and exchange some useful information to improve the performances. They also implemented a EA, but they used a standard tree to create the formula and they used many different crossovers and tree mutations. However they gave me useful information about the initial constant generation. In fact they generate initial costants considering the standard deviation of the inputs values with respect to the output ones. So i followed the same mathematical rule adapting the generation function to my code. They also suggest me to use vizgraph for graph and trees visualization.

- __19/01/2025__: I implemented the custom generation of the initial costant and also a new custom way to improve the adaptivness of the mutation of the single costants.
    * #### Constant tuning
    Since the initial mutation factor was not working well, cause it was adapting to different formulas every time, and it wasn't giving useful tuning to the costant, i create a new tuning function. The simple concept is that the function tries either to increase or decrease the costant with a specific mutation factor according to the resulting fitness. The tuning is done iteratively until the fitness increase for a certain number of iterations. It sacrifies a bit of computational cost to better fit the costants.
    * #### Final tuning
    I've also inserted a final costant tuning regarding only the final winner of the main EA. For that final tuning i inserted a small mutation factor tring to exploit the local maximum. This function as the previous one tries to tune random costants of the winner with a high number of iterations (50000) with a early stopping if it finds a mesa.
    * #### Tree visialization
    Also if i didn't explicitely used a tree structure i implemented a function using vizgraph (as suggested from my collegues) to have a good visualization of the winner.

- __20-22/01/2025__: I gathered together all the data for the given probelms and also implemented a function to convert the genome (array of float and strings) into a single line string corresponding to the final formula.

### Code and results
All the result can be found in the [Proble Solutions File](s330260.py), and the code in the [src folder](src/)
