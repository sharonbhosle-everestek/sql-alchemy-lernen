import time
import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# =====================================================
# CONFIG
# =====================================================

TOKEN = "Bearer eyJraWQiOiJXbXZSaGVVWDNCdHFHbnVvb25xZ3NOZWh6eExJWUQvYjdKSnFGTkczLys0PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIyYmVjMDhkYi1hM2Q1LTRlNTQtOGEwMC01OTkwMjdhNjI4MjkiLCJjb2duaXRvOmdyb3VwcyI6WyJldmh1YjpyZXNvdXJjZSJdLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRwLmFwLXNvdXRoLTEuYW1hem9uYXdzLmNvbS9hcC1zb3V0aC0xX2xaZ2dWNWZ0RSIsInZlcnNpb24iOjIsImNsaWVudF9pZCI6IjFiZHZsdHRhcjBraTg3NmYxdTFwYWFzbXF0Iiwib3JpZ2luX2p0aSI6ImMwNzZjYjQ5LTg1YjMtNDY2OS1iNWFkLWZkNDJjYzg5MjBjMCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE3ODE2NjkzOTAsImV4cCI6MTc4MjIwMjAyNywiaWF0IjoxNzgyMTk4NDI4LCJqdGkiOiJhMWYxODBhOS0zZjFjLTQ2ODItYmM5ZC05NGVmYjA5ZGY2MzEiLCJ1c2VybmFtZSI6Imdvb2dsZV8xMDUwMDY3NTE3MzQ5NjU3NTcwOTIifQ.vzk6r-5p2ijWiGB9iTjG5L8_u3g2CjaZ204TkRr5wZUnu3gC5IPUOA9GS7ybTm5tYthSOsy1Edd8GkvI6nuB2MoHv6yhfD5eUl-9JiHf-OZsc60yuMLS4rgK4KyT5UVOKms71KbaCRThwrYWKtrAMNfDITa0sNLp16ZzLgWBZx-FQe9hO2B9uBdWapAmFQ8Os_XpOURYzmI9j6vI_YixLt57orT2Bae31GTsahp6Agtghp2QJa1SdO10PS6meXNCWEzW7YdfPTD1SenZPW5jDvBwE9wHLM01tslLqQkQmkr-1Aqy9eqS7YaEFswxKg36CvkFXniwdwMYmp_FUuH_jw"

INPUT_FILE = "everestek_employee_directory_fixed.xlsx"
OUTPUT_FILE = "everestek_employee_directory_with_ids.xlsx"

# BASE_URL = "https://hub.everestek.com/dashboard/employees"
BASE_URL = "https://y9qk2879td.execute-api.ap-south-1.amazonaws.com/prod/resources/search"

# =====================================================
# SESSION WITH RETRIES
# =====================================================

session = requests.Session()

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["POST"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session.mount("https://", adapter)
session.mount("http://", adapter)

HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

# =====================================================
# READ EXCEL
# =====================================================

df = pd.read_excel(INPUT_FILE)

if "Username" not in df.columns:
    raise Exception("Username column not found")

if "Email Address" not in df.columns:
    raise Exception("Email Address column not found")

employee_ids = []

total = len(df)

print(f"\nProcessing {total} employees...\n")

# =====================================================
# PROCESS EACH EMPLOYEE
# =====================================================

for index, row in df.iterrows():

    username = str(row["Username"]).strip()
    email = str(row["Email Address"]).strip().lower()

    payload = {
        "currentPage": 1,
        "filter": [],
        "limit": 10,
        "offset": 0,
        "search": username
    }

    # params = {
    #     "search": username
    # }
    # params = params

    employee_id = ""

    try:

        response = session.post(
            BASE_URL,
            # params=params,
            json=payload,
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        resources = data.get("resources", [])

        # ==========================================
        # Priority 1 -> Email Match
        # ==========================================

        for resource in resources:

            api_email = (
                str(resource.get("email", ""))
                .strip()
                .lower()
            )

            if api_email == email:
                employee_id = resource.get("employeeId", "")
                break

        # ==========================================
        # Priority 2 -> Name Match
        # ==========================================

        if not employee_id:

            for resource in resources:

                api_name = (
                    str(resource.get("name", ""))
                    .strip()
                    .lower()
                )

                if api_name == username.lower():
                    employee_id = resource.get("employeeId", "")
                    break

        employee_ids.append(employee_id)

        if employee_id:
            print(
                f"[{index+1}/{total}] "
                f"FOUND -> {username} -> {employee_id}"
            )
        else:
            print(
                f"[{index+1}/{total}] "
                f"NOT FOUND -> {username}"
            )

    except Exception as e:

        employee_ids.append("")

        print(
            f"[{index+1}/{total}] "
            f"ERROR -> {username} -> {str(e)}"
        )

    # avoid rate limiting
    time.sleep(0.2)

# =====================================================
# SAVE RESULT
# =====================================================

df["Employee ID"] = employee_ids

df.to_excel(
    OUTPUT_FILE,
    index=False
)

print("\n====================================")
print("Completed")
print(f"Output File: {OUTPUT_FILE}")
print("====================================")

found_count = sum(
    1 for x in employee_ids
    if str(x).strip()
)

print(f"Employee IDs Found: {found_count}/{total}")