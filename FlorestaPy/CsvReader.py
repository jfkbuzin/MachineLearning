import csv
from collections import OrderedDict
import ValidationData as vd

def read_csv():
    with open('dadosBenchmark_validacaoAlgoritmoAD.csv') as csvDataFile:
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


        for attribute in attribute_matrix:
            try:
                x = float(attribute[1][0])
                attribute[1] = ["NUMERICO"]
            except ValueError:
                continue
       # print(attribute_matrix)
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