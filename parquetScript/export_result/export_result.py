import pandas as pd
import csv

class ExportResult:
    """docstring for ExportResult"""
    def __init__(self, data_list):
        self.data_list = data_list
        self.file_writer = None
        self.csv_file = None

    def writeToCSV(self):
        for data in self.data_list:
            self.file_writer.writerow({'segment': data[0], 'source': data[1], 'metric': data[2], 'score': data[3]})

    def openCSVFile(self, file):
        self.csv_file = open('result.csv', 'a')
        headers = ["segment", "source", "metric", "score"]
        self.file_writer = csv.DictWriter(self.csv_file, delimiter=',', lineterminator='\n', fieldnames=headers)

    def closeCSVFile(self):
        self.csv_file.close()

    def writeHeaderToCSVFile(self):
        self.file_writer.writeheader()

    def clearCSVFile(self, outpu_file):
        self.csv_file = open(outpu_file, 'w')
        self.closeCSVFile()

