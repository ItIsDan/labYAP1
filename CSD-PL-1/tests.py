import requests

response = requests.post(
    'http://localhost:8000/api/v1/time',
    json={'tz': 'Europe/Moscow'}
)
print(response.json())

response = requests.post(
    'http://localhost:8000/api/v1/date',
    json={'tz': 'Europe/Paris'}
)
print(response.json())

response = requests.post(
    'http://localhost:8000/api/v1/datediff',
    json={
        'start': {'date': '2024-12-01 12:00:00'},
        'end': {'date': '2024-12-02 12:00:00'}
    }
)
print(response.json())
