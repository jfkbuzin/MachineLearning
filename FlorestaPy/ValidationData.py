import Util


class ValidationData:

    def __init__(self, tempo, temperatura, umidade, ventoso, joga):
        self.tempo = tempo
        self.temperatura = temperatura
        self.umidade = umidade
        self.ventoso = ventoso
        self.joga = joga

    def print_data(self):
        string = str(self.tempo) + "|" + str(self.temperatura) + "|" + str(self.umidade) + "|" \
               + str(self.ventoso) + "|" + str(self.joga)
        print(string)


def compute_data_set_entropy(validation_data):
    example_size = len(validation_data)
    yes_size = 0
    no_size = 0
    print(validation_data)
    for v in validation_data:
        if v.joga == "Sim":
            yes_size += 1
        else:
            no_size += 1

    d1 = yes_size / example_size
    d2 = no_size / example_size

    info = -d1 * Util.log2(d1) - d2 * Util.log2(d2)

    print("info: " + str(info))
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

    print("info: " + str(info))

    # passar já o valor para calcular a média

    if sizes[0] > 0:
        return (sizes[0] / len(validation_data)) * info

    return 0


def set_sizes(validation_data, attribute, example, sizes):

    present_attribute = None

    for v in validation_data:

        if attribute == "Tempo":
            present_attribute = v.tempo
        if attribute == "Temperatura":
            present_attribute = v.temperatura
        if attribute == "Umidade":
            present_attribute = v.umidade
        if attribute == "Ventoso":
            present_attribute = v.ventoso

        if present_attribute == example:
            sizes[0] += 1

        if present_attribute == example and v.joga == "Sim":
            sizes[1] += 1

        if present_attribute == example and v.joga == "Nao":
            sizes[2] += 1


def is_pure_partition(validation_data, attribute, example):
    sizes = [0.0, 0.0, 0.0]

    set_sizes(validation_data, attribute, example, sizes)

    if (sizes[1] > 0 and sizes[2] == 0) or (sizes[1] == 0 and sizes[2] > 0):
        return True
    else:
        return False
