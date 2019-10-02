import DecisionTree as dt
import ValidationData as vd
import Bootstrap as bs
import CrossValidation as cs
import Util as ut
from collections import OrderedDict

def generateTrainingSet(validation_data, K, i):
    partition_size = round(len(validation_data)/K)
    training_set = validation_data.copy()
    del training_set[i*partition_size:(i+1)*partition_size]
    return training_set

def generateTestSet(validation_data, K, i):
    partition_size = round(len(validation_data)/K)
    test_set = validation_data.copy()[i*partition_size:(i+1)*partition_size]
    return test_set

def run(validation_data, attribute_matrix):
    ntree = 20
    fixedSeed = 0
    seed = 7
    K = 5


    for i in range(K):
        forest = []
        print("K = " + str(i))
        # generate cross validation training (K-1) and evaluation (1) partitions
        training = generateTrainingSet(validation_data, K, i)
        evaluation = generateTestSet(validation_data, K, i)

        # run bootstrap and create each decision tree of forest
        for t in range(ntree):
            training_set = bs.generateTrainingSet(training, fixedSeed)
            test_set = bs.generateTestSet(training, training_set)
            fixedSeed += len(validation_data)

            decisionTree = dt.DecisionTree()
            classes = []

            # m attributes are used
            reduced_matrix = vd.select_m_attributes(attribute_matrix, seed)
            seed += len(validation_data)

            dt.select_node_id(classes, decisionTree, training_set, reduced_matrix)
            dt.add_branch(decisionTree, training_set,reduced_matrix)
            dt.split_examples(classes, decisionTree, training_set, reduced_matrix)

            print("root attribute selected:" + decisionTree.node_id)

            # dt.print_tree(decisionTree)
            forest.append(decisionTree)

            all_classes = ut.get_classes(attribute_matrix)
            ut.evaluateTree(decisionTree, test_set, all_classes)

        # dt.majority_vote(validation_data, forest, attribute_matrix)
        ut.evaluateForest(forest, evaluation, all_classes)