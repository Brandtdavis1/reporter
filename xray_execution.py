"""Module to handle the data for an X-ray execution ticket"""
import json

class XrayExecution:
    """Class for X-ray execution ticket."""
    existing_execution_template = ""
    new_execution_template = ""

    def __init__(self, jira_ticket_key: str, mocha_metadata: json,
                 is_existing_test_execution: bool = False, summary_text: str = None):
        """
        This constructor will initialize several key attributes required by the Jira Xray API

        Args:
            jira_ticket_key (str):
                - If we are creating a new test execution, this will be the test plan key.
                - If we are updating an existing test execution, this will be the test execution key.

            summary_text (str): The summary/title text to be set for the test execution in Jira.
                - Only required for new test executions.
         """
        self.jira_ticket_key = jira_ticket_key
        self.is_existing_execution = is_existing_test_execution
        self.summary_text = summary_text

        self.test_run_start = mocha_metadata['start']
        self.test_run_finish = mocha_metadata['end']

        self.xray_template_file = (XrayExecution.existing_execution_template
            if self.is_existing_execution
            else XrayExecution.new_execution_template)

    def get_new_execution_data_json(self):
        """Return required json data for a new test execution"""
        new_execution_data = {
            "info": {
                "summary": self.summary_text,
                "startDate": self.test_run_start,
                "finishDate": self.test_run_finish,
                "testPlanKey": self.jira_ticket_key
            }
        }
        return new_execution_data

    def get_existing_execution_data_json(self):
        """Return required json data for an existing test execution"""
        existing_execution_data = {
            "testExecutionKey": self.jira_ticket_key,
        }
        return existing_execution_data

    def get_execution_data(self):
        """Return json data for a new or an existing test execution"""
        return (self.get_existing_execution_data_json()
            if self.is_existing_execution
            else self.get_new_execution_data_json())

