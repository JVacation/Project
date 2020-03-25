import json
with open('data.txt') as json_file:
     data = json.load(json_file)
for p in data['config']:
	 clockFrame = (p['clockFrame'])
	 clockSide = (p['clockSide'])

class jsonParser:

     def get_clockFrame():
	 clockFrame = (p['clockFrame'])
	 return clockFrame
	 
	 def get_clockSide():
	  clockSide = (p['clockSide'])
	 return clockSide
	 
