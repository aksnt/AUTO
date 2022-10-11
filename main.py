import parser

""" 
    Return an equivalent string but where all powers are powers of 2
    e.g. (abc,10), (bc,6) returns (abc,2), (abc,8), (bc, 4), (bc,2)
"""
def breakdown(string):
    powers = list()
    for element in string:
        i = 0
        n = element[1]
        while n > 0:
            if n % 2 != 0:
                powers.append((element[0], 2**i))
            n = n // 2
            i = i + 1
    return powers


""" 
    Parameters: Chunk = string, Transition = dict, state = int
    Parse in chunk to a queue but using sets to avoid duplicates in queue for a
    state (usually starting state of 0)
    Returns a set of ending states for a certain chunk given a transition table
"""
def original_dfa(chunk, transitions, state):
    q = set()
    results = set()
    q.add((0, state))

    while q:
        #pop the front of queue and set variables for processing
        front = q.pop()
        idx = front[0]
        state = front[1]
        
        #We have reached some end, add to our set of results
        if idx == len(chunk):
            results.add(state)
            continue #until our queue is empty so all results are handled

        #Otherwise, check our dictionary
        if state in transitions.keys():
            if chunk[idx] in transitions[state]:
                for s in transitions[state][chunk[idx]]:
                    q.add((idx + 1, s)) #add to our idx to keep track of string length
    return results

def decide(automata, string):

    # Construct a transitions table from input: transitions[state][letter] = next_state(s)
    transitions = {}
    for x, y, z in automata['delta']:
        if x not in transitions: transitions[x] = {}
        if y not in transitions[x]: transitions[x][y] = []
        transitions[x][y].append(z)

    ''' 
    Populate chunky transitions for power of 1: 
    Chunky transitions keeps transitions for large strings. 
    chunky_transitions[state][chunk] = next_states -> e.g. abc ends in states 1,2,3
    ''' 
    chunky_transitions = {}
    for state in transitions: 
        for chunk in string: # (aa, 4) 
            if state not in chunky_transitions: chunky_transitions[state] = {}
            if chunk not in chunky_transitions[state]: 
                chunky_transitions[state][(chunk[0],1)] = []
            
            result = original_dfa(chunk[0], transitions, state) #passed into original dfa for that state
            chunky_transitions[state][(chunk[0],1)].extend(result) # stored in chunky_transitions
    
    ''' Populate chunky transitions for remaining powers as we need them only '''
    powers = breakdown(string)
    biggest_powers = {} #stores each chunk's largest power of 2. e.g ab 10 will store (ab, 8) only
    for (c, p) in powers:
        if c not in biggest_powers:
            biggest_powers[c] = p
        elif p > biggest_powers[c]:
            biggest_powers[c] = p
    
    for (c, maxp) in biggest_powers.items():
        p = 2 #all p = 1 are already in chunky transitions
        while p <= maxp:
            # work out, e.g. c^16 = (c^8)(c^8)
            smaller_chunk = (c, p//2)
            for state in transitions:
                current_states = set(state) #sets are used to avoid duplicates and waste time
                middle_states = chunky_transitions[state][smaller_chunk]
                final_states = set()
                for midstate in middle_states:
                    final_states = final_states.union(chunky_transitions[midstate][smaller_chunk])
                chunky_transitions[state][(c,p)] = final_states
            p *= 2 #increment by powers of 2

    #Full chunk is parsed in here with a set of final states returned. 
    final_states = original_dfa(powers, chunky_transitions, automata['start'])

    # If any state in final states is a final state of our automata, then true
    for state in final_states:
        if state in automata['F']: return True
    return False

if __name__ == '__main__':
    
    automata = parser.parse_fa()
    strings = parser.parse_strings()
    
    for string in strings:
        print(decide(automata, string))

