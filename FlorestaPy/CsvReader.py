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

       # print(attribute_matrix)
        return validation_data, attribute_matrix
