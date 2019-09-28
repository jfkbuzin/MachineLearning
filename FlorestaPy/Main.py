import CsvReader
import DecisionTree as dt
import ValidationData as vd

if __name__ == '__main__':
    validation_data, attribute_list = CsvReader.read_csv()

    decisionTree = dt.DecisionTree()

    classes = []

    dt.select_node_id(classes, decisionTree, validation_data)
    dt.add_branch(decisionTree, validation_data)
    dt.split_examples(classes, decisionTree, validation_data)

    print("root attribute selected:" + decisionTree.node_id)

    dt.print_tree(decisionTree)

    test_data1 = vd.ValidationData("Ensolarado","Quente","Normal","Verdadeiro","?") # resposta é Sim
    test_data2 = vd.ValidationData("Chuvoso","Quente","Normal","Verdadeiro","?") # resposta é Nao

    string1 = dt.evaluateData(test_data1, decisionTree)
    print("test1:" + string1)

    string2 = dt.evaluateData(test_data2, decisionTree)
    print("test2:" + string2)


