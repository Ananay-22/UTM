# forward declare types
from __future__ import annotations
from typing import Callable

from math import log
from constants import MAX_ELEMENTS_IN_BLOCK
alphaFromZ: Callable[[float], float] = lambda z: 255 * max(0, 1 - log(z, MAX_ELEMENTS_IN_BLOCK))
"""
Returns the transparency of a block depending on how high it is on the stack in a given block.
Height is not its physical height. It is a measure of when it gets rendered with respect to all the other objects on the current block.
The higher the block, the more transparent.
"""
