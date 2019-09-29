import Util

#Nao esta generico. Nao esta adaptado para 3 respostas
def compute_data_set_entropy(validation_data):
    example_size = len(validation_data)

    yes_size = 0
    no_size = 0

    for v in validation_data:
        atributo_interesse = v[list(v.keys())[-1]]
        if atributo_interesse == "Sim": # Sim depois tem que ser pego do attribute_matrix
            yes_size += 1
        else:
            no_size += 1

    d1 = yes_size / example_size
    d2 = no_size / example_size

    info = -d1 * Util.log2(d1) - d2 * Util.log2(d2)

    print("data set info: " + str(info))
    return info


def compute_sub_set_entropy(validation_data, attribute, example):

    sizes = [0.0, 0.0, 0.0]
    set_sizes(validation_data, attribute, example, sizes)

    info = 0

    if sizes[1] > 0 and sizes[0] > 0:
        d1 = sizes[1] / sizes[0]
        info = info - d1 * Util.log2(d1)

    if sizes[2] > 0 and sizes[0] > 0:
        d2 = sizes[2] / sizes[0]
        info = info - d2 * Util.log2(d2)

    print("subset info: " + str(info))

    # passar já o valor para calcular a média

    if sizes[0] > 0:
        return (sizes[0] / len(validation_data)) * info

    return 0


def set_sizes(validation_data, attribute, example, sizes):

    present_attribute = None

    for v in validation_data:
        present_attribute = v[attribute]

        if present_attribute == example:
            sizes[0] += 1

        if present_attribute == example and v[list(v.keys())[-1]] == "Sim":
            sizes[1] += 1

        if present_attribute == example and v[list(v.keys())[-1]] == "Nao":
            sizes[2] += 1


def is_pure_partition(validation_data, attribute, example):
    sizes = [0.0, 0.0, 0.0]

    set_sizes(validation_data, attribute, example, sizes)

    if (sizes[1] > 0 and sizes[2] == 0) or (sizes[1] == 0 and sizes[2] > 0):
        return True
    else:
        return False
