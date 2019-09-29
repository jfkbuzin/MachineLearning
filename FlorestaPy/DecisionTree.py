from operator import attrgetter
import ValidationData


class AttributeGain:

    def __init__(self, attribute, gain):
        self.attribute = attribute
        self.gain = gain


class DecisionTree:

    def __init__(self, node_id, gain, paths, branches):
        self.node_id = node_id
        self.gain = gain
        self.paths = paths
        self.branches = branches

    def __init__(self):
        self.node_id = "NONE"
        self.gain = 0
        self.paths = []
        self.branches = []


def select_attribute(classes, decision_tree, validation_data, attribute_matrix):
    gain_list = []
    data_set_entropy = ValidationData.compute_data_set_entropy(validation_data)

    for attribute_line in attribute_matrix:

        if attribute_line[0] not in classes:
            if attribute_line[0] != "Joga":
                entropy_average = 0
                for option in attribute_line[1]:
                    entropy_average += ValidationData.compute_sub_set_entropy(validation_data,attribute_line[0], option)
                att = AttributeGain(attribute_line[0], (data_set_entropy - entropy_average))
                gain_list.append(att)

    if gain_list:
        selected = max(gain_list, key=attrgetter('gain'))
        decision_tree.gain = selected.gain

        print("Max Gain: " + str(decision_tree.gain))

        classes.append(selected.attribute)
        return selected.attribute

    #raise ValueError("Gain list is null")
    print("Gain list is null and all classes have been used, setting leaf as the most frequent value")
    return setAttributeByFrequency(validation_data)


def setAttributeByFrequency(validation_data):

    yes_size = 0
    no_size = 0

    for v in validation_data:
        if v["Joga"] == "Sim":
            yes_size += 1
        else:
            no_size += 1

    if yes_size >= no_size:
        return "Sim"
    else:
        return "Nao"

def select_node_id(classes, decision_tree, validation_data, attribute_matrix):
    decision_tree.node_id = select_attribute(classes, decision_tree, validation_data, attribute_matrix)
# 2. Estender a árvore, adicionando uma ramo para cada valor do atributo selecionado existente


def add_branch(decision_tree, validation_data):
    paths = []

    attribute = decision_tree.node_id

    for v in validation_data:
        paths.append(v[attribute])

    paths = list(dict.fromkeys(paths))
    decision_tree.paths = paths


# 3. Dividir os exemplos em partições (uma para cada ramo adicionado), conforme valor do atributo testado

def split_examples(classes, decision_tree, validation_data, attribute_matrix):
    branches = []
    for path in decision_tree.paths:
        new_validation_data = sub_data(decision_tree, path, validation_data)

        branch_decision_tree = DecisionTree()

        if len(new_validation_data) > 0:
            select_node_id(classes, branch_decision_tree, new_validation_data, attribute_matrix)
            add_branch(branch_decision_tree, new_validation_data)
            branches.append(branch_decision_tree)
            split_examples(classes, branch_decision_tree, new_validation_data,attribute_matrix)

        else:
            branch_decision_tree.node_id = select_leaf_id(decision_tree, path, validation_data)
            branches.append(branch_decision_tree)

    if len(branches) > 0:
        decision_tree.branches = branches


def sub_data(decision_tree, path, validation_data):
    new_validation_data = []
    attribute = decision_tree.node_id

    if ValidationData.is_pure_partition(validation_data,attribute,path):
        return new_validation_data
    for v in validation_data:
        if v[attribute] == path:
            new_validation_data.append(v)

    return new_validation_data


def select_leaf_id(decision_tree, path, validation_data):
    attribute = decision_tree.node_id

    for v in validation_data:
        if v[attribute] == path:
            return v[list(v.keys())[-1]]

# 4. Para cada partição de exemplos resultante, repetir passos 1 a 3

# print tree
def print_tree(decision_tree):

    string = "node id:" + decision_tree.node_id + ", node gain:" + str(decision_tree.gain)
    i = 0

    for path in decision_tree.paths:
        i = i + 1
        string = string + ", path" + str(i) + ":" + path

    print(string)

    for node in decision_tree.branches:
        print_tree(node)


# predizer classe a partir do dado de entrada percorrendo a árvore
def evaluateData(validation_data, decision_tree):
    attribute = decision_tree.node_id

    #is leaf
    if not decision_tree.paths:
        return decision_tree.node_id
    else:
        i = 0
        for path in decision_tree.paths:
            if validation_data[attribute] == path:
                return evaluateData(validation_data, decision_tree.branches[i])
            i = i + 1





