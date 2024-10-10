import json

# Globals
CYPRESS_RESULTS_PATH = '/Users/brandt.davis/passportal-clover/tests/cypress_automation/cypress/reports/report.json'

RESULT_FILE_TEMPLATE = '''{
    "info": {
        "summary" : "Test Execution",
        "description" : "This is from the REST API", 
        "startDate" : "2022-09-08T18:42:03.144Z",
        "finishDate" : "2022-09-08T18:42:22.646Z", 
        "testPlanKey" : "OCL-11824"
    },
}'''

class Reporter:
    def __init__(self):
        pass

    def get_json_results(self):
        with open(CYPRESS_RESULTS_PATH, 'r') as f:
            data = json.load(f)
        return data

    def get_start_and_finish_times(self, data):
        return (data['stats']['start'], data['stats']['end'])

    def get_test_status(self, data, test_title):
        for test in data['results'][0]['suites'][0]['tests']:
            if test['title'] == test_title:
                return test['state']

    def create_report(self):
        results = json.loads(RESULT_FILE_TEMPLATE)
        results['startDate'] = self.start

        

r = Reporter()
data = r.get_json_results()
r.start, r.finish = r.get_start_and_finish_times(data)
r.status = r.get_test_status(data, "SsoLoginPage")

print(r.__dict__)
r.create_report()
#print(data["stats"]["start"])