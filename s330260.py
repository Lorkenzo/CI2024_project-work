# Copyright © 2024 Giovanni Squillero <giovanni.squillero@polito.it>
# https://github.com/squillero/computational-intelligence
# Free under certain conditions — see the license for details.

import numpy as np

# All numpy's mathematical functions can be used in formulas
# see: https://numpy.org/doc/stable/reference/routines.math.html


# Notez bien: No need to include f0 -- it's just an example!
def f0(x: np.ndarray) -> np.ndarray:
    return x[0] + np.sin(x[1]) / 5


def f1(x: np.ndarray) -> np.ndarray: 
    return np.sin(x[0])

def f2(x: np.ndarray) -> np.ndarray:
    return ((((((224928 * 3.362 * x[2]) + 977753.9814 * 1.247 * x[1]) - 1747375.474 * np.arctan(-0.4426 * x[2])) * 0.994 * np.cos(-0.502 * x[0])) + 1247989.7133 * np.sin(0.0269 * x[1])) + 3000251.7633 * np.arctan(1.089 *x[0]))

def f3(x: np.ndarray) -> np.ndarray:
    return ((((4.9127 * np.abs(1.7364 * x[0])) - (17.737 * 1.5036 * x[1])) - 2.9209 * 1.1914 * x[2]) + 5.0619 * np.cos(-1.3349 * x[0])) + 51.8489 * np.sin(0.5644 * x[1])

def f4(x: np.ndarray) -> np.ndarray:
    return (((7 * np.cos(x[1])) + (3.2882 * np.cos(0.0193 * x[0]))) + (0.1038 * -0.8764 * x[0]))

def f5(x: np.ndarray) -> np.ndarray:
    return ((((-(8.1123e-10 * np.cos(0.5608 * x[1])) * (3.7141e-11 * np.exp(1.2721 * x[0]))) * (1.9054e-11 * np.arctan(0.333 * x[0]))) / (9.1444e-10 * np.exp(-0.9812 * x[1]))) / (-3.1266e-10 * 1.0488 * x[0]))

def f6(x: np.ndarray) -> np.ndarray:
    return ((1.2832 * 1.3207 * x[1]) - 0.4743 * 1.464 * x[0])

def f7(x: np.ndarray) -> np.ndarray:
    return ((((((-3.35 * 0.9319 * x[1]) * (3.4445 * np.cos(x[0]))) + (10.6769 * 1.2148 * x[0])) * (-0.0493 * -1.8404 * x[1])) + (2.2454 * np.abs(1.0264 * x[1]))) * (4.9920 * np.abs(1.0889 * x[0])))

def f8(x: np.ndarray) -> np.ndarray:
    return ((((((((406.5744 * np.cos(-0.084 * x[1])) + 409.5379 * np.cos(-5.5364e-7*x[0])) + 67.2911 * 0.676 * x[3]) + 2933.8781 * np.tan(0.28*x[5])) - 401.3556 * np.abs(1.4305*x[4])) + 0.001 * np.abs(x[2])) -624.0142 * np.cos(1.0164 * x[4])) - 1848.7071 * np.sin(0.641*x[5]))
