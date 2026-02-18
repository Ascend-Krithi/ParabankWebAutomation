import requests
import json
import base64

class TestRailHandler:
    def __init__(self):
        # Updated Credentials provided by you
        self.base_url = "https://ascendionqe.testrail.io"
        self.user = "kiruthika.ganesan@ascendion.com"
        self.api_key = "3ep3cdPZ0NMbBcLexCWU-2taKo7dxXVGJGNz7lrqb"
        self.project_id = 6
        self.suite_id = 11
        self.section_id = 38
        
        # Setup Auth
        auth_str = f"{self.user}:{self.api_key}"
        self.headers = {
            "Authorization": f"Basic {base64.b64encode(auth_str.encode()).decode()}",
            "Content-Type": "application/json"
        }

    def get_case_ids(self):
        """Fetches all case IDs from the specified section, similar to your Java getCaseIds."""
        url = f"{self.base_url}/index.php?/api/v2/get_cases/{self.project_id}&suite_id={self.suite_id}&section_id={self.section_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            cases = response.json().get("cases", [])
            return [case['id'] for case in cases]
        return []

    def create_test_run(self, case_ids):
        """Creates a new test run for the specified cases."""
        url = f"{self.base_url}/index.php?/api/v2/add_run/{self.project_id}"
        payload = {
            "suite_id": self.suite_id,
            "name": f"Automation Run - {self.get_timestamp()}",
            "include_all": False,
            "case_ids": case_ids
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json().get("id")

    def add_result(self, run_id, case_id, status_id=1):
        """Adds a result (1=Pass) to a specific case in a run."""
        url = f"{self.base_url}/index.php?/api/v2/add_result_for_case/{run_id}/{case_id}"
        payload = {
            "status_id": status_id,
            "comment": "Test executed via Parabank Python Automation Framework"
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json().get("id")

    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def update_testrail_results(self):
        """Orchestrates the full update logic exactly like publishTestReportInTestRail."""
        print("🚀 Starting TestRail result update...")
        case_ids = self.get_case_ids()
        if not case_ids:
            print("⚠️ No case IDs found in Section 38.")
            return

        run_id = self.create_test_run(case_ids)
        print(f"✅ Created Test Run ID: {run_id}")

        for case_id in case_ids:
            result_id = self.add_result(run_id, case_id, status_id=1)
            print(f"✔️ Result added for Case ID {case_id} (Result ID: {result_id})")
