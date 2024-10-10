"""Module to handle the mocha report file and extract the test execution data from it"""
import json

class MochaReport:
    """Class to handle the mocha report file and extract the test execution data from it"""
    def __init__(self, mocha_execution_path: str):
        self.mocha_execution_path = mocha_execution_path
        self.mocha_execution_json = self.get_test_execution_data()
        self.mocha_execution_metadata = self.mocha_execution_json['stats']
        self.mocha_execution_results = self.mocha_execution_json['results']

    def get_test_execution_data(self):
        """Return json data from the mocha report file"""
        with open(self.mocha_execution_path, 'r', encoding="utf-8") as file:
            test_execution_data = json.load(file)
            return test_execution_data
