import random

random.seed(a=1)

#gerar conjunto de treinamento com reposição
def generate_training_set(validation_data,fixedSeed):
    training_set = []

    for i in validation_data:
        random.seed(fixedSeed)
        training_set.append(random.choice(validation_data))
        fixedSeed += 1

    return training_set

#gerar lista com dados que não se encontram no conjunto de treinamento
def generate_test_set(validation_data, training_set):
    test_set = []
    for reg in validation_data:
        if reg not in training_set:
            test_set.append(reg)
    return test_set
