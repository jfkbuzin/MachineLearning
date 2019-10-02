import CsvReader
import DecisionTree as dt
import ValidationData as vd
import Bootstrap as bs
import CrossValidation as cs
import Util as ut
from collections import OrderedDict

def full_tree(validation_data, attribute_matrix):
    fullDecisionTree = dt.DecisionTree()

    classes = []

    dt.select_node_id(classes, fullDecisionTree, validation_data, attribute_matrix)
    dt.add_branch(fullDecisionTree, validation_data, attribute_matrix)
    dt.split_examples(classes, fullDecisionTree, validation_data, attribute_matrix)

    print("root attribute selected:" + fullDecisionTree.node_id)

    # dt.print_tree(fullDecisionTree)

    return fullDecisionTree

def bootstrap_tree(validation_data,fixedSeed):
    training_set = bs.generateTrainingSet(validation_data, fixedSeed)
    test_set = bs.generateTestSet(validation_data, training_set)
    return  training_set, test_set

# if __name__ == '__main__':
#     print("oi")

#     #arquivo = "dataset_31_credit-g.csv"
#     #arquivo = "dataset_191_wine-1.csv"
#     #arquivo = "vertebra.csv"
#     arquivo = "dadosBenchmark_validacaoAlgoritmoAD.csv"

#     validation_data, attribute_matrix = CsvReader.read_csv(arquivo)
#     decision_tree = full_tree(validation_data, attribute_matrix)

#     vertebra_data, attribute_matrix_vertebra = CsvReader.read_csv_numeral()
#     vertebra_decision_tree = full_tree(vertebra_data, attribute_matrix_vertebra)

#     forest = 5
#     fixedSeed = 0
#     list_tuples = []
#     forests = []
#     seed = 7

#     for i in range(1,forest+1):
#         print("tree:" + str(i))
#         training_set, test_set = bootstrap_tree(validation_data,fixedSeed)
#         fixedSeed += len(validation_data)

#         decisionTree = dt.DecisionTree()
#         classes = []

#         # m attributes are used
#         reduced_matrix = vd.select_m_attributes(attribute_matrix, seed)
#         seed += len(validation_data)

#         dt.select_node_id(classes, decisionTree, training_set, reduced_matrix)
#         dt.add_branch(decisionTree, training_set,reduced_matrix)
#         dt.split_examples(classes, decisionTree, training_set, reduced_matrix)

#         print("root attribute selected:" + decisionTree.node_id)

#         # dt.print_tree(decisionTree)
#         forests.append(decisionTree)

#         opcoes_atributo_objetivo = ut.get_classes(attribute_matrix)
#         atributo_objetivo = "Class"

#         j = 1
#         for test in test_set: #test_set:
#             string = dt.evaluateData(test, decisionTree) #can return none!
#             if string is None:
#                 print("unable to evaluate data, too much repetition on training set")
#                 tup = (test[atributo_objetivo], "failed")
#             else:
#                 print("test #" + str(j) + " result: " + "(Verdadeiro / Classificado) (" + test[atributo_objetivo] + " / " + string + ")")
#                 tup = (test[atributo_objetivo], string)

#             j += 1
#             list_tuples.append(tup)
        
#         precision, recall, f1 = ut.performance_binary(list_tuples, opcoes_atributo_objetivo)
#         print("precision:", str(precision))
#         print("recall:", str(recall))
#         print("f1:", str(f1))

#     dt.majority_vote(validation_data,forests,attribute_matrix)

# uncomment to test CrossValidation
if __name__ == '__main__':
    arquivo = "dadosBenchmark_validacaoAlgoritmoAD.csv"
    validation_data, attribute_matrix = CsvReader.read_csv(arquivo)
    cs.run(validation_data, attribute_matrix)
