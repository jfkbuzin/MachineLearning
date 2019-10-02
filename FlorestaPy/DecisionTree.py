from operator import attrgetter
import ValidationData
import Util

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
    data_set_entropy = ValidationData.compute_data_set_entropy(validation_data, attribute_matrix)
    class_index = Util.get_class_attribute_index(attribute_matrix)

    for attribute_line in attribute_matrix:
        if attribute_matrix.index(attribute_line) != class_index:
            if attribute_line[0] not in classes:
                entropy_average = 0
                for option in attribute_line[1]:
                    entropy_average += ValidationData.compute_sub_set_entropy(validation_data, attribute_line[0], option, attribute_matrix)
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
    return set_attribute_by_frequency(validation_data,attribute_matrix)


def set_attribute_by_frequency(validation_data, attribute_matrix):
    atributo_objetivo = "Class"
    opcoes_objetivo = Util.get_classes(attribute_matrix)

    dict_sizes = {}
    for opcao in opcoes_objetivo:
        dict_sizes[opcao] = 0

    for v in validation_data:
        for opcao_atual in opcoes_objetivo:
            if v[atributo_objetivo] == opcao_atual:
                dict_sizes[opcao_atual] += 1

    str_maximo = ""
    max_value = 0

    for opcao in opcoes_objetivo:
        if dict_sizes[opcao] >= max_value:
            str_maximo = opcao
            max_value = dict_sizes[opcao]

    return str_maximo

def select_node_id(classes, decision_tree, validation_data, attribute_matrix):
    decision_tree.node_id = select_attribute(classes, decision_tree, validation_data, attribute_matrix)

def update_matrix_paths(attribute_matrix, validation_data):
    for attribute in attribute_matrix:
        string1 = attribute[0]
        try:
            x = float(validation_data[0][string1])
            class_index = Util.get_class_attribute_index(attribute_matrix)
            if attribute_matrix.index(attribute) != class_index:
                sum = 0
                for v in validation_data:
                    sum += float(v[string1])

                length = len(validation_data)
                average = sum / length
                attribute[1] = ["< " + str(round(average, 3)), "> " + str(round(average, 3))]
        except ValueError:
            continue

# 2. Estender a árvore, adicionando uma ramo para cada valor do atributo selecionado existente
def add_branch(decision_tree, validation_data,attribute_matrix):
    paths = []
    attribute = decision_tree.node_id

    for v in validation_data:
        if attribute in v.keys(): # para evitar que tente encontrar paths pra folha
            try:
                x = float(v[attribute])
                class_index = Util.get_class_attribute_index(attribute_matrix)
                while not paths:
                    for att in attribute_matrix:
                        if attribute_matrix.index(att) != class_index:
                            if att[0] == attribute:
                                print(att)
                                paths.append(att[1][0])
                                paths.append(att[1][1])
            except ValueError:
                paths.append(v[attribute])

    paths = list(dict.fromkeys(paths))
    decision_tree.paths = paths


# 3. Dividir os exemplos em partições (uma para cada ramo adicionado), conforme valor do atributo testado
# 4. Para cada partição de exemplos resultante, repetir passos 1 a 3
def split_examples(classes, decision_tree, validation_data, attribute_matrix):
    branches = []

    for path in decision_tree.paths:
        new_validation_data = sub_data(decision_tree, path, validation_data, attribute_matrix)
        branch_decision_tree = DecisionTree()

        if len(new_validation_data) > 0:
            new_attribute_matrix = attribute_matrix
            update_matrix_paths(new_attribute_matrix, new_validation_data)

            select_node_id(classes, branch_decision_tree, new_validation_data, attribute_matrix)
            add_branch(branch_decision_tree, new_validation_data,attribute_matrix)
            branches.append(branch_decision_tree)
            split_examples(classes, branch_decision_tree, new_validation_data,attribute_matrix)

        else:
            branch_decision_tree.node_id = select_leaf_id(decision_tree, path, validation_data)
            branches.append(branch_decision_tree)

    if len(branches) > 0:
        decision_tree.branches = branches


def sub_data(decision_tree, path, validation_data, attribute_matrix):
    new_validation_data = []
    attribute = decision_tree.node_id

    if ValidationData.is_pure_partition(validation_data,attribute,path,attribute_matrix):
        return new_validation_data
    for v in validation_data:
        try:
            x = float(v[attribute])
            if "<" in path:
                splitString = path.split('< ')
                average = float(splitString[1])
                if x < average:
                    new_validation_data.append(v)

            if ">" in path:
                splitString = path.split('> ')
                average = float(splitString[1])
                if x > average:
                    new_validation_data.append(v)
        except ValueError:
            if v[attribute] == path:
                new_validation_data.append(v)

    return new_validation_data


def select_leaf_id(decision_tree, path, validation_data):
    attribute = decision_tree.node_id

    for v in validation_data:
        try:
            x = float(v[attribute])
            if "<" in path:
                splitString = path.split('< ')
                average = float(splitString[1])
                if x < average:
                    return v["Class"]

            if ">" in path:
                splitString = path.split('> ')
                average = float(splitString[1])
                if x > average:
                    return v["Class"]
        except ValueError:
            if v[attribute] == path:
                return v["Class"]

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

            try:
                x = float(validation_data[attribute])
                if "<" in path:
                    splitString = path.split('< ')
                    average = float(splitString[1])
                    if x < average:
                        return evaluateData(validation_data, decision_tree.branches[i])

                if ">" in path:
                    splitString = path.split('> ')
                    average = float(splitString[1])
                    if x > average:
                        return evaluateData(validation_data, decision_tree.branches[i])

            except ValueError:
                if validation_data[attribute] == path:
                    return evaluateData(validation_data, decision_tree.branches[i])

            i = i + 1

def majority_vote(validation_data, forest,attribute_matrix):
    case = 1

    opcoes_objetivo = Util.get_classes(attribute_matrix)

    for data in validation_data:
        dict_sizes = {}
        for opcao in opcoes_objetivo:
            dict_sizes[opcao] = 0

        for tree in forest:
            string = evaluateData(data, tree)

            for opcao_atual in opcoes_objetivo:
                if string == opcao_atual:
                    dict_sizes[opcao_atual] += 1

            str_maximo = ""
            max_value = 0

            for opcao in opcoes_objetivo:
                if dict_sizes[opcao] >= max_value:
                    str_maximo = opcao
                    max_value = dict_sizes[opcao]

            draw_count = 0
            for opcao in opcoes_objetivo:
                if dict_sizes[opcao] == max_value:
                    draw_count += 1

        if draw_count != 1:
            print("Case:" + str(case) + " Majority vote is inconclusive")
        else:
            print("Case:" + str(case) + " Majority vote is "+ str_maximo +", quantity:" + str(max_value))

        case += 1

def evaluateForest(test_case, forest, all_classes):
    dict_sizes = {}

    for Class in all_classes:
        dict_sizes[Class] = 0

    for tree in forest:
        string = evaluateData(test_case, tree)

        for Class_actual in all_classes:
            if string == Class_actual:
                dict_sizes[Class_actual] += 1

        prediction = ""
        max_value = 0

        for Class in all_classes:
            if dict_sizes[Class] >= max_value:
                prediction = Class
                max_value = dict_sizes[Class]

        draw_count = 0
        for Class in all_classes:
            if dict_sizes[Class] == max_value:
                draw_count += 1

    if draw_count != 1:
        print("Majority vote is inconclusive")
        return None
    else:
        print("Majority vote is "+ prediction +", quantity: " + str(max_value))
        return prediction
