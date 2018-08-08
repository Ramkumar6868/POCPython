from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from export_result.export_result import ExportResult

PRECISION_AT=[1, 5, 10, 25, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 25000]

class ProcessData:
    """ProcessData: except a sorted DataFrame on probabilty and calculate result
    1. calculate precision, f1, recall accuracy from DataFrame at every n of PRECISION_AT
    2. calculate first correct and incorrect prediction
    3. all score return as array [<segement_name>, <source_name>, <metric_name>, <score>]"""
    def __init__(self, data_frame, segment, output_file):
        self.data_frame = data_frame
        self.segment = segment
        self.output_file = output_file

    # process Dataframe
    def processData(self, source):
        data_frame_length = len(self.data_frame)
        result = []
        # calculate metric score at different position
        for n in PRECISION_AT:
            if n >= data_frame_length:
                n = data_frame_length
            # get head n rows from DataFrame
            head_data_frame_n = self.data_frame.head(n)
            # caculate metric score at n
            result += self.calculatePrecisionAtN(n, head_data_frame_n, source)
            # if n reaches number of total rows
            if n >= data_frame_length:
                break
        # calculate where appear firct correct and incorrect prediction
        firstIncorrect, firstCorrect = self.caluculatCorrectIncorrect()
        # write correct incorrect index to csv file
        result.append([self.segment, source, "first_correct_prediction", firstCorrect])
        result.append([self.segment, source, "first_incorrect_prediction", firstIncorrect])
        # write result to CSV output file
        exportObj = ExportResult(result)
        exportObj.openCSVFile(self.output_file)
        exportObj.writeToCSV()
        exportObj.closeCSVFile()

    def calculatePrecisionAtN(self, n, data_frame, source):
        # true data from dataFrame
        true_data = data_frame['is_sensitive'].values.astype('int').tolist()
        # convert probabilty to 0  or 1
        data_frame = data_frame['probability'].apply(lambda p: 1 if float(p) > 0.5 else 0)
        # predicted data from probability
        pred_data = data_frame.values.tolist()
        # metrics for calculate score
        metrics = ['precision', 'recall', 'f1', 'accuracy']
        result = []
        for metric in metrics:
            # calculate score of metric
            data = [self.segment, source, metric + "_at_" + str(n), globals()[metric + "_score"](true_data, pred_data)]
            # appen result data
            result.append(data)
        return result

    # calculate first occurance index of correct and incorrect prediction
    def caluculatCorrectIncorrect(self):
        # -1 no first occurance
        firstCorrect = -1
        firstIncorrect = -1
        # iterate over rows and check first occurance of correct and incorrect
        for index, row in self.data_frame.iterrows():
            # check if first incorrect result
            if firstIncorrect == -1 and ((float(row['probability']) > 0.5 and int(row['is_sensitive']) == 0) or (float(row['probability']) < 0.5 and int(row['is_sensitive']) == 1)):
                firstIncorrect = index
            # check if first correct result
            if firstCorrect == -1 and ((float(row['probability']) > 0.5 and int(row['is_sensitive']) == 1) or (float(row['probability']) < 0.5 and int(row['is_sensitive']) == 0)):
                firstCorrect = index
            # if first correct and incorrect got
            if firstCorrect != -1 and firstIncorrect != -1:
                break
        return firstCorrect, firstIncorrect




