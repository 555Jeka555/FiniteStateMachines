import csv


def readMilyFromCsv(fileName, delimiter=';'):
    with open(fileName, 'r', encoding='ISO-8859-1') as file:
        reader = csv.reader(file, delimiter=delimiter)

        for row in reader:
            print(row)


def writeMureToCsv(fileName, delimiter=';'):
    with open(fileName, 'w', newline='', encoding='ISO-8859-1') as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerows([])


if __name__ == '__main__':
    readMilyFromCsv("data/read/Milly1.csv")
