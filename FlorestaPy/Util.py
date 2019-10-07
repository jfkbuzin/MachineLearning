import math
import numpy as np
import DecisionTree as dt

def get_classes(attribute_matrix):
    for atributo in attribute_matrix:
        if atributo[0] == "Class":
            tipos_classificacao = atributo[1]
            break
    return tipos_classificacao

def log2(x):
    return math.log(x) / math.log(2)

def get_class_attribute_index(attribute_matrix):
    cont = 0
    for att in attribute_matrix:
        if att[0] == "Class":
            return cont
        cont += 1

def get_m(attribute_matrix):
    size = len(attribute_matrix) - 1
    return math.sqrt(size)

def prec(vp, fp):
    if vp + fp != 0:
        return  vp / (vp + fp)
    else:
        return 0.0

def rev(vp, fn):
    if vp + fn != 0:
        return  vp / (vp + fn)
    else:
        return 0.0

def f1_score(precision, recall):
    beta = 1
    if precision == 0.0 and recall == 0.0:
        return 0.0
    return (1 + beta**2) * ((precision * recall) / ((beta**2 * precision) + recall))

# performance_binary: compute the performance of predictions
# parameters:
# - list_tuples: array of tuples
# - classes: array of possible classes (the first must be the positive one)
# returns a tuple with three values: (precision, recall, f1Score)
# return example:
# (0.833, 0.555, 0.666)
def performance_binary(list_tuples, classes):
    if len(list_tuples) == 0 or len(classes) > 2:
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
    f = f1_score(precision, recall)

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
        f = f1_score(precision, recall)
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

def evaluate_tree(decisionTree, test_set, all_classes):
    print("Evaluating Tree")
    list_tuples = []
    for t in range(len(test_set)):
        string = dt.evaluate_data(test_set[t], decisionTree)
        if string is None:
            print("test #" + str(t) + " result: Unable to evaluate data, too much repetition on training set")
        else:
            print("test #" + str(t) + " result: " + "(Verdadeiro / Classificado) (" + test_set[t]["Class"] + " / " + string + ")")
            tup = (test_set[t]["Class"], string)
            list_tuples.append(tup)
    
    if len(all_classes) == 2:
        precision, recall, f1 = performance_binary(list_tuples, all_classes)
        print("performance_binary:")
        print("precision:", str(precision))
        print("recall:", str(recall))
        print("f1:", str(f1))
    else:
        perf = performance_multiclass(list_tuples, all_classes)
        print("performance_multiclass:")
        print(perf)

def evaluate_forest(forest, test_set, all_classes):
    list_tuples = []
    for t in range(len(test_set)):
        string = dt.evaluate_forest(test_set[t], forest, all_classes)
        if string is None:
            pass
        else:
            tup = (test_set[t]["Class"], string)
            list_tuples.append(tup)

    pesos = {}
    str_resultado = "Votos :"
    for opcao in all_classes:
        pesos[opcao] = 0
        for t in list_tuples:
            if t[1] == opcao:
                pesos[opcao] += 1
        str_resultado += " | " + opcao + ": " + str(pesos[opcao])

    if len(all_classes) == 2:
        precision, recall, f1 = performance_binary(list_tuples, all_classes)
        return {
            "precision": precision,
            "recall": recall,
            "f1Score": f1,
        }
    else:
        perf = performance_multiclass(list_tuples, all_classes)
        return perf

def print_stats(stats, all_classes):
    print("\nSTATISTICS")
    if len(all_classes) <= 2:
        f1s = []
        for i in range(len(stats)):
            print("K =", i)
            print("precision =", stats[i]["precision"])
            print("recall =", stats[i]["recall"])
            print("F1 =", stats[i]["f1Score"])
            f1s.append(stats[i]["f1Score"])
            print("*******************************")
        print("Summary")
        print("F1 mean =", np.mean(f1s))
        print("F1 std =", np.std(f1s))
    else:
        f1s = {}
        for i in range(len(stats)):
            print("K =", i)
            for s in stats[i]:
                if type(stats[i][s]) == dict:
                    print("Class", s, "=", stats[i][s])
                    if s in f1s:
                        f1s[s].append(stats[i][s]["f1Score"])
                    else:
                        f1s[s] = [stats[i][s]["f1Score"]]
                else:
                    print(s, "=", stats[i][s])
            print("*******************************")
        print("Summary")
        for c in f1s:
            print("Class", c, "F1 mean =", np.mean(f1s[c]))
            print("Class", c, "F1 std =", np.std(f1s[c]))
        # print(f1s)

                