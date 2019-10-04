import DecisionTree as dt
import ValidationData as vd
import Bootstrap as bs
import CrossValidation as cs
import Util as ut
from collections import OrderedDict

def generatePartitions(data, K):
    partitions = []
    ordered_data = sorted(data.copy(), key=lambda k: k['Class'])

    # generate partitions
    for p in range(K):
        partitions.append([])

    # populate partitions
    for i in range(len(ordered_data)):
        partitions[i % K].append(ordered_data[i])

    return partitions

def run(data, attribute_matrix):
    ntree = 20
    fixedSeed = 0
    seed = 7
    K = 5

    partitions = generatePartitions(data, K)

    for i in range(K):
        forest = []
        print("K = " + str(i))

        # generate cross validation training (K-1) and evaluation (1) partitions
        training = []
        for p in range(K):
            if p != i:
                training = training + partitions[p]
        evaluation = partitions[i]

        # run bootstrap and create each decision tree of forest
        for t in range(ntree):
            training_set = bs.generateTrainingSet(training, fixedSeed)
            test_set = bs.generateTestSet(training, training_set)
            fixedSeed += len(data)

            decisionTree = dt.DecisionTree()
            classes = []

            # m attributes are used
            reduced_matrix = vd.select_m_attributes(attribute_matrix)
            seed += len(data)

            dt.select_node_id(classes, decisionTree, training_set, reduced_matrix)
            dt.add_branch(decisionTree, training_set,reduced_matrix)
            dt.split_examples(classes, decisionTree, training_set, reduced_matrix)


            #print("root attribute selected:" + decisionTree.node_id)

            #dt.print_tree(decisionTree)
            forest.append(decisionTree)

            all_classes = ut.get_classes(attribute_matrix)
            #ut.evaluateTree(decisionTree, test_set, all_classes)

        ut.evaluateForest(forest, evaluation, all_classes)