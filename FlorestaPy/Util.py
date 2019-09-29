import math

def log2(x):
    return math.log(x) / math.log(2)

def prec(vp, fp):
    return  vp / (vp + fp)

def rec(vp, fn):
    return  vp / (vp + fn)

def fScore(listOfTuples, beta):
    vp = 0
    fp = 0
    fn = 0
    vn = 0
    for tup in listOfTuples:
        if tup[0] == 'Sim' and tup[1] == 'Sim':
           vp += 1
        elif tup[0] == 'Sim' and tup[1] == 'Nao':
           fn += 1
        elif tup[0] == 'Nao' and tup[1] == 'Sim':
           fp += 1
        else:
           vn += 1
    precision = prec(vp, fp)
    recall = rec(vp, fn)

    return (1 + beta**2) * ((precision * recall) / ((beta**2 * precision) + recall))