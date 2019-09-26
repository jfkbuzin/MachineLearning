import CsvReader
import DecisionTree as dt

if __name__ == '__main__':
    validation_data, attribute_list = CsvReader.read_csv()

    decisionTree = dt.DecisionTree()

    classes = []

    dt.select_node_id(classes, decisionTree, validation_data)
    dt.add_branch(decisionTree, validation_data)
    dt.split_examples(classes, decisionTree, validation_data)

    print("root attribute selected:" + decisionTree.node_id)
