import csv
import ValidationData as vd

def read_csv():
    with open('dadosBenchmark_validacaoAlgoritmoAD.csv') as csvDataFile:
        validation_data = []
        csvReader = csv.reader(csvDataFile)
        cont = 0
        attribute_list = []
        for row in csvReader:
            if cont == 0:
                attribute_list = row
                cont+=1
                continue

            dado_atual = vd.ValidationData(row[0],row[1],row[2],row[3],row[4])

            validation_data.append(dado_atual)
        # print(attribute_list)
        # print(validation_data)
        return validation_data, attribute_list
