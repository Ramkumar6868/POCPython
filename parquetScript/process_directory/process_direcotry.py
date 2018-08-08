import os
import pandas as pd
import numpy as np
from fetch_server.request import FetchUrl
from process_output_data.process_data import ProcessData
from export_result.export_result import ExportResult



class ProcessDirectory:
    """ProcessDriectory : process directory as per source and per segment and send DataFrame to
    ProcessData modal for processData
    1. Clear the output CSV file
    2. Process throuh directory and fetch data in DataFrame
    3. API call to server and responce is save as DataFrame
    4. Sort Data by Probabilty
    5. send DataFrame with ['file_id', 'probability', 'is_sensitive'] columns to ProcessData Modal"""
    def __init__(self, dir_path, output_file, api_url):
        self.dir_path = dir_path
        self.output_file = output_file
        self.api_url = api_url

    def processDirectory(self):
        # clear output file Data
        exportObj = ExportResult([])
        exportObj.clearCSVFile(self.output_file)
        exportObj.openCSVFile(self.output_file)
        exportObj.writeHeaderToCSVFile()
        exportObj.closeCSVFile()
        # walk through segment by segment
        for segment in os.listdir(self.dir_path):
            # segment DataFrame i.e. result of all files data in one DataFrame
            segment_output_data_frame = pd.DataFrame([])
            # walk through all sources in segment
            for source in os.listdir(self.dir_path + "/" + segment):
                # to store DataFrame of all files in source folder
                source_output_data_frame = self.processSource(self.dir_path + "/" + segment + "/" + source, source)
                # add source DataFrame to segment DataFrame
                segment_output_data_frame = pd.concat([source_output_data_frame, segment_output_data_frame])
                # Process per source data
                processDataObj = ProcessData(source_output_data_frame, segment, self.output_file)
                processDataObj.processData(source)
            # sort segment DataFrame by probability
            segment_output_data_frame = segment_output_data_frame.sort_values('probability', ascending=False).reset_index(drop=True)
            # Process per segement Data
            processDataObj = ProcessData(segment_output_data_frame, segment, self.output_file)
            processDataObj.processData('ALL_SOURCES')

    # process source directory
    def processSource(self, source_path, source_id):
        for root, dirs, files in os.walk(source_path):
            # only .parquet and permission to open files
            files = [f for f in files if (not f[0] == '.') and f.endswith('.parquet')]
            # Source DataFrame to Store
            source_data_frame = pd.DataFrame([])
            for file in files:
                file_path = source_path + "/" + file
                try:
                    data_frame = pd.read_parquet(file_path, engine='fastparquet')
                except PermissionError:
                    print("Permission Error while reading file", file_path)
                except OSError as e:
                    print("Could not process file " + file_path + "because {}".format(str(e)))
                else:
                    # Make batches for API call in 1000 rows per call
                    data_frame_in_batches = self.makeBatches(data_frame, 1000)
                    # process batches
                    output_data_frame = self.processFileData(data_frame_in_batches, source_id)
                    # merge output probabilty with file data
                    output_data_frame = pd.merge(data_frame, output_data_frame, on='file_id')
                    # exract only required columns to process data
                    output_data_frame = pd.DataFrame(data = output_data_frame, columns=["file_id", "is_sensitive", "probability"])
                    # Add output of file DataFrame to source DataFrame
                    source_data_frame = pd.concat([source_data_frame, output_data_frame])
            return source_data_frame.sort_values('probability', ascending=False).reset_index(drop=True)

    # process batches of file
    def processFileData(self, data_frame_in_batches, source_id):
        # request parameters
        request_params = {
            source_id: source_id
        }
        # to hold responce Array
        output = np.array([])
        # process per batch data
        for batch_data_frame in data_frame_in_batches:
            # extract only required column in API params
            request_params["files"] = pd.DataFrame(data = batch_data_frame, columns=["file_id", "name", "level", "entry_count", "path", "files_count", "size"]).to_dict(orient='records')
            # call to server and get responce
            fetch_url = FetchUrl(self.api_url)
            output = np.concatenate([output, np.array(fetch_url.fetchApi(request_params))])
        # return resulted data as DataFrame
        return pd.DataFrame.from_records(output)

    # create batches from file data
    def makeBatches(self, data_frame, size):
        return (data_frame[pos : pos + size] for pos in range(0, len(data_frame), size))



