import math
import numpy as np

def retorna_opcoes_classe(attribute_matrix):
    for atributo in attribute_matrix:
        if atributo[0] == "Class":
            tipos_classificacao = atributo[1]
            break
    return tipos_classificacao

def log2(x):
    return math.log(x) / math.log(2)

def get_m(attribute_matrix):
    size = len(attribute_matrix) - 1
    return math.sqrt(size)

def prec(vp, fp):
    return  vp / (vp + fp)

def rev(vp, fn):
    return  vp / (vp + fn)

def f1Score(precision, recall):
    beta = 1
    return (1 + beta**2) * ((precision * recall) / ((beta**2 * precision) + recall))

# performance_binary: compute the performance of predictions
# parameters:
# - list_tuples: array of tuples
# - classes: array of possible classes (the first must be the positive one)
# returns a tuple with three values: (precision, recall, f1Score)
# return example:
# (0.833, 0.555, 0.666)
def performance_binary(list_tuples, classes):
    if len(classes) > 2:
        return 0, 0, 0

    confusion_matrix = np.zeros((len(classes), len(classes)), dtype=np.int32)

    for tup in list_tuples:
        truth_index = classes.index(tup[0])
        predicted_index = classes.index(tup[1])
        confusion_matrix[truth_index][predicted_index] += 1

    VP = confusion_matrix[0][0]
    FP = confusion_matrix[1][0]
    FN = confusion_matrix[0][1]
    precision = prec(VP, FP)
    recall = rev(VP, FN)
    f = f1Score(precision, recall)

    return precision, recall, f

# performance_multiclass: compute the performance of predictions
# parameters:
# - list_tuples: array of tuples
# - classes: array of possible classes
# returns a dictionary with all classes and metrics
# return example: {
#   'c1': { 'precision': 0.785, 'recall': 0.733, 'f1Score': 0.758 },
#   'c2': { 'precision': 0.571, 'recall': 0.800, 'f1Score': 0.666 },
#   'c3': { 'precision': 0.666, 'recall': 0.600, 'f1Score': 0.631 },
#   'macro': 0.674,
#   'micro': 0.700,
# }
def performance_multiclass(list_tuples, classes):
    if len(classes) <= 2:
        return {}

    confusion_matrix = np.zeros((len(classes), len(classes)), dtype=np.int32)
    performance_dict = {}

    for tup in list_tuples:
        truth_index = classes.index(tup[0])
        predicted_index = classes.index(tup[1])
        confusion_matrix[truth_index][predicted_index] += 1

    VP = np.zeros(len(classes), dtype=int)
    FP = np.zeros(len(classes), dtype=int)
    FN = np.zeros(len(classes), dtype=int)
    for c in range(len(classes)):
        VP[c] += confusion_matrix[c][c]
        for i in range(len(classes)):
            if i != c:
                FP[c] += confusion_matrix[i][c]
                FN[c] += confusion_matrix[c][i]
        precision = prec(VP[c], FP[c])
        recall = rev(VP[c], FN[c])
        f = f1Score(precision, recall)
        performance_dict[classes[c]] = {
            "precision": precision,
            "recall": recall,
            "f1Score": f 
        }
    
    precision_sum = 0
    for item in performance_dict:
        precision_sum += performance_dict[item]["precision"]
    performance_dict["macro"] = precision_sum/len(classes)
    performance_dict["micro"] = np.sum(VP) / (np.sum(VP) + np.sum(FP))
    return performance_dict