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

#    dt.print_tree(fullDecisionTree)

    return fullDecisionTree

def bootstrap_tree(validation_data,fixedSeed):
    training_set = bs.generateTrainingSet(validation_data, fixedSeed)
    test_set = bs.generateTestSet(validation_data, training_set)
    return  training_set, test_set

# uncomment to test CrossValidation
if __name__ == '__main__':
    #validation_data, attribute_matrix = CsvReader.read_csv(arquivo)
    #decision_tree = full_tree(validation_data, attribute_matrix)

    arquivo = "dadosBenchmark_validacaoAlgoritmoAD.csv"
    #arquivo = "vertebra.csv"
    #arquivo = "dataset_191_wine-1.csv"
    #arquivo = "dataset_31_credit-g.csv"
    data, attribute_matrix = CsvReader.read_csv(arquivo)
    # decision_tree = full_tree(data, attribute_matrix)

    cs.run(data, attribute_matrix)
