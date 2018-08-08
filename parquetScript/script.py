# import numpy as np
# import os
import sys
from process_directory.process_direcotry import ProcessDirectory
# import math
# import requests
# import json
# from sklearn.metrics import accuracy_score
# from sklearn.metrics import recall_score
# from sklearn.metrics import f1_score
# from sklearn.metrics import precision_score

if __name__ == '__main__':
    PATH_TO_FOLDER = sys.argv[1]
    OUTPUT_FILE = sys.argv[2]
    API_URL = sys.argv[3]
    pDir = ProcessDirectory(PATH_TO_FOLDER, OUTPUT_FILE, API_URL)
    pDir.processDirectory()
