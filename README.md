# cypress-test-result-reporter
- To convert a mocha/cypress report into xray format:
  - `python main.py ./path_to_cypress_report.json existing region --jira_key=OCL-****`

- To import xray results file to Jira:
  - `python main.py ./path_to_cypress_report.json existing region --jira_key=OCL-**** --import_results=True --xray_report=./path_to_xray_file.json`