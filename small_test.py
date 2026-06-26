import requests

TOKEN = "Bearer eyJraWQiOiJXbXZSaGVVWDNCdHFHbnVvb25xZ3NOZWh6eExJWUQvYjdKSnFGTkczLys0PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIyYmVjMDhkYi1hM2Q1LTRlNTQtOGEwMC01OTkwMjdhNjI4MjkiLCJjb2duaXRvOmdyb3VwcyI6WyJldmh1YjpyZXNvdXJjZSJdLCJpc3MiOiJodHRwczovL2NvZ25pdG8taWRwLmFwLXNvdXRoLTEuYW1hem9uYXdzLmNvbS9hcC1zb3V0aC0xX2xaZ2dWNWZ0RSIsInZlcnNpb24iOjIsImNsaWVudF9pZCI6IjFiZHZsdHRhcjBraTg3NmYxdTFwYWFzbXF0Iiwib3JpZ2luX2p0aSI6ImMwNzZjYjQ5LTg1YjMtNDY2OS1iNWFkLWZkNDJjYzg5MjBjMCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE3ODE2NjkzOTAsImV4cCI6MTc4MjIwMTU5OCwiaWF0IjoxNzgyMTk3OTk5LCJqdGkiOiJmNWMyNTUyNS1jOGIyLTQ3MjItODk4ZC03MTk5YzRkZjhkOGYiLCJ1c2VybmFtZSI6Imdvb2dsZV8xMDUwMDY3NTE3MzQ5NjU3NTcwOTIifQ.OMoYbl-p5re5U6nv_WvDbOZ5WDB6xP1YC85MSjbgnT_1d3m1EIqSsUa53H9rkRvCdOGUDbQWtXAXN4kNUe0ZCm9cS4tT3GYF4SZ44Z-LegBwinns5w523wCoWDmE6SBQCws4KadzQjB7NOsx761eVhadcm7PXO7L-3CfA9cFFNy3Os17r5HVo0pefvob6jdPrA6cFb9pQteTIffSZPqef5epOSWehjpwWa21cGu2c8LFDYeIxu7jUQmjCyqGaLYtZm5kwde0Z_oT_h4HEGMHZB4vC-rzWOcEhbl-naTjwglgiDcHgfm8iIjbJGPeiabKRSroeAuiV2l72tSO2lKrrw"

headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json",
    "Origin": "https://hub.everestek.com",
    "Referer": "https://hub.everestek.com/"
}

payload = {
    "currentPage": 1,
    "filter": [],
    "limit": 10,
    "offset": 0,
    "search": "Abhijit Mangale"
}

r = requests.post(
    "https://y9qk2879td.execute-api.ap-south-1.amazonaws.com/prod/resources/search",
    headers=headers,
    json=payload
)

print(r.status_code)
print(r.text[:1000])