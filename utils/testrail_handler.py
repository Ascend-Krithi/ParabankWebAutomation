import requests
import json
import base64
from datetime import datetime, timedelta, timezone

class TestRailHandler:
    def __init__(self):
        self.base_url = "https://ascendionqe.testrail.io"
        self.user = "kiruthika.ganesan@ascendion.com"
        self.api_key = "3ep3cdPZ0NMbBcLexCWU-2taKo7dxXVGJGNz7lrqb"
        self.project_id = 6
        self.suite_id = 11
        self.section_id = 38
        
        auth_str = f"{self.user}:{self.api_key}"
        self.headers = {
            "Authorization": f"Basic {base64.b64encode(auth_str.encode()).decode()}",
            "Content-Type": "application/json"
        }

    def get_ist_timestamp(self):
        # Creates a timestamp in IST (UTC + 5:30)
        ist_delta = timedelta(hours=5, minutes=30)
        ist_time = datetime.now(timezone.utc) + ist_delta
        return ist_time.strftime("%d-%b-%Y %I:%M:%S %p")

    def get_case_ids(self):
        url = f"{self.base_url}/index.php?/api/v2/get_cases/{self.project_id}&suite_id={self.suite_id}&section_id={self.section_id}"
        response = requests.get(url, headers=self.headers)
        return [case['id'] for case in response.json().get("cases", [])] if response.status_code == 200 else []

    def create_test_run(self, case_ids):
        url = f"{self.base_url}/index.php?/api/v2/add_run/{self.project_id}"
        payload = {
            "suite_id": self.suite_id,
            "name": f"Parabank_Automation_Run_{self.get_ist_timestamp()}",
            "include_all": False,
            "case_ids": case_ids
        }
        response = requests.post(url, headers=self.headers, json=payload)
        run_data = response.json()
        return run_data.get("id"), run_data.get("url")

    def add_result(self, run_id, case_id, status_id=1):
        url = f"{self.base_url}/index.php?/api/v2/add_result_for_case/{run_id}/{case_id}"
        payload = {"status_id": status_id, "comment": "Executed via Automated CI/CD Tool."}
        requests.post(url, headers=self.headers, json=payload)

    def update_testrail_results(self):
        print("\n" + "="*50)
        print("📊 INITIATING TESTRAIL REPORTING (IST)")
        case_ids = self.get_case_ids()
        if not case_ids:
            print("❌ No test cases found to update.")
            return

        run_id, run_url = self.create_test_run(case_ids)
        for c_id in case_ids:
            self.add_result(run_id, c_id)
        
        print(f"✅ RUN COMPLETED SUCCESSFULLY")
        print(f"🔗 TESTRAIL RUN URL: {run_url}")
        print("="*50 + "\n")
