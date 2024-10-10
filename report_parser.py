"""
Module to parse the mocha report file and build the final report to be sent to Xray.
"""
import json
import datetime

from mocha_report import MochaReport
from xray_execution import XrayExecution

class ReportParser:
    """Class to parse the mocha report file and build the final report to be sent to Xray"""
    def __init__(self, report_destination_path: str, region: str,
                 mocha_report: MochaReport, xray_execution: XrayExecution):
        self.report_destination_path = report_destination_path
        self.region = region
        self.xray_report_file = self.set_report_file_path()

        self.mocha_metadata = mocha_report.mocha_execution_metadata
        self.mocha_results = mocha_report.mocha_execution_results

        self.xray_execution = xray_execution

    def set_report_file_path(self):
        """Construct the file path for the final report"""
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return (
            f'{self.report_destination_path}'
            f'/{self.region}'
            f'-{current_date}.json'
        )

    def get_test_execution_results(self):
        """Set the test execution statuses based on the results from the mocha report file"""
        test_execution_statuses = []
        execution_results = self.mocha_results
        for result in execution_results:
            test_title = result['suites'][0]['title']
            num_tests = len(result['suites'][0]['tests'])
            num_passes = len(result['suites'][0]['passes'])

            if num_tests == num_passes:
                test_execution_statuses.append({"testKey": test_title, "status": 'PASSED'})

            elif num_tests > num_passes:
                test_execution_statuses.append({"testKey": test_title, "status": 'TO DO'})

        return test_execution_statuses

    def build_report(self):
        """Build the final report to be sent to Xray"""
        test_execution_results = self.get_test_execution_results()
        test_execution_data = self.xray_execution.get_execution_data()

        test_execution_data['tests'] = test_execution_results
        return test_execution_data

    def write_report_to_file(self, report_data):
        """Write the final report to a file"""
        with open(self.xray_report_file, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
