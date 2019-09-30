import CsvReader
import DecisionTree as dt
import ValidationData as vd
import Bootstrap as bs
from collections import OrderedDict

def full_tree(validation_data, attribute_matrix):
    fullDecisionTree = dt.DecisionTree()

    classes = []

    dt.select_node_id(classes, fullDecisionTree, validation_data, attribute_matrix)
    dt.add_branch(fullDecisionTree, validation_data)
    dt.split_examples(classes, fullDecisionTree, validation_data, attribute_matrix)

    print("root attribute selected:" + fullDecisionTree.node_id)

    dt.print_tree(fullDecisionTree)

    test_data1 = OrderedDict()
    test_data1["Tempo"] = "Ensolarado"
    test_data1["Temperatura"] = "Quente"
    test_data1["Umidade"] = "Normal"
    test_data1["Ventoso"] = "Verdadeiro"
    test_data1["Joga"] = "?"

    test_data2 = OrderedDict()
    test_data2["Tempo"] = "Chuvoso"
    test_data2["Temperatura"] = "Quente"
    test_data2["Umidade"] = "Normal"
    test_data2["Ventoso"] = "Verdadeiro"
    test_data2["Joga"] = "?"

    string1 = dt.evaluateData(test_data1, fullDecisionTree)
    print("test1:" + string1)

    string2 = dt.evaluateData(test_data2, fullDecisionTree)
    print("test2:" + string2)

    return fullDecisionTree

def bootstrap_tree(validation_data,fixedSeed):
    training_set = bs.generateTrainingSet(validation_data,fixedSeed)
    test_set = bs.generateTestSet(validation_data, training_set)
    return  training_set, test_set

if __name__ == '__main__':
    print("oi")
    validation_data, attribute_matrix = CsvReader.read_csv()
    decision_tree = full_tree(validation_data, attribute_matrix)

    vertebra_data, attribute_matrix_vertebra = CsvReader.read_csv_numeral()
    #decision_tree = full_tree(vertebra_data, attribute_matrix_vertebra)

    forest = 5
    fixedSeed = 0
    list_tuples = []
    forests = []
    seed = 7

    for i in range(1,forest+1):
        print("tree:" + str(i))
        training_set, test_set = bootstrap_tree(validation_data,fixedSeed)
        fixedSeed += len(validation_data)

        decisionTree = dt.DecisionTree()
        classes = []

        # m attributes are used
        reduced_matrix = vd.select_m_attributes(attribute_matrix, seed)
        seed += len(validation_data)

        dt.select_node_id(classes, decisionTree, training_set, reduced_matrix)
        dt.add_branch(decisionTree, training_set)
        dt.split_examples(classes, decisionTree, training_set, reduced_matrix)

        print("root attribute selected:" + decisionTree.node_id)

        dt.print_tree(decisionTree)
        forests.append(decisionTree)

        j = 1
        for test in test_set: #test_set:
            string = dt.evaluateData(test, decision_tree) #can return none!
            if string is None:
                print("unable to evaluate data, too much repetition on training set")
                tup = (test["Joga"],"failed")
            else:
                print("test result" + str(j) + ":" + string)
                tup = (test["Joga"],string)

            print(string)
            j += 1
            list_tuples.append(tup)

    dt.majority_vote(validation_data,forests,attribute_matrix)