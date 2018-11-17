import random
import sys
from inspect import isclass

#genGrow and generate function copied from gp.py
#genGrow changed to simply calling another generate function (generate_edit)
#generate_edit created so that when the program tries to add primitives and there are none, it then tries to add terminals (and vice-versa)
#(gives error only if both don't exist)

def genGrow_edit(pset, min_, max_, type_=None):
    """Generate an expression where each leaf might have a different depth
    between *min* and *max*.
    :param pset: Primitive set from which primitives are selected.
    :param min_: Minimum height of the produced trees.
    :param max_: Maximum Height of the produced trees.
    :param type_: The type that should return the tree when called, when
                  :obj:`None` (default) the type of :pset: (pset.ret)
                  is assumed.
    :returns: A grown tree with leaves at possibly different depths.
    """
    def condition(height, depth):
        """Expression generation stops when the depth is equal to height
        or when it is randomly determined that a a node should be a terminal.
        """
        return depth == height or \
            (depth >= min_ and random.random() < pset.terminalRatio)
#CHANGED
    return generate_edit(pset, min_, max_, condition, type_)

def generate_edit(pset, min_, max_, condition, type_=None):
    """Generate a Tree as a list of list. The tree is build
    from the root to the leaves, and it stop growing when the
    condition is fulfilled.
    :param pset: Primitive set from which primitives are selected.
    :param min_: Minimum height of the produced trees.
    :param max_: Maximum Height of the produced trees.
    :param condition: The condition is a function that takes two arguments,
                      the height of the tree to build and the current
                      depth in the tree.
    :param type_: The type that should return the tree when called, when
                  :obj:`None` (default) the type of :pset: (pset.ret)
                  is assumed.
    :returns: A grown tree with leaves at possibly different depths
              dependending on the condition function.
    """

    if type_ is None:
        type_ = pset.ret
    expr = []
    height = random.randint(min_, max_)
    stack = [(0, type_)]

#ADDED
    def add_terminal(retry=True):
        try:
            term = random.choice(pset.terminals[type_])
        except IndexError:
            if retry:
                add_primitive(False)
            else:
                emit_fail(IndexError)
            return

        if isclass(term):
            term = term()
        expr.append(term)

#ADDED
    def add_primitive(retry=True):
        try:
            prim = random.choice(pset.primitives[type_])
        except IndexError:
            if retry:
                add_terminal(False)
            else:
                emit_fail(IndexError)
            return

        expr.append(prim)
        for arg in reversed(prim.args):
            stack.append((depth + 1, arg))

#ADDED
    def emit_fail(IndexError):
        _, _, traceback = sys.exc_info()
        raise IndexError, "The gp.generate function tried to add "\
                          "a terminal of type '%s', but there is "\
                          "none available." % (type_,), traceback

#CHANGED
    while len(stack) != 0:
        depth, type_ = stack.pop()
        if condition(height, depth):
            add_terminal()
        else:
            add_primitive()
    return expr

