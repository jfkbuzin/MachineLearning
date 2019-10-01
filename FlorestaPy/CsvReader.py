import csv
from collections import OrderedDict
import ValidationData as vd

def read_csv(arquivo):
    with open(arquivo) as csvDataFile:
        validation_data = []
        csvReader = csv.reader(csvDataFile)
        cont = 0
        attribute_matrix = []
        for row in csvReader:
            if cont == 0:
                for i in range(len(row)):
                    if row[i] == "Joga" or row[i] == "class":
                        attribute_matrix.append(["Class", []])
                    else:
                        attribute_matrix.append([row[i], []])
                cont+=1
                continue
            dado_atual = OrderedDict()

            for i in range(len(row)):
                dado_atual[attribute_matrix[i][0]] = row[i]
                if row[i] not in attribute_matrix[i][1]:
                    attribute_matrix[i][1].append(row[i])

          #  print(dado_atual)
            validation_data.append(dado_atual)


        for attribute in attribute_matrix:
            try:
                x = float(attribute[1][0])
                attribute[1] = ["NUMERICO"]

            except ValueError:
                continue

        if arquivo == "dataset_31_credit-g.csv":
            attribute_matrix[-1][1] = ["good", "bad"]
        elif arquivo == "dataset_191_wine-1.csv":
            attribute_matrix[0][1] = ["1", "2", "3"]
        elif arquivo == "vertebra.csv":
            attribute_matrix[-1][1] = ["1", "2", "3"]
        else:
            attribute_matrix[-1][1] = ["Sim", "Nao"]

        print(attribute_matrix)

        return validation_data, attribute_matrix

def read_csv_numeral():
    with open('vertebra.csv') as csvDataFile:
        validation_data = []
        csvReader = csv.reader(csvDataFile)
        cont = 0
        attribute_matrix = []
        for row in csvReader:
            if cont == 0:
                for i in range(len(row)):
                    attribute_matrix.append([row[i], []])
                cont+=1
                continue
            dado_atual = OrderedDict()

            for i in range(len(row)):
                dado_atual[attribute_matrix[i][0]] = row[i]
                if row[i] not in attribute_matrix[i][1]:
                    attribute_matrix[i][1].append(row[i])

          #  print(dado_atual)
            validation_data.append(dado_atual)

        #calcular media para cada coluna

        for attribute in attribute_matrix:
            if attribute_matrix.index(attribute) != len(attribute_matrix) - 1:
                try:
                    x = float(attribute[1][0])
                    sum = 0
                    for att in attribute[1]:
                            sum += float(att)

                    length = len(attribute[1])
                    average = sum / length
                    attribute[1] = ["< " + str(round(average,3)), "> " + str(round(average,3))]
                except ValueError:
                    continue
       # print(attribute_matrix)
        return validation_data, attribute_matrix