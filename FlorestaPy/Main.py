import CsvReader
import DecisionTree as dt
import ValidationData as vd
import Bootstrap as bs

def full_tree(validation_data):
    fullDecisionTree = dt.DecisionTree()

    classes = []

    dt.select_node_id(classes, fullDecisionTree, validation_data)
    dt.add_branch(fullDecisionTree, validation_data)
    dt.split_examples(classes, fullDecisionTree, validation_data)

    print("root attribute selected:" + fullDecisionTree.node_id)

    dt.print_tree(fullDecisionTree)

    test_data1 = vd.ValidationData("Ensolarado", "Quente", "Normal", "Verdadeiro", "?")  # resposta é Sim
    test_data2 = vd.ValidationData("Chuvoso", "Quente", "Normal", "Verdadeiro", "?")  # resposta é Nao

    string1 = dt.evaluateData(test_data1, fullDecisionTree)
    print("test1:" + string1)

    string2 = dt.evaluateData(test_data2, fullDecisionTree)
    print("test2:" + string2)

def bootstrap_tree(validation_data):
    training_set = bs.generateTrainingSet(validation_data)
    test_set = bs.generateTestSet(validation_data, training_set)

    decisionTree = dt.DecisionTree()

    classes = []

    dt.select_node_id(classes, decisionTree, training_set)
    dt.add_branch(decisionTree, training_set)
    dt.split_examples(classes, decisionTree, training_set)

    print("root attribute selected:" + decisionTree.node_id)

    dt.print_tree(decisionTree)

    i = 1;
    for test in test_set:
        string = dt.evaluateData(test, decisionTree) #can return none!
        if string is None:
            print("unable to evaluate data, too much repetition on training set")

        else:
            print("test result" + str(i) + ":" + string)

        string = str(test.tempo) + "|" + str(test.temperatura) + "|" + str(test.umidade) + "|" \
                 + str(test.ventoso) + "|" + str(test.joga)
        print(string)
        i = i + 1

if __name__ == '__main__':
    validation_data, attribute_list = CsvReader.read_csv()

    full_tree(validation_data)

    forest = 50

    for i in range(1,forest+1):
        print("tree:" + str(i))
        bootstrap_tree(validation_data)

