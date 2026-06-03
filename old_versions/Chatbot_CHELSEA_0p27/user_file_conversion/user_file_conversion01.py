import json
from datetime import datetime

user_file1 = {}
username = input("What is the name of the user?: ")
try: 

	with open(f"{username}.json", 'r') as user_file:
		user_file1 = json.load(user_file)

except(FileNotFoundError):

	print("No user file by that name.")

user_file2 = {
	'birthday': {
		"date": "",
		"status": "none",
		"last asked": ""
	},
	'zodiac': "",
	'uam': [],
	'uamnot': [],
	'like': {
		'general': [], 
		'color': [],
		'music': [], 
		'music artist': [],
		'song': [], 
		'food': [], 
		'drink': [], 
		'movie': [], 
		'anime': [], 
		'hobby': []
	},
	'dislike': {
		'general': [], 
		'color': [],
		'music': [], 
		'music artist': [],
		'song': [],
		'food': [], 
		'drink': [], 
		'movie': [], 
		'anime': [], 
		'hobby': []
	},
	'favorite': {
		'color': [], 
		'music': [], 
		'music artist': [], 
		'song': [], 
		'food': [], 
		'drink': [], 
		'movie': [], 
		'anime': [], 
		'hobby': []
	},
	'have': [],
	'have not': [],
	'finds funny': [],
	'popular topics': [],
	"happy": 0,
    "angry": 0,
    "sad": 0,
    "afraid": 0,
    "mood": ""
}

#Template for several of the lists
# {
# 	'info': 'something',
# 	'why': '',
# 	'date': timestamp
# }

#Template for topics:
# {
# 'topics': [],
# 'date': timestamp
# }

for uam in user_file1['uam']:
	user_file2['uam'].append({
		'info': uam,
		'why': '',
		'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
	})

for uamnot in user_file1['uamnot']:
	user_file2['uamnot'].append({
		'info': uamnot,
		'why': '',
		'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
	})

user_file2['happy'] = user_file1['happy']
user_file2['angry'] = user_file1['angry']
user_file2['sad'] = user_file1['sad']
user_file2['afraid'] = user_file1['afraid']
user_file2['mood'] = user_file1['mood']

with open(f"{username}_user_details.json", 'w') as user_file:
	json.dump(user_file2, user_file, indent=4)

print("User file successfully converted.")