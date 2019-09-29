import ValidationData
import random
from collections import OrderedDict

def bootstrap(validation_data, training_set, test_set):
    training_set = generateTraniningSet(validation_data)
    test_set = generateTestSet(validation_data, training_set)

#gerar conjunto de treinamento com reposição
def generateTrainingSet(validation_data):
    training_set = []

    for i in validation_data:
        training_set.append(random.choice(validation_data))

    return training_set

#gerar lista com dados que não se encontram no conjunto de treinamento
def generateTestSet(validation_data, training_set):

    test_set = []
    for reg in validation_data:
        if reg not in training_set:
            test_set.append(reg)
    return test_set