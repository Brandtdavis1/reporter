''' Main script to run the Xray test execution report parser and importer '''
import argparse
import os
import re

from API.xray.authenticator import Authenticator
from API.xray.importer import Importer

from report_parser import ReportParser
from mocha_report import MochaReport
from xray_execution import XrayExecution


# Command line args
REGION = ""
RELEASE_VER = ""

# SEALED SECRETS
XRAY_SECRET_NAME = 'XrayApi'

# TEMP
MOCHA_REPORT_PATH = "./report.json"
XRAY_REPORT_PATH = "./"
FINAL_REPORT_FILE_NAME = ''

TEST_EXECUTION_SUMMARY = f"Automated Smoke Test for Release {RELEASE_VER} on {REGION}"

# Command line argument support
# Example usage: python main.py ./report.json existing **** --jira_key=OCL-****
parser = argparse.ArgumentParser(description='Xray Test Execution Report Parser')
parser.add_argument('mocha_file',
                    type=str,
                    help='The filename of the mocha report')

parser.add_argument('execution_status',
                    type=str,
                    choices=['new', 'existing'],
                    help='The status of the test execution')

parser.add_argument('env',
                    type=str,
                    choices=['stage4', 'stage5', 'stage6',
                             'stage7', 'stage8', 'stage10',
                             'ca', 'us', 'au', 'de', 'uk'],
                    help='The region where the tests were executed')

parser.add_argument('--jira_key',
                    type=str,
                    help='Jira key for existing test execution')


args = parser.parse_args()

# -------- Validate Args --------
# Stop if the mocha report file does not exist
if os.path.isfile(args.mocha_file) is False:
    parser.error('The mocha report file does not exist')

# Stop if we are missing Jira key for existing test execution
if args.execution_status == 'existing' and args.jira_key is None:
    parser.error('--jira_key is required for existing test execution')

# Stop if the Jira key is not in the correct format
if args.execution_status == 'existing' and re.search("^OCL-.+[0-9]$", args.jira_key) is None:
    parser.error('Invalid Jira key format. Must be in the format OCL-####')

print(args)

authenticator = Authenticator(XRAY_SECRET_NAME)

# mocha_execution_report = MochaReport(MOCHA_REPORT_PATH)
# xray_execution_report = XrayExecution(args.jira_key,
#                                       mocha_execution_report.mocha_execution_metadata,
#                                       True,
#                                       TEST_EXECUTION_SUMMARY)

# reporter = ReportParser(XRAY_REPORT_PATH,
#                         args.env,
#                         mocha_execution_report,
#                         xray_execution_report)

# xray_report = reporter.build_report()
# reporter.write_report_to_file(xray_report)

with open(FINAL_REPORT_FILE_NAME, 'r', encoding='utf-8') as f:
    importer = Importer(authenticator.auth_headers)
    print('Sending results to Jira...')
    response = importer.import_results(f.read())
    print(response.content)
