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


def select_attribute(classes, decision_tree, validation_data):
    gain_list = []
    data_set_entropy = ValidationData.compute_data_set_entropy(validation_data)
    entropy_average = 0

    if "Tempo" not in classes:
        entropy_average = ValidationData.compute_sub_set_entropy(validation_data, "Tempo", "Ensolarado") \
                          + ValidationData.compute_sub_set_entropy(validation_data, "Tempo", "Nublado") \
                          + ValidationData.compute_sub_set_entropy(validation_data, "Tempo", "Chuvoso")

        att = AttributeGain("Tempo", (data_set_entropy - entropy_average))
        gain_list.append(att)

    if "Temperatura" not in classes:
        entropy_average = ValidationData.compute_sub_set_entropy(validation_data, "Temperatura", "Quente") \
                          + ValidationData.compute_sub_set_entropy(validation_data, "Temperatura", "Fria") \
                          + ValidationData.compute_sub_set_entropy(validation_data, "Temperatura", "Amena")

        att = AttributeGain("Temperatura", data_set_entropy - entropy_average)
        gain_list.append(att)

    if "Umidade" not in classes:
        entropy_average = ValidationData.compute_sub_set_entropy(validation_data, "Umidade", "Alta") \
                          + ValidationData.compute_sub_set_entropy(validation_data, "Umidade", "Normal")

        att = AttributeGain("Umidade", data_set_entropy - entropy_average)
        gain_list.append(att)

    if "Ventoso" not in classes:
        entropy_average = ValidationData.compute_sub_set_entropy(validation_data, "Ventoso", "Falso") \
                          + ValidationData.compute_sub_set_entropy(validation_data, "Ventoso", "Verdadeiro")

        att = AttributeGain("Ventoso", data_set_entropy - entropy_average)
        gain_list.append(att)

    if len(gain_list) != 0:
        selected = max(gain_list, key=attrgetter('gain'))
        decision_tree.gain = selected.gain

        print("Max Gain: " + str(decision_tree.gain))

        if decision_tree.gain == 0:
            return "purePartition"

        classes.append(selected.attribute)
        return selected.attribute

    return None


def select_node_id(classes, decision_tree, validation_data):
    decision_tree.node_id = select_attribute(classes, decision_tree, validation_data)


# 2. Estender a árvore, adicionando uma ramo para cada valor do atributo selecionado existente

def add_branch(decision_tree, validation_data):
    paths = []

    attribute = decision_tree.node_id

    if attribute == "Tempo":
        for v in validation_data:
            paths.append(v.tempo)
    elif attribute == "Temperatura":
        for v in validation_data:
            paths.append(v.temperatura)
    elif attribute == "Umidade":
        for v in validation_data:
            paths.append(v.umidade)
    elif attribute == "Ventoso":
        for v in validation_data:
            paths.append(v.ventoso)

    paths = list(dict.fromkeys(paths))
    decision_tree.paths = paths


# 3. Dividir os exemplos em partições (uma para cada ramo adicionado), conforme valor do atributo testado

def split_examples(classes, decision_tree, validation_data):
    branches = []
    for path in decision_tree.paths:
        new_validation_data = sub_data(decision_tree, path, validation_data)

        branch_decision_tree = DecisionTree()

        if len(new_validation_data) > 0:
            select_node_id(classes, branch_decision_tree, new_validation_data)
            add_branch(branch_decision_tree, new_validation_data)
            branches.append(branch_decision_tree)
            split_examples(classes, branch_decision_tree, new_validation_data)

        else:
            branch_decision_tree.node_id = select_leaf_id(decision_tree, path, validation_data)
            branches.append(branch_decision_tree)

    if len(branches) > 0:
        decision_tree.branches = branches


def sub_data(decision_tree, path, validation_data):
    new_validation_data = []
    attribute = decision_tree.node_id

    if attribute == "Tempo":

        if ValidationData.is_pure_partition(validation_data, "Tempo", path):
            return new_validation_data
        for v in validation_data:
            if v.tempo == path:
                new_validation_data.append(v)

    if attribute == "Temperatura":

        if ValidationData.is_pure_partition(validation_data, "Temperatura", path):
            return new_validation_data
        for v in validation_data:
            if v.temperatura == path:
                new_validation_data.append(v)

    if attribute == "Umidade":

        if ValidationData.is_pure_partition(validation_data, "Umidade", path):
            return new_validation_data
        for v in validation_data:
            if v.umidade == path:
                new_validation_data.append(v)

    if attribute == "Ventoso":

        if ValidationData.is_pure_partition(validation_data, "Ventoso", path):
            return new_validation_data
        for v in validation_data:
            if v.ventoso == path:
                new_validation_data.append(v)

    return new_validation_data


def select_leaf_id(decision_tree, path, validation_data):
    attribute = decision_tree.node_id

    if attribute == "Tempo":
        for v in validation_data:
            if v.tempo == path:
                return v.joga

    if attribute == "Temperatura":
        for v in validation_data:
            if v.temperatura == path:
                return v.joga

    if attribute == "Umidade":
        for v in validation_data:
            if v.umidade == path:
                return v.joga

    if attribute == "Ventoso":
        for v in validation_data:
            if v.ventoso == path:
                return v.joga


# 4. Para cada partição de exemplos resultante, repetir passos 1 a 3

# print tree
def print_tree(decision_tree):

    if decision_tree.gain is not None:
        string = "node id:" + decision_tree.node_id + ", node gain:" + str(decision_tree.gain)
    else:
        string = "leaf id:" + decision_tree.node_id
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
        if attribute == "Tempo":
            i = 0
            for path in decision_tree.paths:
                if validation_data.tempo == path:
                    return evaluateData(validation_data, decision_tree.branches[i])
                i = i + 1

        if attribute == "Temperatura":
            i = 0
            for path in decision_tree.paths:
                if validation_data.temperatura == path:
                    return evaluateData(validation_data, decision_tree.branches[i])
                i = i + 1

        if attribute == "Umidade":
            i = 0
            for path in decision_tree.paths:
                if validation_data.umidade == path:
                    return evaluateData(validation_data, decision_tree.branches[i])
                i = i + 1

        if attribute == "Ventoso":
            i = 0
            for path in decision_tree.paths:
                if validation_data.ventoso == path:
                    return evaluateData(validation_data, decision_tree.branches[i])
                i = i + 1





