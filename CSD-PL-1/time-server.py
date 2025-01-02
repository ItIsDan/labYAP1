from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
import json 
from datetime import datetime, timedelta
import pytz
from tzlocal import get_localzone

def application(environment, start_response):
    path = environment.get('PATH_INFO', '/')
    method = environment.get('REQUEST_METHOD', 'GET')
    content_length = int(environment.get('CONTENT_LENGTH', 0) or 0)

    if content_length:
        body = environment['wsgi.input'].read(content_length).decode('utf-8')
    
    server_timezone = get_localzone()

    try:
        if method == 'GET':
            if path == '/timezones': # Выводит все часовые пояса, захотелось так.
                response = all_timezones()
                start_response('200 OK', [('Content-Type', 'text/html')])
                
                return [response.encode('utf-8')]
            elif path == '/': # Выводит текущее время по запросу страницы.
                response = server_time(server_timezone)
                start_response('200 OK', [('Content-Type', 'text/html')])
                
                return [response.encode('utf-8')]
            elif path.startswith('/'): # Выводит время конкретного часового пояса
                time_zone_name = path[1:]
                response = timezone_time(time_zone_name)
                start_response('200 OK', [('Content-Type', 'text/html')])

                return [response.encode('utf-8')]
            
        elif method == 'POST':
            if path == '/api/v1/time':
                if body: 
                    data = json.loads(body)
                
                timezone_name = data.get('tz', str(server_timezone))
                response = time_json(timezone_name)
                start_response('200 OK', [('Content-Type', 'application/json')])
                
                return [json.dumps(response).encode('utf-8')]

            elif path == '/api/v1/date':
                if body:
                    data = json.loads(body)
                
                timezone_name = data.get('tz', str(server_timezone))
                response = date_json(timezone_name)
                start_response('200 OK', [('Content-Type', 'application/json')])
                
                return [json.dumps(response).encode('utf-8')]

            elif path == '/api/v1/datediff':
                if body:
                    data = json.loads(body)
                
                response = datediff_json(data)
                start_response('200 OK', [('Content-Type', 'application/json')])
                
                return [json.dumps(response).encode('utf-8')]

        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        
        return [b'Not Found']

    except Exception as e:
        start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
        
        return [json.dumps({'error': str(e)}).encode('utf-8')]

def server_time(timezone):
    current_time = datetime.now(timezone)
    
    return f"<html><body><h1>Current Server Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}</h1></body></html>"

def all_timezones():
    timezones = pytz.all_timezones
    response = "<html><body><h1>All Timezones</h1><ul>"
    
    for tz_name in timezones:
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz)
        response += f"<li><h2><a href='/{tz_name}'>{tz_name}</a>: {now.strftime('%Y-%m-%d %H:%M:%S')}</h2></li>"
    
    response += "</ul></body></html>"
    
    return response

def timezone_time(timezone_name):
    try:
        timezone = pytz.timezone(timezone_name)
        now = datetime.now(timezone)
    
        return f"<html><body><h1>Current Time in {timezone_name}: {now.strftime('%Y-%m-%d %H:%M:%S')}</h1></body></html>"
    
    except pytz.UnknownTimeZoneError:
        return f"<html><body><h1>Error: Unknown timezone {timezone_name}</h1></body></html>"

def time_json(timezone_name):
    try:
        timezone = pytz.timezone(timezone_name)
    
    except pytz.UnknownTimeZoneError:
        timezone = get_localzone()
    
    now = datetime.now(timezone)
    
    return {'time': now.strftime('%Y-%m-%d %H:%M:%S'), 'tz': timezone.zone if hasattr(timezone, 'zone') else str(timezone)}

def date_json(timezone_name):
    try:
        timezone = pytz.timezone(timezone_name)
    
    except pytz.UnknownTimeZoneError:
        timezone = get_localzone()
    
    now = datetime.now(timezone)
    
    return {'date': now.strftime('%Y-%m-%d'), 'tz': timezone.zone if hasattr(timezone, 'zone') else str(timezone)}

def datediff_json(data):
    try:
        start = data['start']
        end = data['end']

        start_date = parse_date_with_timezone(start)
        end_date = parse_date_with_timezone(end)

        diff = abs(end_date - start_date)
    
        return {'Difference_seconds': diff.total_seconds(),
                'Difference_minutes': diff.total_seconds() // 60}
    
    except KeyError as e:
        return {'error': f'Missing key: {str(e)}'}

def parse_date_with_timezone(date_data):
    date_str = date_data['date']
    timezone_name = date_data.get('tz', str(get_localzone()))
    timezone = pytz.timezone(timezone_name)
    
    return timezone.localize(datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S'))

# Start server
if __name__ == '__main__':
    with make_server('', 8000, application) as server: # host, port, app
        print("Serving on port 8000...")
        server.serve_forever()
