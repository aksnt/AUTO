""" This module contains a very simple parser to help you read the input files.
You don't need to edit this file, but you can if you want. You can even delete
it, if you'd prefer to write your own parsing functions."""

from sys import stdin

def next_line(stream):
    for line in stream:
        line = line.split(';')[0].strip()
        yield line

def parse_fa(stream=stdin):
    """Read from the stream, return a dictionary representing the nfa/dfa.

    key 'Sigma' gives the set of alphabet symbols (as a list)
    key 'Q' gives the set of states (as a list)
    key 'start' gives the label of the start state
    key 'F' gives the set of final states (as a list)
    key 'delta' gives a list of (s, c, t) tuples

    This is not a very efficient representation of a FA, you may want to
    use this data to construct something more useful.
    """
    it = iter(next_line(stream))
    automata = dict()
    automata['Sigma'] = next(it).split('=')[1].split()
    automata['Q'] = next(it).split('=')[1].split()
    automata['start'] = next(it).split('=')[1].strip()
    automata['F'] = next(it).split('=')[1].split()
    # the remaining lines are the transitions delta(s,c)=t
    automata['delta'] = list()
    for line in it:
        if not line:
            break
        s, c, t = line.split()
        automata['delta'].append((s, c, t))
    return automata

def parse_strings(stream=stdin):
    """Read a series of implicit strings from the stream.
    Returned as a list of lists of tuples (x_i, n_i) where:
        x_i is a string
        n_i is an integer exponent

    For example, the input:
        ab 30 cda 200 bb 17
    Would be returned as:
        [('ab', 30), ('cda', 200), ('bb', 17)]"""
    it = iter(next_line(stream))
    strings = []
    for line in it:
        string = line.split()
        strings.append(list(zip(string[0::2], map(int, string[1::2]))))
    return strings
