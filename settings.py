import json

file = open("packages/styling.json")
styling = json.loads(file.read())
file.close()
