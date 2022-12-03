import copy

class State:
    final = False
    previousState = []
    nextState = []
    output = []

    

alphabet = "abcdefghijklmnopqrstuvwxyz"

def Member(dict, state):
    for i in range(len(dict)):
        if (id(dict[i]) == id(state)):
            return state
    return None

def Insert(dict,state):
    dict.append(state)

def ClearState(state: State):
    state.previousState = []
    state.nextState = []
    state.output = []
    state.final = False

def SetTransition(state1: State,c,state2: State):
    state1.nextState.append([c,state2, ""])
    state2.previousState.append([c,state1,""])

def SetFinal(state: State):
    state.final = True

def Output(state: State, c):
    for i in range(len(state.nextState)):
        if state.nextState[i][0] == c:
            return state.nextState[i][2]
        else:
            return ""

def SetOutput(state: State, c, str):
    for i in range(len(state.nextState)):
        if state.nextState[i][0] == c:
            state.nextState[i][2] = str

def CPrefix(s1,s2):
    prefix = ""
    for i in range(min(len(s1),len(s2))):
        if s1[i] == s2[i]:
            prefix = prefix + s1[i]
        else: break 
    return prefix

def CSuffix(s1,s2):
    a = s2[len(s1):len(s2)]
    if a == None:
        return ""
    else: return a 

def StateOutput(state: State):
    return state.output

def SetStateOutput(state:State, array):
    state.output = array

def Transition(state:State, c):
    for i in range(len(state.nextState)):
        if state.nextState[i][0] == c:
            return state.nextState[i][1]

def dfs(visited, node): 
    if node not in visited:
        print (node)
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)
    


StateDict = []

#dictionary = ["abacate","abelha","amanda","amor","banana","batata","beta","betaa","casimireee"]
dictionary = ["abcd"]

MaxWordSize = 4

TempState = [""]*(MaxWordSize+1)

def FindMinimized(s: State) -> State:
    r = State()
    r = Member(StateDict,s)
    if r == None:
        r = s
        Insert(StateDict,s)
    return r

def FST(dictionary):
    for i in range(MaxWordSize+1):
        TempState[i] = State()
    PreviousWord = ""
    ClearState(TempState[0])
    
    for CurrentWord in dictionary:
        i = 1
        CurrentOutput = ""
        while (i<len(CurrentWord) and i<len(PreviousWord) and PreviousWord[i-1] == CurrentWord[i-1]):
            i = i+1
        PrefixLength = i

        for i in reversed(range(PrefixLength,len(PreviousWord)+1)):
            SetTransition(TempState[i-1],PreviousWord[i-1],FindMinimized(TempState[i]))
            
        for i in range(PrefixLength,len(CurrentWord)+1):
            ClearState(TempState[i])
            SetTransition(TempState[i-1],CurrentWord[i-1],TempState[i])
            
        if CurrentWord != PreviousWord:
            SetFinal(TempState[len(CurrentWord)])
            SetStateOutput(TempState[len(CurrentWord)],[])

        for j in range(1,PrefixLength):
            CommonPrefix =  CPrefix(Output(TempState[j-1], CurrentWord[j-1]), CurrentOutput)
            WordSuffix = CSuffix(CommonPrefix,Output(TempState[j-1],CurrentWord[j-1]))
            SetOutput(TempState[j-1],CurrentWord[j-1],CommonPrefix)

            for c in alphabet:
                if Transition(TempState[j],c) != None:
                    SetOutput(TempState[j],c, WordSuffix + Output(TempState[j],c))

            if TempState[j].final:
                TempSet = []
                for TempString in StateOutput(TempState[j]):
                    TempSet.append(WordSuffix + TempString)
                SetStateOutput(TempState[j],TempSet)

            CurrentOutput = CSuffix(CommonPrefix,CurrentOutput)

        if CurrentWord == PreviousWord:
            SetStateOutput(TempState[len(CurrentWord)], StateOutput(TempState[len(CurrentWord)]).append(CurrentOutput))
        else: 
            SetOutput(TempState[PrefixLength-1],CurrentWord[PrefixLength-1],CurrentOutput)
        PreviousWord = CurrentWord
        
    for i in reversed(range(1,len(CurrentWord)+1)):
        SetTransition(TempState[i-1],PreviousWord[i-1],FindMinimized(TempState[i]))
    FindMinimized(TempState[0])

FST(dictionary)
for i in range(MaxWordSize):
    print(StateDict[i].nextState)
    print(StateDict[i].previousState)
    print("\n")