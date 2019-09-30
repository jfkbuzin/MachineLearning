import Util
import numpy as np
import random

#Nao esta generico. Nao esta adaptado para 3 respostas
def compute_data_set_entropy(validation_data, attribute_matrix):
    example_size = len(validation_data)

    tipos_classificacao = attribute_matrix[-1][1]

    dict_sizes = {}
    for opcao in tipos_classificacao:
        dict_sizes[opcao] = 0

    for v in validation_data:
        atributo_interesse = v[list(v.keys())[-1]]
        dict_sizes[atributo_interesse] = dict_sizes[atributo_interesse] + 1


    d_list = []
    for opcao in tipos_classificacao:
        d_atual = dict_sizes[opcao] / example_size
        d_list.append(d_atual)

    info = 0
    for d_atual in d_list:
        info += -d_atual * Util.log2(d_atual)

    #info = -d1 * Util.log2(d1) - d2 * Util.log2(d2)

    print("data set info: " + str(info))
    return info


def compute_sub_set_entropy(validation_data, attribute, example, attribute_matrix):

    tipos_classificacao = attribute_matrix[-1][1]

    sizes = [0.0] + [0.0] * len(tipos_classificacao)
    set_sizes(validation_data, attribute, example, sizes, tipos_classificacao)

    info = 0

    for i in range(1,len(sizes)):
        if sizes[i] > 0 and sizes[0] > 0:
            d1 = sizes[i] / sizes[0]
            info = info - d1 * Util.log2(d1)

    print("subset info: " + str(info))

    # passar já o valor para calcular a média

    if sizes[0] > 0:
        return (sizes[0] / len(validation_data)) * info

    return 0


def set_sizes(validation_data, attribute, example, sizes, tipos_classificacao):

    present_attribute = None

    for v in validation_data:
        present_attribute = v[attribute]

        if present_attribute == example:
            sizes[0] += 1 # quantidade de registros
            classificacao_registro_atual = v[list(v.keys())[-1]]

            for classificacao_possivel in tipos_classificacao:
                if classificacao_registro_atual == classificacao_possivel:
                    posicao = tipos_classificacao.index(classificacao_registro_atual) + 1
                    sizes[posicao] += 1


def is_pure_partition(validation_data, attribute, example, attribute_matrix):
    tipos_classificacao = attribute_matrix[-1][1]
    sizes = [0.0] + [0.0] * len(tipos_classificacao)
    set_sizes(validation_data, attribute, example, sizes, tipos_classificacao)

    classes_presentes = 0
    for i in range(1,len(sizes)):
        if sizes[i] > 0:
            classes_presentes += 1


    if classes_presentes == 1:
        return True
    else:
        return False


def select_m_attributes(attribute_matrix,seed):

    m_attribute_matrix = []
    m_attributes = []
    m = Util.get_m(attribute_matrix)

    while m != 0:
        random.seed(seed)
        seed += 1
        x = random.randint(0, len(attribute_matrix) - 2)
        if x in m_attributes:
            continue
        else:
            m_attributes.append(x)
            m_attribute_matrix.append(attribute_matrix[x])
            m -= 1

    #must add joga in the end
    m_attribute_matrix.append(attribute_matrix[len(attribute_matrix) - 1])
    return m_attribute_matrix