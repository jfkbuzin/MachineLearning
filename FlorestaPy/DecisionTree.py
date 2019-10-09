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


def select_attribute(decision_tree, validation_data, attribute_matrix,is_full_tree):
    gain_list = []
    data_set_entropy = ValidationData.compute_data_set_entropy(validation_data, attribute_matrix)
    class_index = Util.get_class_attribute_index(attribute_matrix)

    if is_full_tree:
        reduced_matrix = attribute_matrix
    else:
        reduced_matrix = ValidationData.select_m_attributes(attribute_matrix)

    for attribute_line in reduced_matrix:
        if attribute_matrix.index(attribute_line) != class_index:
            #if attribute_line[0] not in classes:
            entropy_average = 0
            for option in attribute_line[1]:
                entropy_average += ValidationData.compute_sub_set_entropy(validation_data, attribute_line[0], option, attribute_matrix)
            att = AttributeGain(attribute_line[0], (data_set_entropy - entropy_average))
            gain_list.append(att)

    if gain_list:
        selected = max(gain_list, key=attrgetter('gain'))
        decision_tree.gain = selected.gain

       # print("Max Gain: " + str(decision_tree.gain))

        #classes.append(selected.attribute)
        return selected.attribute

    #print("Gain list is null and all classes have been used, setting leaf as the most frequent value")
    return set_attribute_by_frequency(validation_data,attribute_matrix)


def set_attribute_by_frequency(validation_data, attribute_matrix):
    atributo_objetivo = "Class"
    opcoes_objetivo = Util.get_classes(attribute_matrix)

    if not validation_data:
        print("Empty partition")

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

def select_node_id(decision_tree, validation_data, attribute_matrix,is_full_tree):
    decision_tree.node_id = select_attribute(decision_tree, validation_data, attribute_matrix,is_full_tree)

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
                attribute[1] = ["@< " + str(round(average, 3)), "@> " + str(round(average, 3))]
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
                                paths.append(att[1][0])
                                paths.append(att[1][1])
            except ValueError:
                paths.append(v[attribute])

    paths = list(dict.fromkeys(paths))
    decision_tree.paths = paths


# 3. Dividir os exemplos em partições (uma para cada ramo adicionado), conforme valor do atributo testado
# 4. Para cada partição de exemplos resultante, repetir passos 1 a 3
def split_examples(decision_tree, validation_data, attribute_matrix,is_full_tree):
    branches = []

    for path in decision_tree.paths:
        new_validation_data = sub_data(decision_tree, path, validation_data, attribute_matrix)
        branch_decision_tree = DecisionTree()

        if len(new_validation_data) > 0:
            new_attribute_matrix = attribute_matrix
            update_matrix_paths(new_attribute_matrix, new_validation_data)

            select_node_id(branch_decision_tree, new_validation_data, new_attribute_matrix,is_full_tree)
            add_branch(branch_decision_tree, new_validation_data,new_attribute_matrix)
            branches.append(branch_decision_tree)
            split_examples(branch_decision_tree, new_validation_data,new_attribute_matrix,is_full_tree)

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
            if "<" in path and "@" in path:
                splitString = path.split('< ')
                average = float(splitString[1])
                if x < average:
                    new_validation_data.append(v)

            if ">" in path and "@" in path:
                splitString = path.split('> ')
                average = float(splitString[1])
                if x >= average:
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
            if "<" in path and '@' in path:
                splitString = path.split('< ')
                average = float(splitString[1])
                if x < average:
                    return v["Class"]

            if ">" in path and '@' in path:
                splitString = path.split('> ')
                average = float(splitString[1])
                if x >= average:
                    return v["Class"]
        except ValueError:
            if v[attribute] == path:
                return v["Class"]

# print tree
def print_tree(decision_tree):
    if decision_tree is None or decision_tree.node_id is None or decision_tree.gain is None:
        return

    string = "node id:" + decision_tree.node_id + ", node gain:" + str(decision_tree.gain)
    i = 0

    for path in decision_tree.paths:
        i = i + 1
        string = string + ", path" + str(i) + ":" + path

    print(string)

    for node in decision_tree.branches:
        print_tree(node)


# predizer classe a partir do dado de entrada percorrendo a árvore
def evaluate_data(validation_data, decision_tree):
    attribute = decision_tree.node_id

    #is leaf
    if not decision_tree.paths:
        return decision_tree.node_id
    else:
        i = 0
        for path in decision_tree.paths:

            try:
                x = float(validation_data[attribute])
                if "<" in path and '@' in path:
                    splitString = path.split('< ')
                    average = float(splitString[1])
                    if x < average:
                        return evaluate_data(validation_data, decision_tree.branches[i])

                if ">" in path and '@' in path:
                    splitString = path.split('> ')
                    average = float(splitString[1])
                    if x >= average:
                        return evaluate_data(validation_data, decision_tree.branches[i])

            except ValueError:
                if validation_data[attribute] == path:
                    return evaluate_data(validation_data, decision_tree.branches[i])

            i = i + 1

def evaluate_forest(test_case, forest, all_classes):
    dict_sizes = {}

    for Class in all_classes:
        dict_sizes[Class] = 0

    for tree in forest:
        string = evaluate_data(test_case, tree)

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
        # print("Majority vote is inconclusive")
        return None
    else:
        # print("Majority vote is "+ prediction +", quantity: " + str(max_value))
        return prediction
