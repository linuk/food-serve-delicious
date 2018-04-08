from urllib.request import urlopen
import json

api_key = '84726f78a89e843ebb8216386a86dd5d'
url = 'http://api.openweathermap.org/data/2.5/weather?q=London%2C%20UK&units=metric&appid={}'.format(api_key)
data = urlopen(url).read()
weather = json.loads(data)

# Print data in a prettier way
print(json.dumps(weather, indent=4, sort_keys=True))
