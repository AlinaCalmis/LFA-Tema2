import sys
from typing import List, Tuple, Set, Dict


State = int
Word = str
Configuration = Tuple[State, Word]
Transition = Tuple[State, Word, List[State]]
EPSILON = ""

vector_of_states = []
class DFA:
    def __init__(self, numberOfStatesD, finalStatesD, statesCodificationD,
                 deltaD):
        self.numberOfStatesD = numberOfStatesD
        self.finalStatesD = finalStatesD
        self.statesCodificationD = statesCodificationD
        self.deltaD = deltaD


class NFA:
    def __init__(self, numberOfStates: int, alphabet: Set[chr], finalStates: Set[State],
                 delta: Dict[Tuple[State, chr], Set[State]]):
        self.numberOfStates = numberOfStates
        self.states = set(range(self.numberOfStates))
        self.alphabet = alphabet
        self.initialState = 0
        self.finalStates = finalStates
        self.delta = delta

    def epsilonClosure(self):
        eps = set()
        E = []

        # calculeaza inchiderile epsilon pentru fiecare stare in parte

        for i in self.states:
            current_state = i
            eps.add(current_state)
            for (s, l) in self.delta:
                for i in self.delta[(s, l)]:
                    if s == current_state and l == '':
                        eps.add(i)
                        if (i,'') not in self.delta:
                            continue
                        else:
                            current_state = i
            E.append(eps)
            eps = set()

        return E

    def getDFA(self, closures):
        zero_state = -1
        count_states = 0
        current_state = 0

        final = dict()
        final_DFA_states = set()

        # se porneste de la inchiderea lui 0
        vector_of_states.append(closures[0])

        for i in self.finalStates:
            for el in closures[0]:
                if i == el:
                    final_DFA_states.add(0)
                    break

        while zero_state != count_states:

            zero_state = current_state

            if zero_state == 0:
                closure = closures[0]
            else :
                cl = vector_of_states.pop(current_state)
                vector_of_states.insert(current_state,cl)
                closure = cl
            # pentru fiecare litera din alfabet, in afare de EPSILON
            # si pentru fiecare stare din inchidere se creeaza un nou vector de stari
            for letter in self.alphabet:
                if letter != '':
                    new_state = set()
                    for state in closure:
                        if (state,letter) in self.delta:
                            for next_step in self.delta[(state,letter)]:
                                new_state.add(next_step)

                    aux_new_State = set()
                    for element in new_state:
                        for e in closures[element]:
                            aux_new_State.add(e)

                    if aux_new_State in vector_of_states:
                        idx = vector_of_states.index(aux_new_State)
                        final[(zero_state, letter)] = idx
                    else:
                        count_states += 1
                        final[(zero_state,letter)] = count_states
                        vector_of_states.append(aux_new_State)
                        for i in self.finalStates:
                            if i in aux_new_State:
                                final_DFA_states.add(count_states)
                                break
            current_state += 1

        # toate datele se salveaza intr-un dfa
        dfa = DFA(
            numberOfStatesD = count_states,
            finalStatesD = final_DFA_states,
            statesCodificationD = vector_of_states,
            deltaD = final
        )

        return dfa



if __name__ == '__main__':
    alphabet = set()
    with open(sys.argv[1]) as file:
        numberOfStates = int(file.readline().rstrip())
        finalStates = set(map(int, file.readline().rstrip().split(" ")))
        delta = dict()
        while True:
            transition = file.readline().rstrip().split(" ")
            if transition == ['']:
                break
            if transition[1] == "eps":
                transition[1] = EPSILON

            delta[(int(transition[0]), transition[1])] = set(map(int, transition[2:]))

    for (state, w) in delta:
        alphabet.add(w)

    nfa = NFA(
        numberOfStates=numberOfStates,
        alphabet=alphabet,
        finalStates=finalStates,
        delta=delta
    )

    closures = nfa.epsilonClosure()
    dfa = nfa.getDFA(closures)

    w = open(sys.argv[2], "w")
    w.write(str(dfa.numberOfStatesD + 1))
    w.write("\n")

    for i in dfa.finalStatesD:
        w.write(str(i) + " ")

    w.write("\n")

    for (s, l) in dfa.deltaD:
        w.write(str(s) + " " +str(l) + " " + str(dfa.deltaD[(s,l)]))
        w.write("\n")
