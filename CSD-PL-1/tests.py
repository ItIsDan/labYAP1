import requests

response = requests.get('http://localhost:8000/')
assert response.status_code == 200
print(response.text)

response = requests.get('http://localhost:8000/timezones')
assert response.status_code == 200
print("All good!")

response = requests.get('http://localhost:8000/Europe/Moscow')
assert response.status_code == 200
print(response.text)

response = requests.get('http://localhost:8000/UnknownZone')
assert response.status_code == 200
print(response.text)

response = requests.post(
    'http://localhost:8000/api/v1/time',
    json={'tz': 'Europe/Moscow'}
)
print("time", response.json())

response = requests.post(
    'http://localhost:8000/api/v1/date',
    json={'tz': 'Europe/Paris'}
)
print("date", response.json())

response = requests.post(
    'http://localhost:8000/api/v1/time',
    json={'tz': ''}
)
print("time, no tz", response.json())

response = requests.post(
    'http://localhost:8000/api/v1/date',
    json={'tz': ''}
)
print("date, no tz", response.json())

response = requests.post(
    'http://localhost:8000/api/v1/datediff',
    json={
        'start': {'date': '2024-12-01 12:00:00'},
        'end': {'date': '2024-12-02 12:00:00'}
    }
)
print(response.json())
