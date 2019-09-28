import ValidationData
import random

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
    return list(set(validation_data) - set(training_set))
