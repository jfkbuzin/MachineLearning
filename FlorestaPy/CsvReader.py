import csv
def read_csv(validation_data):
    with open('dadosBenchmark_validacaoAlgoritmoAD.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        cont = 0
        for row in csvReader:
            if cont == 0:
                cont+=1
                continue
            validation_data.append(row)
        print(validation_data)