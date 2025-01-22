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

def f2(x: np.ndarray) -> np.ndarray: ...


def f3(x: np.ndarray) -> np.ndarray: ...


def f4(x: np.ndarray) -> np.ndarray:
    return (((7 * np.cos(x[1])) + (3.2882 * np.cos(0.0193 * x[0]))) + (0.1038 * -0.8764 * x[0]))

def f5(x: np.ndarray) -> np.ndarray:
    return ((((-(8.1123e-10 * np.cos(0.5608 * x[1])) * (3.7141e-11 * np.exp(1.2721 * x[0]))) * (1.9054e-11 * np.arctan(0.333 * x[0]))) / (9.1444e-10 * np.exp(-0.9812 * x[1]))) / (-3.1266e-10 * 1.0488 * x[0]))

def f6(x: np.ndarray) -> np.ndarray:
    return ((1.2832 * 1.3207 * x[1]) - 0.4743 * 1.464 * x[0])

def f7(x: np.ndarray) -> np.ndarray: ...


def f8(x: np.ndarray) -> np.ndarray: ...
