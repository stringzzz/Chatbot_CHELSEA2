#   chatbotCHELSEA, an AI chatbot with simulated emotions, math logic, and some self identity (chelsea class)
#   Copyright (C) 2024 stringzzz, Ghostwarez Co.
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Chatbot CHELSEA: CHat Emotion Logic SEnse Automator (0.30) (BETA)

import json
import os
import re
import random
from datetime import datetime
import subprocess
import sys
import time
import math
from difflib import SequenceMatcher
from CHELSEA_MATH_LOGIC import CHELSEA_Math_Logic
from DATE_DIFFERENCE import date_difference

class chelsea:
	def __init__(self, bot_name):
		self.bot_name = bot_name
		self.dictionary = {}

		self.bigrams = {}
		self.reverse_bigrams = {}
		self.trigrams = {}
		self.reverse_trigrams = {}
		self.imagined_blacklist = []
		self.imagined_blacklist_counter = 1
		self.past_topic_blacklist = []

		self.message_dict2 = {}
		self.unanswered_questions = {}
		self.popular_words = {"happy": [], "angry": [], "sad": [], "afraid": []}
		self.nEmotions = ["happy", "angry", "sad", "afraid"]
		self.current_mood = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0, "pitch": 435, "speed": 0.85}
		self.pitches = {"happy": 435, "angry": 390, "sad": 400, "afraid": 445}
		self.speeds = {"happy": 0.85, "angry": 0.82, "sad": 0.92, "afraid": 0.8}
		self.user_message = " "
		self.user_self = {}
		self.chatlog = []
		self.Xchatlog = []
		self.chatlog_file = {"regular": f"{self.bot_name}chatlog.txt", "extended": f"{self.bot_name}Xchatlog.txt" }
		self.file_path = "" #PATH
		self.chelsea_self = {}
		self.agree = ['agreed, ', 'true ', 'yes ', 'i know ', 'true that, ', 'okay ', 'for sure, ', 'oh yeah, ', 'indeed, ', 'yep, ', 'you know it, ', 'correct, ']
		self.disagree = ['no, ', 'disagree, ', 'wrong, ', 'not true, ', 'false, ', 'nope, ', 'incorrect, ', 'i know otherwise, ', 'oh no, ', 'not valid, ', 'negative, ']
		self.topics = {}
		self.previous_pairs = []

		self.unanswered = {"what": False, "why is": False, "why are": False}

		#For piper voice model
		self.MODEL_PATH = "/YOUR_DIRECTORY_HERE/.local/share/piper-tts/piper-voices/en_US-amy-low.onnx"
		self.piper_proc = None

		#For use in determining time frames from now to specific timestamp
		self.date_difference = date_difference()

		#Set all modes to off (False) by default
		self.enabled_modes = {
			'speech_recognition': False,
			'no_user_file': False,
			'no_memory_output': False
		}

		#Synonym list for various pattern matching and responses
		self.synonym_lists = {
			'yes': ['yes', 'absolutely', 'certainly', 'indeed', 'by all means', 'assuredly', 'undoubtedly', 'yeah', 'yep', 
			'yup', 'mhm', 'uh-huh', 'yah', 'for sure', 'you bet', 'of course', 'affirmative', 'exactly', 'roger that', 'correct'],
			'no': ['no', 'by no means', 'in no way', 'negative', 'nope', 'nah', 'nah bro', 'mm-mm', 'uh-uh', 'no way', 'nay', 'not', 'incorrect'],
			'have': ['have', 'own', 'possess', 'got', 'gots'],
			'have not': ['do not have', 'don\'t have', 'do not own', 'do not possess', 'don\'t got', 'have no'],
			'because': ['because', 'as', 'as a result of', 'by cause of', 'by reason of', 'by virtue of', 'considering', 'due to', 'for the reason that', 'owing to', 'since', 'thanks to', 'cuz'],
			'like': ['like', 'love', 'enjoy', 'adore', 'appreciate'],
			'dislike': ['dislike', 'hate', 'loathe', 'detest', 'despise', 'don\'t like'],
			'favorite': ['favorite', 'preferred', 'favored', 'choice', 'most beloved', 'most treasured', 'fondest', 'fav', 'fave', 'best'],
			'confirmation': ['okay', 'that\'s cool', 'cool', 'i\'ll remember that', 'got it', 'for sure', 'fo sho', 
			'awesome', 'that\'s good', 'good to know', 'roger that', 'alright', 'indeed', 'now i know', 'excellent', 'sweet', 'confirmed'],
			'besides': ['besides', 'other than', 'in addition to', 'on top of', 'except for', 'apart from', 'aside from', 'excluding'],
			'still': ['still', 'currently', 'continuously', 'presently', 'as of now'],
			'mind': ['mind', 'opinion', 'tastes', 'preference'],
			'change': ['change', 'alter', 'switch', 'flip'],
			'lol': ['lol', 'lulz', 'lmao', 'rofl', 'lmfao', 'roflmao', 'lol, good one' 'lulz, good one', 'that\'s funny', 'that\'s hilarious', 
		    'that\'s pretty funny', 'that\'s pretty hilarious',  'that is funny', 'that is hilarious', 'that is pretty funny', 'that is pretty hilarious', 
		    'that cracked me up', 'that made me laugh', 'that made me lol', 'that made me lmao', 'haha', 'hehe'],
			'months': ['january', 'jan', 'february', 'feb', 'march', 'mar', 'april', 'apr', 'may', 'june', 'jun', 'july', 'jul', 'august', 
			'aug', 'september', 'sep', 'october', 'oct', 'november', 'nov', 'december', 'dec'],
			'topics': ['color', 'music artist', 'music', 'song', 'food', 'drink', 'movie', 'anime', 'hobby']
		} #'months' and 'topics' not actually synonyms, just stored here for conveniance

		#Save details when asking questions about the user
		self.asked_question = {
			'question type': 'None',
			'info': '',
			'info type': 'None',
			'why': '',
			'date': '',
			'index': 0
		}

		#To not let CHELSEA learn a response such as 'i like cats' or 'i have a nice car':
		self.user_gave_details = False

		#Prevents response from going into 'ask_past_user_details' and falls through to the next ones instead
		#Needed after modifying user message to fit the pattern another method catches
		self.fall_through = False

		#To prevent CHELSEA from saying too many random dictionary definitions
		self.random_response_counter = 0

	#Input memory
	def input_dictionary(self):

		#Load the dictionary of words with ties to emotions
		with open(f"{self.file_path}dictionary2.json", 'r') as dictionary_file:
			self.dictionary = json.load(dictionary_file)
		
		self.dictionary_count = len(self.dictionary)

	def input_bigram_dicts(self):

		#Load the dictionary of bigrams (2 word groups)
		with open(f"{self.file_path}bigramDictionary2.json", 'r') as bigram_dictionary_file:
			self.bigrams = json.load(bigram_dictionary_file)

		#Load the dictionary of reverse bigrams
		with open(f"{self.file_path}reverseBigramDictionary2.json", 'r') as bigram_dictionary_file:
			self.reverse_bigrams = json.load(bigram_dictionary_file)

	def input_trigram_dicts(self):

		#Load the dictionary of trigrams (3 word groups)
		with open(f"{self.file_path}trigramDictionary2.json", 'r') as trigram_dictionary_file:
			self.trigrams = json.load(trigram_dictionary_file)

		#Load the dictionary of reverse trigrams
		with open(f"{self.file_path}reverseTrigramDictionary2.json", 'r') as trigram_dictionary_file:
			self.reverse_trigrams = json.load(trigram_dictionary_file)

	def input_message_dictionary(self):

		#Load the dictionary of message/response pairs
		with open(f"{self.file_path}messageDictionary2.json", 'r') as message_dictionary_file:
			self.message_dict2 = json.load(message_dictionary_file)

		#Get the number of responses for triggering certain choices in how to respond
		self.response_count = 0
		for emotion in self.nEmotions:
			self.response_count += len(self.message_dict2[emotion])

	def input_unanswered_questions(self):

		#Load the dictionary of unanswered questions, so sometimes CHELSEA can ask them for an answer
		with open(f"{self.file_path}unanswered_questions2.json", 'r') as unanswered_questions_file:
			self.unanswered_questions = json.load(unanswered_questions_file)

	def input_self(self):

		try:

			#Try to load self identity file
			with open(f"{self.file_path}{self.bot_name}self.json", 'r') as self_file:
				self.chelsea_self = json.load(self_file)

			#Check if birthday exists, if not create it as today
			if 'birthday' not in self.chelsea_self:

				self.chelsea_self['birthday'] = re.sub(r'(\d\d:\d\d:\d\d)', '00:00:00', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

			if 'moods' in self.chelsea_self and len(self.chelsea_self['moods']) > 0:
				
				#Load previous mood
				self.current_mood = dict(self.chelsea_self['moods'][-1]['mood'])

				#Potentially reduce mood values depending on how long since previous chat
				past_time = datetime.strptime(self.chelsea_self['moods'][-1]['mood date'], "%m/%d/%Y, %H:%M:%S")
				current_time = datetime.now()

				time_difference = (current_time - past_time).total_seconds() / 60			
				mood_reducer = math.floor(time_difference) #1440 in 1 day

				for mood in self.nEmotions:
					self.current_mood[mood] -= mood_reducer
					if self.current_mood[mood] < 0:
						self.current_mood[mood] = 0

				if self.current_mood['happy'] == 0 and self.current_mood['angry'] == 0 and self.current_mood['sad'] == 0 and self.current_mood['afraid'] == 0:
					self.current_mood['mood'] = 'happy'

				self.Xchatlog.append(f"{self.bot_name} (Thinking): Emotions decreased by {mood_reducer} since the previous chat.")

				self.adjust_mood()

		except(FileNotFoundError):

			#Self identity file doesn't exist, new chatbot
			self.chelsea_self = {"iam": [], "iamnot": []}

	def input_memory(self):

		#Input all memory from files
		self.input_dictionary()
		self.input_bigram_dicts()
		self.input_trigram_dicts()
		self.input_message_dictionary()
		self.input_unanswered_questions()
		self.input_self()

		#Open the temp file for writing to with piper subprocess:
		self.temp_piper_output_file = open('temp_piper_output', 'wb', buffering=0)
		self.load_tts_subprocess()

		#Make sure voice model and other parts in piper are fully loaded before the initial message
		time.sleep(4)

	def process_arguments(self, arguments):
		if len(arguments) > 1:

			if 'sr' in arguments:
				
				#Enable speech recognition mode, use speech-to-text for user replies
				self.enabled_modes['speech_recognition'] = True
				print("Speech recognition mode enabled.")

			if 'nouser' in arguments:

				#Enable no user mode, treats as if new user, also doesn't output user file at end of chat
				self.enabled_modes['no_user_file'] = True
				print("No user file mode enabled.")

			if 'nomem' in arguments:

				#Enable no memory output mode, only outputs chatlogs at end of chat, not any of CHELSEA's memory files
				self.enabled_modes['no_memory_output'] = True
				print("No memory output mode enabled.")

	def input_user_self(self):

		#Get self.username
		self.botReply("What is your name?")
		self.username = input("")
		self.username = re.sub(r"( )", "_", self.username)

		new_user_detected = False
		if self.enabled_modes['no_user_file']:
				
				#No user file mode, treat as if new user detected
				new_user_detected = True

		else:
			
			#Input the user file for the current user, if it exists
			try: 

				with open(f"{self.file_path}{self.username}_user_details.json", 'r') as user_file:
					self.user_self = json.load(user_file)

			except(FileNotFoundError):

				#New user detected
				new_user_detected = True

		if new_user_detected:

			#New user detected, create empty dictionary for user

			self.user_self = {
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
				'nothave': [],
				'finds funny': [],
				'popular topics': [],
				"happy": 0,
				"angry": 0,
				"sad": 0,
				"afraid": 0,
				"mood": ""
			}

		#If there are topics stored in the user file, input the newest set of them into current_topics
		if len(self.user_self['popular topics']) > 0:

			self.current_topics = list(self.user_self['popular topics'][-1]['topics'])

	def load_tts_subprocess(self):
		#Load the subprocesses for text-to-speech

		#Start Piper tts, piping stdout to temp file
		self.piper_proc = subprocess.Popen(
			[
				"stdbuf", "-oL",
				"piper", '--model', self.MODEL_PATH, '--length-scale', 
				str(self.current_mood["speed"]), '--output-raw'
			],
			stdin=subprocess.PIPE,
			stdout=self.temp_piper_output_file.fileno(),
			stderr=sys.stderr,
			bufsize=0
		)

	def close_tts_subprocess(self):

		#Close the subprocess for text-to-speech
		self.piper_proc.stdin.close()
		self.piper_proc.wait()

	def check_file_age(self, file_path, mod_limit):

		#Get modification time and current time as raw timestamps (floats)
		m_time_timestamp = os.path.getmtime(file_path)
		current_time_timestamp = time.time()

		#Calculate age in seconds
		age_seconds = current_time_timestamp - m_time_timestamp

		#Return True if time modified is greater than mod_limit AND file size is not 0
		if age_seconds >= mod_limit and os.path.getsize(file_path) != 0:
			return True
		
		else:
			return False

	def speak_response(self, response):

		#Send response text to piper to generate audio and output to temp file
		self.piper_proc.stdin.write(f"{response}\n".encode("utf-8"))
		self.piper_proc.stdin.flush()

		#See if temp piper output file hasn't been modified for at least 0.2 seconds
		while not self.check_file_age('temp_piper_output', 0.2):
			#Check every 1/10th second
			time.sleep(0.1)

		#Print the response text and then play the audio with play
		print(f"{self.bot_name}: {response}")
		os.system(f"play -q -r 16000 -c 1 -b 16 -e signed-integer -t raw temp_piper_output pitch {str(self.current_mood["pitch"])} 2>/dev/null")

		#Clear the temp file and rewind to start of file
		with open('temp_piper_output', 'w'):
			pass
		self.temp_piper_output_file.seek(0)
			
	#Output memory
	def output_dictionary(self):

		with open(f"{self.file_path}dictionary2.json", 'w') as dictionary_file:
			json.dump(self.dictionary, dictionary_file, indent=4)

	def output_bigram_dicts(self):

		with open(f"{self.file_path}bigramDictionary2.json", 'w') as bigram_dictionary_file:
			json.dump(self.bigrams, bigram_dictionary_file, indent=4)

		with open(f"{self.file_path}reverseBigramDictionary2.json", 'w') as bigram_dictionary_file:
			json.dump(self.reverse_bigrams, bigram_dictionary_file, indent=4)

	def output_trigram_dicts(self):

		with open(f"{self.file_path}trigramDictionary2.json", 'w') as trigram_dictionary_file:
			json.dump(self.trigrams, trigram_dictionary_file, indent=4)

		with open(f"{self.file_path}reverseTrigramDictionary2.json", 'w') as trigram_dictionary_file:
			json.dump(self.reverse_trigrams, trigram_dictionary_file, indent=4)	
			
	def output_message_dictionary(self):

		with open(f"{self.file_path}messageDictionary2.json", 'w') as message_dictionary_file:
			json.dump(self.message_dict2, message_dictionary_file, indent=4)

	def output_unanswered_questions(self):

		with open(f"{self.file_path}unanswered_questions2.json", 'w') as unanswered_questions_file:
			json.dump(self.unanswered_questions, unanswered_questions_file, indent=4)

	def output_self(self):

		#Moods list not found, create empty one
		if 'moods' not in self.chelsea_self:
			self.chelsea_self['moods'] = []

		#Store the current mood
		self.chelsea_self['moods'].append({
			'mood': self.current_mood, 
			'mood date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
		})

		#Only store previous 50 moods
		if len(self.chelsea_self['moods']) > 50:
			del self.chelsea_self['moods'][0]

		with open(f"{self.file_path}{self.bot_name}self.json", 'w') as self_file:
			json.dump(self.chelsea_self, self_file, indent=4)

	def chatlogOutput(self, chatlogFile, chatList):

		chatlog_file = open(f"{self.file_path}{chatlogFile}", 'a')
		chatlog_file.write(f"\n\n\n{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}")
		
		for line in chatList:
			chatlog_file.write(f"\n{line}")
		
		chatlog_file.close()		
	
	def output_chatlogs(self):

		self.chatlogOutput(self.chatlog_file["regular"], self.chatlog)
		self.chatlogOutput(self.chatlog_file["extended"], self.Xchatlog)

	def output_chelsea_data(self):

		#Output various data about CHELSEA's memory
		#Useful for debugging and analyzing her features
		data_file = open(f"{self.file_path}{self.bot_name}data.txt", 'w')

		#Output data about the number of words in the dictionary
		data_file.write(f"Words in emotion dictionary: {len(self.dictionary)}\n")
		for emotion in self.nEmotions:
			data_file.write(f"Number of {emotion} words in dictionary: {len([word for word in self.dictionary.keys() if self.dictionary[word]["emotion"] == emotion])}\n")
		data_file.write("\n")

		#Output number of known bigrams or trigrams
		data_file.write(f"Number of seen bigrams: {len(self.bigrams)}\n")
		data_file.write(f"Number of seen trigrams: {len(self.trigrams)}\n\n")
		
		#Output number of message/response pairs in memory
		message_count = 0
		for emotion in self.nEmotions:
			message_count += len(self.message_dict2[emotion])
			data_file.write(f"Number of {emotion} message/response pairs: {len(self.message_dict2[emotion])}\n")
		data_file.write(f"Total message/response pairs: {message_count}")

		#Output number of unanswered questions
		data_file.write(f"\n\nNumber of unanswered 'what is/are' questions: {len(self.unanswered_questions["what"])}")
		data_file.write(f"\nNumber of unanswered 'why is' questions: {len(self.unanswered_questions["why is"])}")
		data_file.write(f"\nNumber of unanswered 'why are' questions: {len(self.unanswered_questions["why are"])}")
		
		#Output current popular words
		for emotion in self.nEmotions:
			data_file.write(f"\n\nPopular {emotion} words: {", ".join(self.popular_words[emotion])}")
		data_file.close()

	def output_memory(self):

		if not self.enabled_modes['no_memory_output']:

			#Output all memory to files
			self.output_dictionary()
			self.output_bigram_dicts()
			self.output_trigram_dicts()
			self.output_message_dictionary()
			self.output_unanswered_questions()
			self.output_self()
			self.output_chelsea_data()

		else:

			print("Memory files not output.")

		self.output_chatlogs()

	def output_user_self(self):

		if not self.enabled_modes['no_user_file']:

			#Output user profile if not in no user mode

			#Output the current topics if any:
			if len(self.current_topics) > 0:
				self.user_self['popular topics'].append({
					'topics': self.current_topics, 
					'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
				})

				#Keep up to 50 lists of topics
				if len(self.user_self['popular topics']) > 50:
					
					#If more than 50, delete the oldest one
					del self.user_self['popular topics'][0]

			#Get educated guess of user's mood
			user_emotions = {}
			for emotion in self.nEmotions:
				user_emotions[emotion] = self.user_self[emotion]
			user_overall_mood = self.getMood2(user_emotions, True)
			self.user_self['mood'] = f"{self.username} seems to be a(n) {user_overall_mood} person."
			
			#Output the user's details
			with open(f"{self.file_path}{self.username}_user_details.json", 'w') as user_file:
				json.dump(self.user_self, user_file, indent=4)

		else:

			#No user file mode enabled, don't output the user dictionary

			print("User file not output.")
		
	def adjust_mood(self):

		#Change mood, pitch, and speaking speed according to CHELSEA's emotional values
		temp_dict = { 'happy': self.current_mood['happy'], 'angry': self.current_mood['angry'], 'sad': self.current_mood['sad'], 'afraid': self.current_mood['afraid'] }

		#Get potential new mood and check if it actually is different from current mood
		temp_mood = self.getMood2(temp_dict, True)
		if self.current_mood['mood'] != temp_mood:

			#Potential new mood must have value at least 100 higher than value for previous mood to change moods
			if self.current_mood[temp_mood] - self.current_mood[self.current_mood["mood"]] >= 100:

				self.Xchatlog.append(f"{self.bot_name} (Thinking): Mood changed from {self.current_mood['mood']} to {temp_mood}")
				self.current_mood['mood'] = temp_mood

				self.current_mood["pitch"] = self.pitches[self.current_mood["mood"]]
				self.current_mood["speed"] = self.speeds[self.current_mood["mood"]]

	#Other methods
	def addToMood(self):

		#Store previous mood to compare to next
		previous_mood = self.current_mood['mood']

		#Add the emotional values of the user reply to CHELSEA's emotional values
		for emotion in self.nEmotions:
			self.current_mood[emotion] += int(self.reply_mood[emotion] * 0.1)

		self.adjust_mood()

		#Output her current mood to the extended chatlog
		self.Xchatlog.append(f"{self.bot_name} (Thinking): I feel {self.current_mood["mood"]}")

		#If mood changes, reload piper subprocess for the new voice speed
		if self.current_mood['mood'] != previous_mood:
			self.close_tts_subprocess()
			self.load_tts_subprocess()

	def getReplyMood(self):

		#Get the mood of the user reply by looking at the emotion counts gathered on it
		temp_dict = { 'happy': self.reply_mood['happy'], 'angry': self.reply_mood['angry'], 'sad': self.reply_mood['sad'], 'afraid': self.reply_mood['afraid'] }
		self.reply_mood["mood"] = self.getMood2(temp_dict, True)

		#Output the educated guess of the user's mood to the extended chatlog
		self.Xchatlog.append(f"{self.bot_name} (Thinking): {self.username} seems to be {self.reply_mood["mood"]}")

	def getMood2(self, moodDictionary, botTF):

		#Get the overall mood of either CHELSEA or the user's response
		highest = max(moodDictionary.values())
		max1 = [k for k, v in moodDictionary.items() if v == highest]
		
		if (len(max1) == 1):
			#If there is a highest emotion, return the highest	
			return max1[0]
		
		#If there is a tie for highest emotion:
		if (botTF):
			#If using for bot mood, default 'happy'
			return 'happy'
		
		else:
			#If using for user mood, default 'temp neutral'
			return 'temp neutral'

	def botReply(self, botResponse):

		#Do the various parts of CHELSEA's response, text-to-speech with piper tts, chatlogs
		self.speak_response(botResponse)
		self.chatlog.append(f"{self.bot_name}: {botResponse}")
		self.Xchatlog.append(f"{self.bot_name}: {botResponse}")

		return botResponse

	def getMost(self, dictio, emotion):

		#Find which word has the highest emotion
		#For use when asking 'Which do you like/dislike more...' questions
		temp_dict = {}
		for key in dictio.keys():
			if (dictio[key]['emotion'] == emotion):
				temp_dict[key] = dictio[key][emotion]

		highest = max(temp_dict.values())
		max1 = [k for k, v in temp_dict.items() if v == highest]

		return max1
	
	#Chat methods
	def initial_greeting(self):

		#Initial message
		self.CHELSEA_previous_response = "hello"

		#Check if user birthday
		birthday_message = ''
		if self.date_difference.match_date(self.user_self['birthday']['date']):
			birthday_message = ' Happy birthday! :3'

		greeting = self.date_difference.get_time_greeting()
		holiday_greeting = self.date_difference.get_holiday_greeting()

		self.botReply(f"{greeting}, {self.username}.{birthday_message}{holiday_greeting}")

	def get_user_reply(self, sr, r, source):

		if not self.enabled_modes['speech_recognition']:
			
			#User text reply
			print(f"{self.username}: ", end = '')
			self.user_message = (input("")).lower()

			#Switch to speech recognition mode
			if self.user_message == 'enable speech':
				
				print("Speech recognition enabled")
				return True
		
		else:

			#Prevents problems arising from background noise by detecting it before the speech happens
			r.adjust_for_ambient_noise(source, duration=1)

			#'flush = True' needed after previous method, otherwise text won't print
			print(f"{self.username}: (Listening for response...)", end = '', flush = True)
			
			#timeout = None means it will wait forever until speech starts
			audio = r.listen(source, timeout = None) #, phrase_time_limit=10 #Add this if recording longer sentences is getting cut off

			try:

				#Using vosk offline voice model
				recorded_text = r.recognize_vosk(audio)

			except sr.UnknownValueError:
				print("Could not understand audio")

			except sr.RequestError as e:
				print(f"Could not request results; {e}")

			#User reply from speech recognition
			self.user_message = recorded_text.lower()

			#Clear the extra messages from the chat after audio detection
			#And reload the chat through the chatlog
			os.system("clear")
			print("\n".join(self.chatlog))
			print(f"{self.username}: {self.user_message}")

			#Option to disable speech with voice, switches to text only mode
			if self.user_message == 'disable speech':

				print("Speech recognition disabled")
				return True

		self.chatlog.append(f"{self.username}: {self.user_message}")
		self.Xchatlog.append(f"\n{self.username}: {self.user_message}")

		if self.user_message == "exit the chat":

			#If user said 'exit the chat', end chat and output all memory (Does this in 'chatbotCHELSEA.py'). 
			#Must use to output all memory!
			return True
		
		#Return False if not exiting the chat
		return False
		
	def math_comprehension(self):

		#Math comprehension logic
		m1 = re.search(r"what does ([a-zA-Z0-9\(\)\*/\^\-\+ ,]*) (equal|=)\??", self.user_message)
		
		#If math question detected
		if (m1):

			self.Xchatlog.append(f"{self.bot_name} (Thinking): Was asked a math question.")
			math_output = CHELSEA_Math_Logic(m1)

			if (math_output == "Invalid expression!"):

				#Something wrong with format of math question
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Incorrect syntax or error for math question.")

			else:

				#Math question format valid, found answer
				self.Xchatlog.append(f"{self.bot_name} (Thinking): I have the solution to the math question.")
			
			self.speak_response(math_output) #Might remove this if long math question is too much for tts
			self.chatlog.append(f"{self.bot_name}: {math_output}")
			self.Xchatlog.append(f"{self.bot_name}: {math_output}")
			
			#Was a math question
			return True
		
		#Was not a math question
		return False

	def chelsea_birthday(self):

		#Deal with CHELSEA's birthday stuff

		if re.search(r'(when|what day) is (your|ur) (birthday|b( |-)?day)\??', self.user_message):

			#User asked when CHELSEA's birthday is

			self.Xchatlog.append(f"{self.bot_name} (Thinking): Was asked when my birthday is, have answer.")
			self.botReply(f"my birthday is {self.chelsea_self['birthday'][:5]}")

			return True
		
		if re.search(r'happy birthday', self.user_message):

			#User wished CHELSEA 'happy birthday'

			if self.date_difference.match_date(self.chelsea_self['birthday']):

				if self.date_difference.get_days_past(self.chelsea_self['birthday']) == 0:

					#Is technically her birthday, but she was 'born' today

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Was given 'happy birthday', but I was born today.")
					self.botReply("i was actually born today")

					return True
				
				else:

					#Is her actual birthday, respond with thanks

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Was given 'happy birthday', respond with thanks.")
					self.botReply("thank you :3")

					return True
				
			else:

				#Is not her birthday

				self.Xchatlog.append(f"{self.bot_name} (Thinking): Was given 'happy birthday', today is not my birthday.")

				if random.randint(1, 33) == 1:

					self.botReply("today is not my birthday, it's my unbirthday! >:3")

				else:
					
					self.botReply("today is not my birthday >:3")

				return True
			
		if re.search(r'(how old|how many years( old)?) (are you|are u|r you|r u|ru|)\??', self.user_message):

			#User asked how old CHELSEA is, respond with number of years

			self.Xchatlog.append(f"{self.bot_name} (Thinking): Was asked 'how old are you?', respond with answer.")
			self.botReply(f"i am {self.date_difference.get_years_past(self.chelsea_self['birthday'])} years old")

			return True
		
		return False
	
	def ask_if_is(self):

		#Ask CHELSEA what CHELSEA is or is not
		match1 = re.search(r"what are you( not)?\?*$", self.user_message)
		if (match1):

			#'What are you...?' question format found

			if (not(match1.group(1)) and len(self.chelsea_self['iam']) != 0):

				#Asked 'what are you' question, give random answer from self memory
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Was asked what I am, have an answer.")
				self.botReply(f"i am {random.choice(self.chelsea_self['iam'])}")

				return True
			
			elif (match1.group(1) and len(self.chelsea_self['iamnot']) != 0):
			
				#Asked 'what are you not' question, give random answer from self memory
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Was asked what I am not, have an answer.")
				self.botReply(f"i am not {random.choice(self.chelsea_self['iamnot'])}")

				return True

		#'What are you...?' question format not found	
		return False
	
	def ask_if_user_is(self):

		#Ask CHELSEA what user is or is not
		match1 = re.search(r"what am i( not)?\?*$", self.user_message)

		if (match1):

			#'What am i...?' question format found

			if (not(match1.group(1)) and len(self.user_self['uam']) != 0):

				#Asked 'what am i' question, give random answer from user profile memory
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Was asked what user is, have an answer.")
				self.botReply(f"you are {re.sub(r"(your)", "my", random.choice(self.user_self['uam'])['info'])}")
				
				return True
			
			elif (match1.group(1) and len(self.user_self['uamnot']) != 0):

				#Asked 'what am i not' question, give random answer from user profile memory
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Was asked what user is not, have an answer.")
				self.botReply(f"you are not {re.sub(r"(your)", "my", random.choice(self.user_self['uamnot'])['info'])}")
				
				return True

		#'What am i...?' question format not found	
		return False
	
	def tell_what_is(self):

		#Tell CHELSEA what CHELSEA is or is not and see if there's agreement according to CHELSEA self memory
		match1 = re.search(r"^(?:are you|you are|you're) (not )?([a-z0-9, '\-]*)\?*", self.user_message)
		
		if (match1):

			#'are you/you are...' message found

			if (not(match1.group(1))):

				#'not' not detected in message

				breakout = False
				for iam in self.chelsea_self['iam']:

					if (iam == match1.group(2)):

						#Found agreement to what CHELSEA is in memory, answer back accordingly
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found agreement with 'I am'.")
						self.botReply(f"{random.choice(self.agree)}I am {match1.group(2)}")

						#Found agreement, break out of loop
						breakout = True
						break

				#If found agreement, return True	
				if (breakout):
					return True
				
				for iamnot in self.chelsea_self['iamnot']:

					if (iamnot == match1.group(2)):

						#Found disagreement to what CHELSEA is in memory, answer back accordingly
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found disagreement with 'I am'.")
						self.botReply(f"{random.choice(self.disagree)}I am not {match1.group(2)}")
						
						#Found disagreement, break out of loop
						breakout = True
						break
					
				#If found disagreement, return True	
				if (breakout):
					return True
				
				#What CHELSEA 'is' not found in memory, add identity of new 'is' to memory
				if (not(re.search(r"are you[a-z ]*\?*", self.user_message))):
					self.chelsea_self['iam'].append(match1.group(2))		
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new 'I am'.")
			
			else:

				#'not' detected in message

				breakout = False
				for iamnot in self.chelsea_self['iamnot']:

					if (iamnot == match1.group(2)):

						#Found agreement with what CHLESEA is not in memory, answer back accordingly
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found agreement with 'I am not'.")
						self.botReply(f"{random.choice(self.agree)}I am not {match1.group(2)}")
						
						#Found agreement, break out of loop
						breakout = True
						break

				#If found agreement, return True	
				if (breakout):
					return True
				
				for iam in self.chelsea_self['iam']:

					if (iam == match1.group(2)):

						#Found disagreement with what CHELSEA is not in memory, answer back accordingly
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found disagreement with 'I am not'.")
						self.botReply(f"{random.choice(self.disagree)}I am {match1.group(2)}")
						
						#Found disagreement, break out of loop
						breakout = True
						break

				#Found disagreement, return True	
				if (breakout):
					return True
				
				#What CHELSEA 'is not' not found in memory, add identity of new 'is not' to memory
				if (not(re.search(r"are you[a-z '\-]*\?*", self.user_message))):
					self.chelsea_self['iamnot'].append(match1.group(2))		
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new 'I am not'.")
		
		#CHELSEA 'is/is not' message not found, or learned new 'is/is not'
		return False

	def filter_user_reply(self):
		
		#Filter certain chars from userMessage
		self.user_message = re.sub(r"([^a-z0-9, \"'\-\?!/])", '', self.user_message)

	def get_exclaim_count(self):
		
		#Detect exclamation points at end of user_message to add emotional emphasis (Multiply emotion word counts by (self.exclaim_count + 1))
		
		self.exclaim_count = 1
		exclaim_match = re.search(r"(!+)$", self.user_message)
		
		if (exclaim_match):

			#Exclamation points detected at end of message
		
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Exclamation detected, exclaim count: {len(exclaim_match.group(1))}")

			#Get counts of exclamation points + 1 (Always non-zero for multiplication)
			self.exclaim_count = len(exclaim_match.group(1)) + 1

	def split_user_reply(self):
		
		#Filter out punctuation from user message and split to list of words
		self.message_words = (re.sub(r"([^a-z0-9 '\-])", '', self.user_message)).split(" ")

	def reset_temp_vars(self):
		
		#Reset these variables after the emotions of each message is processed, for the next use

		self.unknown_words = []
		self.reply_mood = {"mood": "happy", "happy": 0, "angry": 0, "sad": 0, "afraid": 0}
		self.word_emotions = ""
	
	def detect_emotion_words(self):

		#Detect emotion words, get reply mood, add user reply emotional values to CHELSEA's emotional values

		for word in self.message_words:
		
			if word == '':
				continue
		
			try:
		
				if (self.dictionary[word]['emotion'] != "permanent neutral" and self.dictionary[word]['emotion'] != "temp neutral"):

					#Word not neutral, for each emotion, add dictionary word emotion times exclaim count to reply mood and user mood

					for emotion in self.nEmotions:

						self.reply_mood[emotion] += (self.dictionary[word][emotion] * self.exclaim_count)
						self.user_self[emotion] += (self.dictionary[word][emotion] * self.exclaim_count)

					#Use this for the extended chatlog to show the detected emotions of each word in the user message
					self.word_emotions = f"{self.word_emotions}{self.dictionary[word]['emotion']} "
		
				else: 
		
					#Word is neutral, show this
					self.word_emotions = f"{self.word_emotions} neutral "
		
			except(KeyError):
		
				#Unknown word detected, add to list of unknown words for processing after determining reply mood
				self.unknown_words.append(word)
				self.word_emotions = f"{self.word_emotions} unknown "
		
		#Display the list of emotions for each word from the user reply in the extended chatlog
		self.Xchatlog.append(f"Word emotions in previous reply: {self.word_emotions}")

	def detect_unknown_words(self):
		
		#Mark unknown words in the emotion dictionary according to the overall mood of the user reply
		
		if len(self.unknown_words) > 0:

			#Detected unknown words
		
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Unknown words detected: {self.unknown_words}")
		
			for word in self.unknown_words:

				#Add unknown words to dictionary, set them to same emotion as the mood of the reply		
				self.dictionary[word] = {'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0, 'emotion': "", 'seen': 0, 'associated': {}}
				self.dictionary[word]['emotion'] = self.reply_mood["mood"] 
		
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned unknown words as '{self.reply_mood["mood"]}' words.")
		
			for word in self.unknown_words:
		
				#Create list of 'what is/are ____?' questions for the newly learned words
				self.unanswered_questions["what"][f"what is/are {word}?"] = ''
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned unknown words as unanswered questions")

	def add_to_word_counts(self):
		
		#Add to counts for each word
		
		for word in self.message_words:
		
			try:
		
				if (self.dictionary[word]['emotion'] == 'permanent neutral'):

					#Ignore if neutral word
					continue
		
			except(KeyError):

				#Word does not exist in dictionary
				continue
		
			#Increase counts for the word's mood and how many times it has been seen
			self.dictionary[word][self.reply_mood["mood"]] += 1 * self.exclaim_count
			self.dictionary[word]["seen"] += 1
		
			#Use a temporary dictionary to get the mood of the word
			temp_dict = { 'happy': self.dictionary[word]['happy'], 'angry': self.dictionary[word]['angry'], 'sad': self.dictionary[word]['sad'], 'afraid': self.dictionary[word]['afraid'] }
			word_emotion = self.getMood2(temp_dict, False)
		
			if (word_emotion != self.dictionary[word]['emotion']):
		
				#Detected change in definition of mood for the word, apply the new mood to it
				self.dictionary[word]['emotion'] = word_emotion
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Switched emotion of word '{word}' to {word_emotion}")

	def mark_associated_words(self):
		
		#Mark associated words in list
		
		for word in self.message_words:
		
			try:
		
				if (self.dictionary[word]['emotion'] == 'permanent neutral' or self.dictionary[word]['emotion'] == 'temp neutral'):

					#Ignore neutral words
					continue
		
			except(KeyError):

				#Unknown word detected
				continue
		
			for word2 in self.message_words:
		
				if (word == word2):

					#Ignore when both words are the same, no need to associate word with itself
					continue
		
				try:
		
					if (self.dictionary[word2]['emotion'] == 'permanent neutral' or self.dictionary[word2]['emotion'] == 'temp neutral'):

						#Ignore neutral words
						continue
		
				except(KeyError):

					#Unknown word detected
					continue
		
				try:
		
					#Detected word2 already has an association with word, add to counts
					self.dictionary[word]['associated'][word2] += 1
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Added to count of association of {word} and {word2}")
					continue
		
				except(KeyError):
		
					#Detected word2 has never been associated with word, start new count
					self.dictionary[word]['associated'][word2] = 1
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned association of {word} and {word2}")
					continue

	def get_bigrams2(self):
		
		#Identify new bigrams or add to counts of existing ones
		
		for n in range(len(self.message_words)):
		
			if n != len(self.message_words) - 1:

				#If at end of message words, no more bigrams to detect
		
				words = [self.message_words[n], self.message_words[n+1]]

				if words[0] not in self.bigrams:

					#Bigram doesn't exist in dictionary
					self.bigrams[words[0]] = {}
					self.bigrams[words[0]][words[1]] = 0
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new bigram: '{self.message_words[n]} {self.message_words[n+1]}'")

				if words[1] not in self.bigrams[words[0]]:

					#Second word of bigram doesn't exist in dictionary
					self.bigrams[words[0]][words[1]] = 1
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new bigram: '{self.message_words[n]} {self.message_words[n+1]}'")

				else:

					#bigram exists in dictionary, add to count of times seen
					self.bigrams[words[0]][words[1]] += 1

				if words[1] not in self.reverse_bigrams:

					#Reverse bigram not found in dictionary
					self.reverse_bigrams[words[1]] = {}
					self.reverse_bigrams[words[1]][words[0]] = 0
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new reverse bigram: '{self.message_words[n+1]} {self.message_words[n]}'")				

				if words[0] not in self.reverse_bigrams[words[1]]:

					#Second word of reverse bigram doesn't exist in dictionary
					self.reverse_bigrams[words[1]][words[0]] = 1
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new reverse bigram: '{self.message_words[n+1]} {self.message_words[n]}'")	

				else:

					#reverse bigram exists in dictionary, add to count of times seen
					self.reverse_bigrams[words[1]][words[0]] += 1

	def get_trigrams2(self):
		
		#Identify new trigrams or add to counts of existing ones
		
		for n in range(len(self.message_words)):
		
			if n != 0 and n != len(self.message_words) - 1:

				#If at end of message words, no more trigrams to detect
		
				words = [self.message_words[n-1], self.message_words[n], self.message_words[n+1]]
				
				if not f"{words[0]} {words[1]}" in self.trigrams:

					#trigram not found in dictionary
					self.trigrams[f"{words[0]} {words[1]}"] = {}
					self.trigrams[f"{words[0]} {words[1]}"][words[2]] = 0
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new trigram: '{self.message_words[n-1]} {self.message_words[n]} {self.message_words[n+1]}'")

				if words[2] not in self.trigrams[f"{words[0]} {words[1]}"]:

					#Third word of trigram doesn't exist in dictionary
					self.trigrams[f"{words[0]} {words[1]}"][words[2]] = 1
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new trigram: '{self.message_words[n-1]} {self.message_words[n]} {self.message_words[n+1]}'")

				else:

					#trigram found in dictionary, add to count of times seen
					self.trigrams[f"{words[0]} {words[1]}"][words[2]] += 1

				if not f"{words[1]} {words[2]}" in self.reverse_trigrams:

					#Reverse trigram not found in dictionary
					self.reverse_trigrams[f"{words[1]} {words[2]}"] = {}
					self.reverse_trigrams[f"{words[1]} {words[2]}"][words[0]] = 0
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new reverse trigram: '{self.message_words[n-1]} {self.message_words[n]} {self.message_words[n+1]}'")
				
				if words[0] not in self.reverse_trigrams[f"{words[1]} {words[2]}"]:

					#Third word of reverse trigram doesn't exist in dictionary
					self.reverse_trigrams[f"{words[1]} {words[2]}"][words[0]] = 1
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new reverse trigram: '{self.message_words[n-1]} {self.message_words[n]} {self.message_words[n+1]}'")

				else:

					#Reverse trigram found in dictionary, add to count of times seen
					self.reverse_trigrams[f"{words[1]} {words[2]}"][words[0]] += 1

	def get_topic_counts(self):
		
		#Get counts for words in current conversation				
		
		for word in self.message_words:
		
			try:
		
				if (self.dictionary[word]['emotion'] == 'permanent neutral' or self.dictionary[word]['emotion'] == 'temp neutral'):
					
					#Ignore neutral words
					continue
		
			except(KeyError):

				#Ignore words not found in emotion dictionary
				continue
		
			try:
				#If word is already found in topics, add to its count
				self.topics[word] += (1 * self.exclaim_count)
		
			except(KeyError):
				#Word not already found in topics, create new count
				self.topics[word] = (1 * self.exclaim_count)

	def determine_current_topics(self):
		
		#Get current topics of the conversation by the highest counts
		
		if (not(len(self.topics) == 0)):

			#At least 1 topic word
		
			#Get the current topics by the ones with the maximum count for all words in the topics dictionary
			temp_highest = max(self.topics.values())
			self.current_topics = [k for k, v in self.topics.items() if v == temp_highest]
		
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Current topic(s) is/are {" & ".join(self.current_topics)}")

	def add_to_previous_pairs(self):
		
		#Add to previous pairs (For depth words)	
		self.previous_pairs.append([self.CHELSEA_previous_response, self.user_message])

		#Only keep 3 previous pairs, delete the oldest if >3
		if (len(self.previous_pairs) > 3):
			del self.previous_pairs[0]

	def get_depth_words(self):
		
		#Get depth words
		
		self.depth_words = []	
		if (len(self.previous_pairs) == 3):

			#List of previous pairs full at 3
		
			temp_depth_words = {}		
		
			for pair in self.previous_pairs:
		
				#Separate user messages and CHELSEA responses into lists of words
				temp_messages = (re.sub(r"([^a-z0-9 '\-])", '', pair[0])).split(" ")
				temp_responses = (re.sub(r"([^a-z0-9 '\-])", '', pair[1])).split(" ")
		
				for word1 in temp_messages:

					#Loop through words from user message
		
					try:
		
						if (self.dictionary[word1]['emotion'] == "permanent neutral" or self.dictionary[word1]['emotion'] == "temp neutral"):
							#Ignore neutral words
							continue
		
					except(KeyError):
						#Word not found in emotion dictionary, ignore
						continue
		
					for word2 in temp_responses:

						#Loop through words from CHELSEA response
		
						try:
		
							if (self.dictionary[word2]['emotion'] == "permanent neutral" or self.dictionary[word2]['emotion'] == "temp neutral"):
								#Ignore neutral words
								continue
		
						except(KeyError):
							#Word not found in emotion dictionary, ignore
							continue
		
						if (word1 == word2):

							#Found word that matched in both user message and CHELSEA response
							temp_depth_words[word1] = 1
		
			#Get all the words that matched in both
			self.depth_words = list(temp_depth_words.keys())
		
			if (len(self.depth_words) > 0):

				#Display these words in the extended chatlog only if at least 1 was detected
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Found depth words: {" ".join(self.depth_words)}")

	def get_popular_words(self):
		
		#Determine the lists of words for each emotion given highest 'seen' count
		
		for emotion in self.nEmotions:
		
			#Grab the words tied to a particular emotion
			words = [word for word in self.dictionary.keys() if self.dictionary[word]["emotion"] == emotion]
			
			#Get the list of popular words for a particular emotion by finding ones matching the seen count with the maximum seen count for that emotion
			temp_highest = max([self.dictionary[word]["seen"] for word in words])
			self.popular_words[emotion] = [word for word in words if self.dictionary[word]["seen"] == temp_highest]
	
	def learn_why_isare_question(self):
		
		#Detect if _1_ is/are _2_ pattern in previous user reply		
		
		if not(re.search(r'^why', self.user_message)):
		
			#Check if user reply makes claim that _1_ is/are _2_, grab relevant parts
			m1 = re.search(r'([a-z ,\'\-]+) (is|are) ([a-z ,\'\-]+)', self.user_message)
			is_match1 = ""
			is_are = ""
			is_match2 = ""
		
			if m1:
				#Matches pattern to _1_ is/are _2_
				is_match1 = m1.group(1)
				is_are = m1.group(2)
				is_match2 = m1.group(3)
		
			else:
				#User reply pattern not _1_ is/are _2_
				return

			#Grab messages/responses that may hold the same answer already		
			messages = [message for message in self.message_dict2["happy"].keys()]
			for response in self.message_dict2["happy"].values():
				messages.extend(response)
		
			if not(re.search(r'(because|as|as a result of|by cause of|by reason of|by virtue of|considering|due to|for the reason that|owing to|since|thanks to)', is_match2)):
		
				#User reply doesn't contain words showing explanation of _1_ is/are _2_
				because_match_found = False
		
				#Determine is _1_ is/are _2_ because/etc is found in memory (Answer to question)
				for message2 in messages:
		
					if not(re.search(r'^why', message2)):
						#Not asking question, so might be answering the question

						if message2.find(self.user_message) != -1:
							#Possible answer to question found to contain user's reply

							m1 = re.search(r'[a-z ,\'\-]+ (is|are) ([a-z ,\'\-]+)', message2)
							is_match3 = ""
		
							if m1:
								#Potential answer follows pattern
								is_are2 = m1.group(1)
								is_match3 = m1.group(2)
		
							else:
								#Potential answer doesn't follow pattern, move on to next potential answer
								continue
		
							if re.search(r'(because|as|as a result of|by cause of|by reason of|by virtue of|considering|due to|for the reason that|owing to|since|thanks to)', is_match3) and is_are == is_are2:
								#Potential answer does contain words signaling that it is an explanation, '_1_ is/are _2_ because/etc'
								because_match_found = True
								break
		
							else:
								#Potential answer doesn't contain proper words for answering question
								continue
		
				if not(because_match_found):
		
					#Attempt to see if question already exists
					try:
						self.unanswered_questions[f"why {is_are}"][f"why {is_are} {is_match1} {is_match2}?".replace("  ", " ")]
		
					#Answer to why _1_ is/are _2_ not found, add question
					except(KeyError):
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new 'why is/are' question: 'why {is_are} {is_match1} {is_match2}?'")
						self.unanswered_questions[f"why {is_are}"][f"why {is_are} {is_match1} {is_match2}?".replace("  ", " ")] = ""
								
			else:
				#Already have answer to what is/are question
				return

	def check_for_answer_what(self):
		
		#Check for answer to previous what is/are question
		
		if (self.unanswered["what"]):
			#Previously asked question 'what is/are ___?'
		
			question_word = re.search(r"what is/are ([a-z ,'\-]+)", self.CHELSEA_previous_response)
		
			if (question_word):
		
				#Grab the word or phrase that was asked about, see if user reply answers the question
				question_word = question_word.group(1)
				answer = re.search(re.compile(f"({question_word} (is|are) [a-z ,'\\-]+)"), self.user_message)
		
				if (answer):
					#User did answer 'what is/are' question
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Answered what is/are question.")
		
					#Replace 'is/are' in question with either 'is' or 'are' 
					temp_question = self.CHELSEA_previous_response
					self.CHELSEA_previous_response = re.sub(r"(is/are)", answer.group(2), self.CHELSEA_previous_response)
					self.message_dict2[self.reply_mood["mood"]][self.CHELSEA_previous_response] = []

					#Append answer as response to question 
					self.message_dict2[self.reply_mood["mood"]][self.CHELSEA_previous_response].append(self.user_message)
		
					#Delete question from unanswered questions
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Deleted unanswered what is/are question, have answer now.")
					del self.unanswered_questions["what"][temp_question]

					#Possibly learn new question from answer:
					self.learn_why_isare_question()
		
				else:
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Unanswered what is/are question still not answered, moving on.")		
		
		#Answer not found or invalid format to answer, forgetting question was asked
		self.unanswered["what"] = False

	def check_for_answer_why_general(self, isare):
		
		if re.search(r"that('s| is) ((not (proper|right|accurate|flawless|good|correct|acceptable|suitable))|(improper|inaccurate|flawed|incorrect|unacceptable|unsuitable)) grammar", self.user_message):
			#CHELSEA told question formed doesn't follow proper grammar pattern

			self.Xchatlog.append(f"{self.bot_name} (Thinking): Deleted unanswered why is question with improper grammar.")
			del self.unanswered_questions[f"why {isare}"][self.CHELSEA_previous_response]
		
			self.unanswered[f"why {isare}"] = False
		
			#Give random response from current mood
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Gave random response.")	
			self.CHELSEA_previous_response = self.botReply(random.choice(random.choice(list(self.message_dict2[self.current_mood["mood"]].values()))))
			return True
		
		#Question formed either follows proper gramar pattern or CHELSEA not corrected
		question_word = re.search(re.compile(f"why {isare} ([a-z ,'\\-]+)"), self.CHELSEA_previous_response)
		
		if (question_word):
		
			#Look for answer pattern to question in user reply
			question_words = question_word.group(1).replace(",", '').split(" ")
			question_words.append(isare)
			answer = re.search(r"([a-z ,'\-]+) (because|as|as a result of|by cause of|by reason of|by virtue of|considering|due to|for the reason that|owing to|since|thanks to)", self.user_message)
		
			if not(answer):
				#Answer to why is/are question pattern not found, forgetting question was asked
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Unanswered why {isare} question still not answered, moving on.")
				self.unanswered[f"why {isare}"] = False
				return False
		
			#Answer pattern found
			answer = answer.group(1)
			answer_not_found = False
		
			for word in question_words:
		
				if answer.find(word) == -1:
					
					#Word or phrase in question not found in user reply answer
					answer_not_found = True
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Unanswered why {isare} question still not answered, moving on.")
					break
		
			if not(answer_not_found):
		
				#Found answer to why is/are question, append answer as response to question
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Answered why {isare} question.")
				temp_question = self.CHELSEA_previous_response
				self.message_dict2[self.reply_mood["mood"]][self.CHELSEA_previous_response] = []
				self.message_dict2[self.reply_mood["mood"]][self.CHELSEA_previous_response].append(self.user_message)
		
				#Delete question from unanswered questions
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Deleted unanswered why {isare} question, have answer now.")
				del self.unanswered_questions[f"why {isare}"][temp_question]
		
			else:
				#Answer not found
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Unanswered why {isare} question still not answered, moving on.")

	def check_for_answer_why(self):
		
		#Check for answer to previous why is/are question
		#Uses 'check_for_answer_why_general' for each case, 'is' or 'are'
		
		if (self.unanswered["why is"]):
		
			#Why is
			if self.check_for_answer_why_general("is"):
				return True

		elif (self.unanswered["why are"]):
		
			#Why are 
			if self.check_for_answer_why_general("are"):
				return True
			
		self.unanswered["why is"] = False
		self.unanswered["why are"] = False
		
		return False

	def fuzzy_match(self, message, similarity_threshold):

		#Try to find a match to input message given a specified similarity threshold between 0% and 100%
 
		best_match = None
		highest_score = 0.0
		
		for temp_message in self.temp_message_keys:

			#Calculate a similarity score between 0.0 and 1.0
			score = SequenceMatcher(None, message, temp_message).ratio()
			
			if score > highest_score:

				#New highest score found
				
				temp_response = random.choice(self.message_dict2[self.current_mood['mood']][temp_message])
				
				#Only use if the chosen response is not the same as the input message
				if temp_response != message:
				
					highest_score = score
					best_match = temp_response
				
		#Only use if highest_score meets the similarity threshold specified in the 2nd argument of this method
		if highest_score >= similarity_threshold:
			return {
				'response': best_match,
				'score': highest_score
			}
			
		return None

	def give_clarification(self):

		self.temp_message_keys = list(self.message_dict2[self.current_mood["mood"]].keys())
		random.shuffle(self.temp_message_keys) #Note: This shuffled list is potentially re-used in other parts of the script
		
		#Check for question about previous message meaning
		
		meaning_match = re.search(r"(what (do you|does that) mean|(can you|(do you|can you) care to) clarify|i('m| am) confused|i do( not|n't) (understand|get( it)?)( what you mean| what (that|this) means)?|why (do|did) you (say|think) (that|this))\?*$", self.user_message)
		
		if (meaning_match):
			#Pattern asking for clarification on previous response found
		
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Found pattern of user asking for clarification, attempting to use fuzzy match to find relevant response to what I previously said.")			

			#Try to find message matching CHELSEA's previous response with similarity score of at least 70%
			fuzzy_response = self.fuzzy_match(self.CHELSEA_previous_response, 0.70)
			
			if fuzzy_response:

				#Match found, respond with the response paired to the matching message

				self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked to clarify previous response, gave corresponding response from fuzzy match with similarity {fuzzy_response['score'] * 100}%.")
				self.CHELSEA_previous_response = self.botReply(fuzzy_response['response'])
				
				return True				
		
		#Does not follow pattern asking for clarification, or couldn't find response relevant to previous response
		return False
	
	def ask_what_feel(self):
		
		#Ask what CHELSEA feels about ___
		feel_about_match = re.search(r"(?:how|what) do you (?:feel|think) (?:about|toward(?:s)?) ([a-z0-9, '\-]+)\?*$", self.user_message)
		
		if (feel_about_match):
		
			#Split words at end of user reply into a list
			feel_words = (re.sub(r"([^a-z0-9 '\-])", '', feel_about_match.group(1))).split(" ")
			temp_dict = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
		
			for word in feel_words:
		
				try:
					
					#Skip neutral words
					if (self.dictionary[word]['emotion'] == 'temp neutral' or self.dictionary[word]['emotion'] == 'permanent neutral'):
						continue
		
				except(KeyError):
					#Skip words not found in dictionary
					continue
		
				#Get the emotion counts for each word
				temp_dict[self.dictionary[word]['emotion']] += 1
		
			#Determine the mood tied to the words
			feel_emotion = self.getMood2(temp_dict, False)
		
			if (feel_emotion == 'temp neutral'):
		
				#Overall mood of words is neutral, respond accordingly
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Feel nothing.")
				self.CHELSEA_previous_response = self.botReply(f"i feel nothing about {feel_about_match.group(1)}")
				return True
		
			else:
		
				#Overall mood of words is tied to a cetain emotion, give appropriate response
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Have emotion to answer question.")
				self.CHELSEA_previous_response = self.botReply(f"i feel {feel_emotion} about {feel_about_match.group(1)}")
				return True
		
		#'How/what do you fell about ___' pattern not found in user reply
		return False
	
	def ask_if_like(self):
		
		#Ask do you like question
		
		like_match = re.search(r"^do you (like|love|enjoy|adore|appreciate|dislike|hate|loathe|detest|despise) ([a-z0-9, '\-]+)\?*$", self.user_message)
		
		if (like_match):
		
			#Prepare like words and dictionary of emotions to determine overall mood of what CHELSEA likes/dislikes
			like_terms = ['like', 'love', 'enjoy', 'adore', 'appreciate']
			dislike_terms = ['dislike', 'hate', 'loathe', 'detest', 'despise'] #Unused, maybe just remove?
			like_words = (re.sub(r"([^a-z0-9 '\-])", '', like_match.group(2))).split(" ")
			
			temp_dict = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
			
			for word in like_words:
			
				try:
			
					#Ignore neutral words
					if (self.dictionary[word]['emotion'] == 'temp neutral' or self.dictionary[word]['emotion'] == 'permanent neutral'):
						continue
			
				except(KeyError):
					#Ignore words not found in dictionary
					continue
			
				#Get the emotion counts for each word
				temp_dict[self.dictionary[word]['emotion']] += 1
			
			#Get the overall mood of the words
			like_emotion = self.getMood2(temp_dict, False)
			
			if (like_emotion != 'temp neutral'):
			
				#Overall mood not neutral
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Like or dislike match found.")
				like_dislike = ''
			
				found = False
				for term in like_terms:
					#Determine if asking 'like'
			
					if (like_match.group(1) == term):
			
						like_dislike = 'like'
						found = True
						break
			
				if (not(found)):
					#must be asking 'dislike', since 'like' word not found
					like_dislike = 'dislike' 
			
				#Found agreement with 'do you like/dislike ___', respond accordingly
				if ((like_emotion == 'happy' and like_dislike == 'like') or (like_emotion != 'happy' and like_dislike == 'dislike')):
					self.CHELSEA_previous_response = self.botReply(f"yes, i {like_match.group(1)} {like_match.group(2)}")
			
				#Found disagreement with 'do you like/dislike ___', respond accordingly
				elif ((like_emotion == 'happy' and like_dislike == 'dislike') or (like_emotion != 'happy' and like_dislike == 'like')):
					self.CHELSEA_previous_response = self.botReply(f"no, i don't {like_match.group(1)} {like_match.group(2)}")
			
				return True
			
			else:
			
				#Overall mood towards it is neutral, respond accordingly
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Neither like or dislike")
				self.CHELSEA_previous_response = self.botReply(f"i don't feel anything about {like_match.group(2)}")
				return True
		
		#Pattern in user reply not matching
		return False
	
	def ask_which_better(self):
		
		#Ask which is better, 1 or 2?
		
		better_match = re.search(r"(?:which|what) (?:is (?:better,? ?|best,? ?)|do you (?:like (?:better,? ?|best,? ?|more,? ?))) ([a-z0-9, '\-]+) or ([a-z0-9, '\-]+)\?*$", self.user_message)
		
		if (better_match):
		
			#Grab the first term and set up dictionary to find overall mood of term
			better_words1 = (re.sub(r"([^a-z0-9 '\-])", '', better_match.group(1))).split(" ")
			temp_dict1 = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
		
			for word in better_words1:
		
				try:
					#Ignore neutral words

					if (self.dictionary[word]['emotion'] == 'temp neutral' or self.dictionary[word]['emotion'] == 'permanent neutral'):
						continue
		
				except(KeyError):
					#Ignore words not found in dictionary
					continue
		
				#Add to counts of emotions for word
				temp_dict1[self.dictionary[word]['emotion']] += 1
		
			#Get overall mood of the words (term)
			better_emotion1 = self.getMood2(temp_dict1, False)

			#Grab the second term and set up dictionary to find overall mood of term
			better_words2 = (re.sub(r"([^a-z0-9 '\-])", '', better_match.group(2))).split(" ")
			temp_dict2 = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }
		
			for word in better_words2:
		
				try:
					#Ignore neutral words

					if (self.dictionary[word]['emotion'] == 'temp neutral' or self.dictionary[word]['emotion'] == 'permanent neutral'):
						continue
		
				except(KeyError):
					#Ignore words not found in dictionary
					continue
		
				#Add to counts of emotions for word
				temp_dict2[self.dictionary[word]['emotion']] += 1
		
			#Get overall mood of the words (2nd term)
			better_emotion2 = self.getMood2(temp_dict2, False)
			
			if (better_emotion1 == 'happy' and better_emotion2 == 'happy'):
		
				#CHELSEA likes both terms
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Found like both, determining which more.")
				happy_count1 = 0
				happy_count2 = 0
		
				#Get counts of happy association for 1st term
				for word in better_words1:
					happy_count1 += self.dictionary[word]['happy']
		
				#Get counts of happy association for 2nd term
				for word in better_words2:
					happy_count2 += self.dictionary[word]['happy']
		
				if (happy_count1 > happy_count2):
					#1st term has higher happy association, respond accordingly

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Determined I like first option better.")
					self.CHELSEA_previous_response = self.botReply(f"i like both, but {better_match.group(1)} most")
					return True
		
				elif (happy_count2 > happy_count1):
					#2nd term has higher happy association, respond accordingly
					
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Determined I like second option better.")
					self.CHELSEA_previous_response = self.botReply(f"i like both, but {better_match.group(2)} most")
					return True
		
				else:	
					#Both terms have equal happy association, respond accordingly

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Determined I like both equally.")
					self.CHELSEA_previous_response = self.botReply(f"i like both {better_match.group(1)} & {better_match.group(2)} the same")
					return True
		
			elif (better_emotion1 == 'happy' and better_emotion2 != 'happy'):
				#CHELSEA likes 1st term, not 2nd, respond accordingly

				self.Xchatlog.append(f"{self.bot_name} (Thinking): Found like first.")
				self.CHELSEA_previous_response = self.botReply(f"i like {better_match.group(1)} better ")
				return True
		
			elif (better_emotion1 != 'happy' and better_emotion2 == 'happy'):
				#CHELSEA likes 2nd term, not 1st, respond accordingly

				self.Xchatlog.append(f"{self.bot_name} (Thinking): Found like second.")
				self.CHELSEA_previous_response = self.botReply(f"i like {better_match.group(2)} better ")
				return True
		
			elif (better_emotion1 != 'happy' and better_emotion2 != 'happy'):
				#CHELSEA doesn't like either term, resond accordingly
				
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Like neither.")
				self.CHELSEA_previous_response = self.botReply(f"i don't prefer either {better_match.group(1)} or {better_match.group(2)}")
				return True
		
		#User reply pattern doesn't match 'like more' question
		return False
	
	def ask_why_is(self):
		
		#Check for 'why is/are' question match
		
		response_made = False
		whyis_match = re.search(r"why (?:is|are) ([a-z0-9, '\-]+)\?*$", self.user_message)
		
		if (whyis_match):
		
			#Split words in 'why is/are' question into a list
			whyis_words = (re.sub(r"([^a-z0-9 '\-])", '', whyis_match.group(1))).split(" ")
			temp_message_values = list(self.message_dict2[self.current_mood["mood"]].values())
			random.shuffle(temp_message_values)

			#Check values
			for message in temp_message_values:
		
				#Grab a random response value from the message, see if it matches as a valid answer to the question
				message = random.choice(message)
				because_match = re.search(r"([a-z0-9, '\-]+) (because|as|as a result of|by cause of|by reason of|by virtue of|considering|due to|for the reason that|owing to|since|thanks to)", message)
		
				if (because_match):
					match_count = 0
		
					for word in whyis_words:
						#Loop through the words from the user question and see if they are all found in the potential answer
		
						if ((because_match.group(1)).find(word) != -1):
							match_count += 1
		
						else:
							break
		
						if (match_count == len(whyis_words)):
		
							#All words in question match the words in answer, respond accordingly
							#Kind of loose, may not be actual valid answer to the question, no fact checking is done, and words in answer may not be in same order as words in question
							self.Xchatlog.append(f"{self.bot_name} (Thinking): Possible answer to 'why is' question match found in values for: {" ".join(whyis_words)}")
							self.CHELSEA_previous_response = self.botReply(message)
							response_made = True
							break
		
					if response_made:
						break
		
			if response_made:
				return True
			
			#Check keys
			for message in self.temp_message_keys:
		
				because_match = re.search(r"([a-z0-9, '\-]+) (because|as|as a result of|by cause of|by reason of|by virtue of|considering|due to|for the reason that|owing to|since|thanks to)", message)
		
				if (because_match):
		
					match_count = 0
					for word in whyis_words:
						#Loop through the words from the user question and see if they are all found in the potential answer

						if ((because_match.group(1)).find(word) != -1):
							match_count += 1
		
						else:
							break
		
						if (match_count == len(whyis_words)):
		
							#All words in question match the words in answer, respond accordingly
							#Kind of loose, may not be actual valid answer to the question, no fact checking is done, and words in answer may not be in same order as words in question
							self.Xchatlog.append(f"{self.bot_name} (Thinking): Possible answer to 'why is' question match found in keys for: {" ".join(whyis_words)}")
							self.CHELSEA_previous_response = self.botReply(message)
							response_made = True
							break
		
					if response_made:
						break
		
			if response_made:
				return True
		
		#User reply did not match pattern for 'why is/are' question
		return False
	
	def ask_most_question(self):
		
		#Ask 'most' question		
		
		max1 = []
		temp_emotion = ''

		#See if asking most happy question
		happy_words = ['happy', 'contented', 'content', 'cheerful', 'cheery', 'merry', 'joyful', 'jovial', 'jolly', 'gleeful', 'delighted', 'joyous', 'thrilled', 'exuberant', 'elated', 'exhilarated', 'ecstatic', 'blissful', 'overjoyed']
		m1 = re.search(re.compile(f"what makes you most ({"|".join(happy_words)})\\?*$"), self.user_message)		
		if (m1):
		
			max1 = self.getMost(self.dictionary, 'happy')
			temp_emotion = 'happy'

		#See if asking most angry question
		angry_words = ['angry', 'frustrated', 'irate', 'vexed', 'irritated', 'exasperated', 'indignant', 'aggrieved', 'irked', 'piqued', 'displeased', 'provoked', 'galled', 'resentful', 'furious', 'enraged', 'infuriated', 'raging', 'incandescent', 'wrathful', 'fuming', 'ranting', 'raving', 'seething', 'frenzied', 'beside oneself', 'outraged', 'choleric', 'crabby', 'waspish', 'hostile', 'antagonistic', 'mad', 'livid', 'boiling', 'riled', 'aggravated', 'sore', 'ticked off', 'ill-tempered', 'acrimonious']
		m1 = re.search(re.compile(f"what makes you most ({"|".join(angry_words)})\\?*$"), self.user_message)	
		if (m1):
		
			max1 = self.getMost(self.dictionary, 'angry')
			temp_emotion = 'angry'
		
		#See if asking most sad question		
		sad_words = ['sad', 'unhappy', 'sorrowful', 'depressed', 'downcast', 'miserable', 'glum', 'gloomy', 'dismal', 'blue', 'melancholy']
		m1 = re.search(re.compile(f"what makes you most ({"|".join(sad_words)})\\?*$"), self.user_message)
		if (m1):
		
			max1 = self.getMost(self.dictionary, 'sad')
			temp_emotion = 'sad'
		
		#See if asking most afraid question		
		afraid_words = ['afraid', 'frightened', 'scared', 'terrified', 'fearful', 'petrified', 'nervous', 'worried', 'panicky', 'timid', 'spooked']
		m1 = re.search(re.compile(f"what makes you most ({"|".join(afraid_words)})\\?*$"), self.user_message)	
		if (m1):
		
			max1 = self.getMost(self.dictionary, 'afraid')
			temp_emotion = 'afraid'	
		
		#'most' question continued: Get max(es) for emotional words, respond accordingly	
		if (len(max1) == 1):	
			#Only one word relevant to 'most _emotion_' question

			self.Xchatlog.append(f"{self.bot_name} (Thinking): Most {temp_emotion} match found.")
			self.CHELSEA_previous_response = self.botReply(f"{max1[0]} makes me most {temp_emotion}")
			return True
		
		elif (len(max1) > 1):
		
			#Many words relevant to 'most _emotion_' question, choose one at random
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Most {temp_emotion} matches found.")
			self.CHELSEA_previous_response = self.botReply(f"{random.choice(max1)} is one of many that makes me most {temp_emotion}")
			return True
		
		return False

	def answer_fuzzy_question(self):

		#Avoid catching same pattern that needs to be caught in 'recall_past_topic' method later on
		if re.search(r'(((do you (remember|recall) ?)?what (were|was|we) (we|i|were) (talking|conversing|gabbing) about ((?P<num_days>[0-9]+)|(?P<string_days>[a-z]+)) day(s)? (ago|before|prior( to today)?)))|((((?P<num_days2>[0-9]+)|(?P<string_days2>[a-z]+)) days (ago|before|prior( to today)?),? )what (were|was|we) (we|i|were) (talking|conversing|gabbing) about)\??', self.user_message):
			return False

		#Find if user likely asking a WH question
		question_match = re.search(r"(?P<question>.*?(who|what|when|where|why|which|how).*?\?)", self.user_message)
		
		if question_match:

			#Question pattern possibly found, try to find a fuzzy match to the question in memory

			self.Xchatlog.append(f"{self.bot_name} (Thinking): Found pattern of user asking 'WH' question, attempting to use fuzzy match to find relevant answer to similar question.")

			fuzzy_answer = self.fuzzy_match(question_match.group('question'), 0.75)
		
			if fuzzy_answer:

				#Fuzzy match found with at least 75% similarity, give one of the responses tied to the matching message
			
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked 'WH' question, gave corresponding answer to response from fuzzy match with similarity {fuzzy_answer['score'] * 100}%.")
				self.CHELSEA_previous_response = self.botReply(fuzzy_answer['response'])
			
				return True

		return False

	def get_random_word(self, word_type):

		#For use in various parts where choosing random synonyms of words from a list is better than giving the same generic response

		return random.choice(self.synonym_lists[word_type])
	
	def get_joined_list(self, list_type):

		#For use in regular expressions
		
		return "|".join(self.synonym_lists[list_type])

	def ask_user_details(self):

		#Don't enter this method if question already asked
		if self.asked_question['question type'] != 'None':
			return False

		patterns = [
			re.compile(f"^my ((top|most|number one) )?({self.get_joined_list('favorite')}) (?P<topic>{self.get_joined_list('topics')}) is (?P<info>[a-z0-9 \\-']+)"),
			re.compile(f"^(?P<info>[a-z0-9 \\-']+) is my ((top|most|number one) )?({self.get_joined_list('favorite')}) (?P<topic>{self.get_joined_list('topics')})"),
			re.compile(f"^i like ([a-z0-9 \\-']+ )?(?P<topic>{self.get_joined_list('topics')})(s|es)?, but (?P<info>[a-z0-9 \\-']+) is my ((top|most|number one) )?({self.get_joined_list('favorite')})"),
			re.compile(f"^of all the (?P<topic>{self.get_joined_list('topics')})(s|es)?( [a-z0-9 \\-']+)?, my ((top|most|number one) )?({self.get_joined_list('favorite')}) is (?P<info>[a-z0-9 \\-']+)"),
			re.compile(f"^i ((?!do not|don't)[a-z0-9 \\-',]+ )?(((?P<dislike>{self.get_joined_list('dislike')})|(?P<like>{self.get_joined_list('like')}))) ((the )?(?P<topic>{self.get_joined_list('topics')}) )?(?P<info>[a-z0-9 \\-',]+)"),
			re.compile(f"^(?P<info>[a-z0-9 \\-',]+) (is|are) (([a-z0-9 \\-'])|(((the|a|an) )?(?P<topic>{self.get_joined_list('topics')}) ))? i((?!do not|don't) [a-z0-9 \\-']+)? (((?P<dislike>{self.get_joined_list('dislike')})|(?P<like>{self.get_joined_list('like')})))"),
			re.compile(f"^i ((?!do not|don't)[a-z0-9 \\-',]+ )?(((?P<have_not>{self.get_joined_list('have not')})|(?P<have>{self.get_joined_list('have')}))) (?P<info>[a-z0-9 \\-',]+)"),
			re.compile(f"^(?P<info>[a-z0-9 \\-',]+) (is|are) (([a-z0-9 \\-'])|(the|a|an) )? i((?!do not|don't) [a-z0-9 \\-']+)? (((?P<have_not>{self.get_joined_list('have not')})|(?P<have>{self.get_joined_list('have')})))"),
			re.compile(f"^i ((?P<am_not>am not)|(?P<am>am)) (?P<info>[a-z0-9 \\-',]+)"),
			re.compile(f"^(?P<info>[a-z0-9 \\-',]+?) is ([a-z0-9 \\-']+ )?i ((?P<am_not>am not)|(?P<am>am))")
		]

		#Detect last user reply fitting the pattern 'i like _', 'my favorite _ is _', etc.
		#If match, return from this method without doing anything (To let fall through to next)
		for pattern in patterns:
			if re.search(pattern, self.user_message):
				return False
			
		if random.randint(1, 12) == 1:
			
			whats = ['what is', 'what\'s', 'wut is']

			dice_roll = random.randint(1, 6)

			if dice_roll in {1, 2, 3}:

				#Get a list of the favorite topics that have no information yet
				unanswered_favorites = []
				for topic in self.synonym_lists['topics']:

					if len(self.user_self['favorite'][topic]) == 0:
						unanswered_favorites.append(topic)

				if len(unanswered_favorites) != 0:

					#Randomly choose one of the favorite topics with no information and ask question about it

					selected_topic = random.choice(unanswered_favorites)
					what_question = f"{random.choice(whats)} {random.choice(['your', 'yo', 'ur'])} favorite {selected_topic}?"
					
					self.asked_question = {
						'question type': 'what favorite',
						'info': '',
						'info type': selected_topic,
						'why': '',
						'date': '',
						'index': 0
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked about user's favorite that i don't yet know.")
					self.CHELSEA_previous_response = self.botReply(what_question)
					return True					

				else:

					#Get a list of the 'like' topics that have no information yet
					
					unanswered_likes = []
					for topic in self.synonym_lists['topics']:

						if len(self.user_self['like'][topic]) == 0:
							unanswered_likes.append(topic)

					if len(unanswered_likes) != 0:

						#Randomly choose one of the 'like' topics with no information and ask question about it

						selected_topic = random.choice(unanswered_likes)
						what_question = f"what {selected_topic} do you {self.get_random_word('like')}?"
						
						self.asked_question = {
							'question type': 'what like',
							'info': '',
							'info type': selected_topic,
							'why': '',
							'date': '',
							'index': 0
						}

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked about user's likes that i don't yet know.")
						self.CHELSEA_previous_response = self.botReply(what_question)
						return True	
					
					else:

						#Ask question about what the user likes/dislikes in general, no specific topic

						likeness = 'like' if random.randint(1, 2) == 1 else 'dislike'

						what_question = f"what do you {self.get_random_word(likeness)}?"
						
						self.asked_question = {
							'question type': f"what {likeness}",
							'info': '',
							'info type': '',
							'why': '',
							'date': '',
							'index': 0
						}

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked about user's {likeness}s that i don't yet know.")
						self.CHELSEA_previous_response = self.botReply(what_question)
						return True	

			elif dice_roll in {4, 5}:

				#Build list of favorite topics that have an entry in information but lack the 'why' part
				
				unanswered_why = []
				for topic in self.synonym_lists['topics']:

					index = 0
					for entry in self.user_self['favorite'][topic]:

						if entry['why'] == '':
							unanswered_why.append([entry, index, topic])

						index += 1

				if len(unanswered_why) != 0:

					#Randomly select one of the favorite topics to ask 'why is _ your favorite _?'

					selected_entry = random.choice(unanswered_why)

					info = selected_entry[0]['info']
					topic = selected_entry[2]

					self.asked_question = {
						'question type': 'why favorite',
						'info': info,
						'info type': topic,
						'why': '',
						'date': selected_entry[0]['date'],
						'index': selected_entry[1]
					}

					responses = [
						f"why is your {self.get_random_word('favorite')} {topic} {info}?",
						f"why is {info} your {self.get_random_word('favorite')} {topic}?",
						f"{self.get_random_word('confirmation')} why is your {self.get_random_word('favorite')} {topic} {info}?",
						f"{self.get_random_word('confirmation')} why is {info} your {self.get_random_word('favorite')} {topic}?",
					]

					self.Xchatlog.append(f"{self.bot_name} (Thinking): The 'why' about user's favorite not found, asking 'why' it is their favorite.")
					self.CHELSEA_previous_response = self.botReply(random.choice(responses))
					self.user_gave_details = True

					return True
				
				else:

					#Build list of like/dislike with no 'why' info part filled in

					likeness = 'like' if random.randint(1, 2) == 1 else 'dislike'

					unanswered_why = []
					for topic in self.synonym_lists['topics']:

						index = 0
						for entry in self.user_self[likeness][topic]:

							if entry['why'] == '':
								unanswered_why.append([entry, index, topic])

							index += 1

					if len(unanswered_why) != 0:

						#Select one of the likes/dislikes at random and ask question of 'why do you like/dislike _?'

						selected_entry = random.choice(unanswered_why)

						info = selected_entry[0]['info']
						topic = selected_entry[2]

						self.asked_question = {
							'question type': f"why {likeness}",
							'info': info,
							'info type': topic,
							'why': '',
							'date': selected_entry[0]['date'],
							'index': selected_entry[1]
						}

						responses = [
							f"why do you {self.get_random_word(likeness)} {info}?",
							f"why is {info} something you {self.get_random_word(likeness)}?",
							f"{self.get_random_word('confirmation')} why do you {self.get_random_word(likeness)} {info}?",
							f"{self.get_random_word('confirmation')} why is {info} something you {self.get_random_word(likeness)}?",
						]

						self.Xchatlog.append(f"{self.bot_name} (Thinking): The 'why' about user's {likeness}s not found, asking 'why' they {likeness} it.")
						self.CHELSEA_previous_response = self.botReply(random.choice(responses))
						self.user_gave_details = True

						return True		
			
					else:

						return False
			else:

				#Build list of existing 'likes'
				
				answered_likes = []
				for topic in self.synonym_lists['topics']:

					if len(self.user_self['like'][topic]) != 0:
						answered_likes.append(topic)

				if len(answered_likes) != 0:

					#Given a randomly selected 'LIKE', ask question 'besides LIKE, what _ do you like?'

					selected_topic = random.choice(answered_likes)
					what_question = f"{self.get_random_word('besides')} {random.choice(self.user_self['like'][selected_topic])['info']}, what {selected_topic} do you {self.get_random_word('like')}?"
					
					self.asked_question = {
						'question type': 'what like',
						'info': '',
						'info type': selected_topic,
						'why': '',
						'date': '',
						'index': 0
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked about user's likes that i don't yet know, besides one already known.")
					self.CHELSEA_previous_response = self.botReply(what_question)
					return True		

	def confirm_user_details_what(self):
		
		if self.asked_question['question type'] != 'None':

			#Don't enter this method if question not asked
			
			if self.asked_question['question type'] == 'what favorite':

				#Question 'what is your favorite _?' previously asked
				
				patterns = [
					re.compile(f"^my ((top|most|number one) )?({self.get_joined_list('favorite')}) (?P<topic>{self.get_joined_list('topics')}) is (?P<info>[a-z0-9 \\-']+)"),
					re.compile(f"^(?P<info>[a-z0-9 \\-']+) is my ((top|most|number one) )?({self.get_joined_list('favorite')}) (?P<topic>{self.get_joined_list('topics')})"),
					re.compile(f"^i like ([a-z0-9 \\-']+ )?(?P<topic>{self.get_joined_list('topics')})(s|es)?, but (?P<info>[a-z0-9 \\-']+) is my ((top|most|number one) )?({self.get_joined_list('favorite')})"),
					re.compile(f"^of all the (?P<topic>{self.get_joined_list('topics')})(s|es)?( [a-z0-9 \\-']+)?, my ((top|most|number one) )?({self.get_joined_list('favorite')}) is (?P<info>[a-z0-9 \\-']+)")
				] #Add more of these later
			
				for pattern in patterns:

					if re.search(pattern, self.user_message):

						self.asked_question = {
							'question type': 'None',
							'info': '',
							'info type': 'None',
							'why': '',
							'date': '',
							'index': 0
						}

						return #Fits format for giving details of favorite, just let fall through to next methods
					
				#'_HAVE_NOT_ favorite _TOPIC_'	
				if re.search(re.compile(f"({self.get_joined_list('have not')}) ((a|an|the|any) )?favorite {self.asked_question['info type']}"), self.user_message):

					#This actually falls through if give an 'i don't have _' reply. Not the intended behavior, but it does seem to make sense to add it to the list of stuff the user doesn't have?
					#I think I will keep it for now, though it may cause trouble later on.
					self.Xchatlog.append(f"{self.bot_name} (Thinking): User said they don't have a favorite {self.asked_question['info type']}, moving on.")
				
				else:
					
					#Modify user message to force format and then fall through into the next methods to process
					
					#! Problem: could give answer like 'favorite is _', '_ for sure', etc.
					#! This would lead to messed up responses. Patterns may still match, but it can cause unexpected results.
					#! Try this instead:
					self.user_message = re.sub(re.compile(f"(({self.get_joined_list('favorite')}) ?)?({self.asked_question['info type']} ?)?((is|are) ?)?"), '', self.user_message)
					#! Works for now, but is ignoring many other possible patterns the user could say

					self.user_message = f"my favorite {self.asked_question['info type']} is {self.user_message}"

					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': '',
						'index': 0
					}

					self.fall_through = True
					
					return

			elif self.asked_question['question type'] in {'what like', 'what dislike'}:

				patterns = [
					re.compile(f"^i ((?!do not|don't)[a-z0-9 \\-',]+ )?(((?P<dislike>{self.get_joined_list('dislike')})|(?P<like>{self.get_joined_list('like')}))) ((the )?(?P<topic>{self.get_joined_list('topics')}) )?(?P<info>[a-z0-9 \\-',]+)"),
					re.compile(f"^(?P<info>[a-z0-9 \\-',]+) (is|are) (([a-z0-9 \\-'])|(((the|a|an) )?(?P<topic>{self.get_joined_list('topics')}) ))? i((?!do not|don't) [a-z0-9 \\-']+)? (((?P<dislike>{self.get_joined_list('dislike')})|(?P<like>{self.get_joined_list('like')})))")
				]				
				
				for pattern in patterns:
					
					if re.search(pattern, self.user_message):
					
						return #Fits format for giving details of like/dislike, just let fall through to next methods
					
				#'_HAVE_NOT_ favorite _TOPIC_'	
				if re.search(re.compile(f"({self.get_joined_list('have not')}) ((any|an|a) ){self.asked_question['info type']}(s|es)? i (((?P<dislike>{self.get_joined_list('dislike')})|(?P<like>{self.get_joined_list('like')})))"), self.user_message):
					#! Need more patterns, so many more possibilities
					
					self.Xchatlog.append(f"{self.bot_name} (Thinking): User said they don't have any {self.asked_question['info type']}(s) they like/dislike, moving on.")
				
				else:
					
					#Modify user message to force format and then fall through into the next methods to process
					likeness = self.asked_question['question type'].split(" ")[1]

					self.user_message = re.sub(re.compile(f"(({self.get_joined_list(likeness)}) ?)?({self.asked_question['info type']} ?)?((is|are) ?)?({self.asked_question['info type']} ?)?"), '', self.user_message)
					#! Works for now, but is ignoring many other possible patterns the user could say

					self.user_message = f"i {likeness} the {self.asked_question['info type']} {self.user_message}"
				
				self.asked_question = {
					'question type': 'None',
					'info': '',
					'info type': 'None',
					'why': '',
					'date': '',
					'index': 0
				}
				
				return
			
			#Let 'why favorite' and 'why like/dislike' fall through to the other 'confirm' methods.
		
		return

	def determine_if_like(self, info):

		#Given the word or words in info, determine the emotion associated with them

		like_words = (re.sub(r"([^a-z0-9 '\-])", '', info)).split(" ")

		temp_dict = { 'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0 }

		for word in like_words:

			try:

				#Ignore neutral words
				if (self.dictionary[word]['emotion'] == 'temp neutral' or self.dictionary[word]['emotion'] == 'permanent neutral'):
					continue

			except(KeyError):
				#Ignore words not found in dictionary
				continue

			#Get the emotion counts for each word
			temp_dict[self.dictionary[word]['emotion']] += 1

		#Get the overall mood of the words
		like_emotion = self.getMood2(temp_dict, False)

		return 'happy' if like_emotion == 'temp neutral' else like_emotion
	
	def get_likeness_emotion(self, likeness, info):

		info_emotion = self.determine_if_like(info)
		
		if likeness == 'like':

			#If user likes _, increase the emotion tied to _ by 15

			self.current_mood[info_emotion] += 15

			self.adjust_mood()

			if info_emotion != 'happy':

				self.Xchatlog.append(f"{self.bot_name} (Thinking): Found user likes what makes me {info_emotion}.")
				return f"i don't like {info}, it makes me {info_emotion}"
			
			else:

				self.Xchatlog.append(f"{self.bot_name} (Thinking): Found user likes what makes me happy.")
				return None

		elif likeness == 'dislike':

			#If user dislikes _, increase angry and sad by 10 if emotion tied to _ is happy,
			#Else increase happy by 10 if _ is tied to non-happy emotion

			if info_emotion == 'happy':

				self.current_mood['angry'] += 10
				self.current_mood['sad'] += 10

				self.adjust_mood()

				self.Xchatlog.append(f"{self.bot_name} (Thinking): Found user dilikes what makes me happy.")
				return f"i happen to {self.get_random_word('like')} {info}..."

			else:

				self.current_mood['happy'] += 10

				self.adjust_mood()	

				self.Xchatlog.append(f"{self.bot_name} (Thinking): Found user dislikes what makes me {info_emotion}.")
				return None

		return None

	def ask_past_user_details(self):

		#Given information already in user file, if information is at least 14 days old, ask about it. ('do you still like _?')

		if self.asked_question['question type'] != 'None':

			#If a question was previously asked and awaiting an answer, don't enter this method
			
			return False

		if self.fall_through:

			#If the user message was previously modified to fit the pattern detected in another method, return from this method

			self.fall_through = False
			return False
		
		if random.randint(1, 12) == 1:
			
			dice_roll = random.randint(1, 4)

			if dice_roll == 1: #Favorite
				
				#Build list of existing favorites older than 14 days
				
				past_favorites = []
				for topic in self.synonym_lists['topics']:

					index = 0
					for favorite in self.user_self['favorite'][topic]:

						if self.date_difference.get_days_past(favorite['date']) >= 14:

							past_favorites.append({
								'favorite': favorite,
								'topic': topic,
								'index': index
							})
						
						index += 1

				if len(past_favorites) > 0:

					#Choose one of the existing favorites at random, ask if still favorite

					chosen_favorite = random.choice(past_favorites)

					topic = chosen_favorite['topic']

					self.asked_question = {
						'question type': 'asked past favorite',
						'info': chosen_favorite['favorite']['info'],
						'info type': topic,
						'why': '',
						'date': '',
						'index': chosen_favorite['index']
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked about user's past favorite.")
					self.CHELSEA_previous_response = self.botReply(f"{self.date_difference.get_time_range(chosen_favorite['favorite']['date'])} you said {chosen_favorite['favorite']['info']} was your {self.get_random_word('favorite')} {topic}, is it {self.get_random_word('still')} your {self.get_random_word('favorite')}?")
					
					return True
				
				else:

					#No existing favorites older than 14 days found

					return False
			
			elif dice_roll == 2: #like/dislike
				
				likeness = 'like' if random.randint(1, 3) in {1, 2} else 'dislike'

				#Build a list of existing likes/dislikes older than 14 days

				past_likes = []
				topics = list(self.synonym_lists['topics'])
				topics.append('general')
				for topic in topics:

					index = 0
					for like in self.user_self[likeness][topic]:

						if self.date_difference.get_days_past(like['date']) >= 14:

							past_likes.append({
								'like': like,
								'topic': topic,
								'index': index
							})
						
						index += 1

				if len(past_likes) > 0:

					#Randomly choose one of the existing likes/dislikes and ask 'N days/weeks/etc. ago you said you like/dislike _, do you still like/dislike _?'

					chosen_like = random.choice(past_likes)

					topic = chosen_like['topic']

					self.asked_question = {
						'question type': f"asked past {likeness}",
						'info': chosen_like['like']['info'],
						'info type': topic,
						'why': '',
						'date': '',
						'index': chosen_like['index']
					}

					topic = '' if topic == 'general' else f"the {topic} "

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked about user's past {likeness}.")
					self.CHELSEA_previous_response = self.botReply(f"{self.date_difference.get_time_range(chosen_like['like']['date'])} you said you {self.get_random_word(likeness)} {topic}{chosen_like['like']['info']}, do you {self.get_random_word('still')} {self.get_random_word(likeness)} that?")
					
					return True
				
				else:

					return False
			
			elif dice_roll == 3: #have
				
				#Build list of existing 'haves' older than 14 days

				past_haves = []

				index = 0
				for have in self.user_self['have']:

					if self.date_difference.get_days_past(have['date']) >= 14:

						past_haves.append({
							'have': have,
							'index': index
						})
					
					index += 1

				if len(past_haves) > 0:

					#Choose one of the 'haves' at random and ask user if they still have it ('N days/weeks/etc. ago you said you have _, do you still have _?')

					chosen_have = random.choice(past_haves)

					self.asked_question = {
						'question type': f"asked past have",
						'info': chosen_have['have']['info'],
						'info type': '',
						'why': '',
						'date': '',
						'index': chosen_have['index']
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked about user's past 'have'.")
					self.CHELSEA_previous_response = self.botReply(f"{self.date_difference.get_time_range(chosen_have['have']['date'])} you said you {self.get_random_word('have')} {chosen_have['have']['info']}, do you {self.get_random_word('still')} {self.get_random_word('have')} that?")
					
					return True
				
				else:

					return False				
			
			elif dice_roll == 4: #uam/uamnot
				
				amness = 'uam' if random.randint(1, 3) in {1, 2} else 'uamnot'

				#Build list of existing entries for what user is (uam) or is not (uamnot) older than 14 days

				past_ams = []

				index = 0
				for am in self.user_self[amness]:

					if self.date_difference.get_days_past(am['date']) >= 14:

						past_ams.append({
							'am': am,
							'index': index
						})
					
					index += 1

				if len(past_ams) > 0:

					#Randomly choose one of the entries about what user is or is not and ask if they still are or are not

					chosen_am = random.choice(past_ams)

					self.asked_question = {
						'question type': f"asked past {amness}",
						'info': chosen_am['am']['info'],
						'info type': '',
						'why': '',
						'date': '',
						'index': chosen_am['index']
					}

					are_string = 'are' if amness == 'uam' else 'are not'
					not_string = 'not ' if amness == 'uamnot' else ''

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked about user's past '{amness}'.")
					self.CHELSEA_previous_response = self.botReply(f"{self.date_difference.get_time_range(chosen_am['am']['date'])} you said you {are_string} {chosen_am['am']['info']}, are you {self.get_random_word('still')} {not_string}{chosen_am['am']['info']}?")
					
					return True
				
				else:

					return False
		
		return False

	def contradiction_anger(self, timestamp):

		#Add to angry count if contradiction made within 1 day
		#Adds 0-35 depending on how soon contradiction made
       
		past_time = datetime.strptime(timestamp, "%m/%d/%Y, %H:%M:%S")
		current_time = datetime.now()

		if (current_time - past_time).days == 0:

			time_difference = (current_time - past_time).total_seconds() / 60
		
			anger_increase = math.floor(abs(time_difference - 3600) / 100)
			self.current_mood['angry'] += anger_increase

			self.Xchatlog.append(f"{self.bot_name} (Thinking): Anger increased by {anger_increase} due to user changing their mind so rapidly.")

			self.adjust_mood()

		return
			
	def confirm_past_user_details(self):
		
		if self.asked_question['question type'] != 'None':

			#Don't enter this method unless a question was previously asked
						
			if self.asked_question['question type'] == 'asked past favorite':

				#Previously asked about user's existing favorite
						
				match = re.search(re.compile(f"(?<!in)({self.get_joined_list('yes')})"), self.user_message)
				if match: #'yes' answer

					topic = self.asked_question['info type']
					index = self.asked_question['index']

					#Update timestamp of existing favorite, important to not have CHELSEA repeatedly ask about the same item (Only asks if 14+ days old)
					self.user_self['favorite'][topic][index]['date'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
					
					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': '',
						'index': 0
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Confirmed user's past favorite.")
					self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
					
					return True
				
				else:
					match = re.search(re.compile(f"({self.get_joined_list('no')})"), self.user_message)
					if match: #'No' answer

						#Determined no longer user's favorite _, ask another question to find out what their new favorite _ is
						
						topic = self.asked_question['info type']
						index = self.asked_question['index']

						del self.user_self['favorite'][topic][index]

						self.asked_question['question type'] = 'what favorite'

						whats = ['what is', 'what\'s', 'wut is']
						what_question = f"then, {random.choice(whats)} {random.choice(['your', 'yo', 'ur'])} new favorite {topic}?"

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Forgot old favorite, asked about user's new favorite that i don't yet know.")
						self.CHELSEA_previous_response = self.botReply(what_question)
						
						return True	
					
					else: #Neither 'yes' or 'no' response
						
						#Not getting the needed yes/no response, forget the question and move on
						
						self.asked_question = {
							'question type': 'None',
							'info': '',
							'info type': 'None',
							'why': '',
							'date': '',
							'index': 0
						}

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Didn't get answer from user about past favorite, forgetting the question.")

						if random.randint(1, 4) == 1:

							self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
						
							return True
						
						else:

							return False

			elif self.asked_question['question type'] in {'asked past like', 'asked past dislike'}:

				#Previously asked about user's existing like/dislike

				likeness = self.asked_question['question type'].split(' ')[2]
						
				match = re.search(re.compile(f"(?<!in)({self.get_joined_list('yes')})"), self.user_message)
				if match: #'yes' answer

					topic = self.asked_question['info type']
					index = self.asked_question['index']

					#Update timestamp of existing like/dislike, important to not have CHELSEA repeatedly ask about the same item (Only asks if 14+ days old)
					self.user_self[likeness][topic][index]['date'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
					
					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': '',
						'index': 0
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Confirmed user's past favorite.")
					self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
					
					return True
				
				else:
					match = re.search(re.compile(f"({self.get_joined_list('no')})"), self.user_message)
					if match: #'No' answer
						
						#User said no longer like or dislike _, need to ask for clarification before flipping entry
						
						topic = self.asked_question['info type']
						topic = '' if topic == 'general' else f"the {topic} "

						self.asked_question['question type'] = f"changed mind past {likeness}"

						flipped_likeness = 'dislike' if likeness == 'like' else 'like'

						changed_mind_question = f"then, did you {self.get_random_word('change')} your {self.get_random_word('mind')}, do you {self.get_random_word(flipped_likeness)} {topic}{self.asked_question['info']} now?"

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked if user changed mind about {likeness}, {flipped_likeness} now?")
						self.CHELSEA_previous_response = self.botReply(changed_mind_question)
						
						return True	
					
					else: #Neither 'yes' or 'no' response

						#Didn't get needed yes/no response, forget question and move on
						
						self.asked_question = {
							'question type': 'None',
							'info': '',
							'info type': 'None',
							'why': '',
							'date': '',
							'index': 0
						}

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Didn't get answer from user about past {likeness}, forgetting the question.")

						if random.randint(1, 4) == 1:

							self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
						
							return True
						
						else:

							return False
		
			elif self.asked_question['question type'] in {'changed mind past like', 'changed mind past dislike'}:

				#Previously asked if user changed mind about thier like or dislike

				likeness = self.asked_question['question type'].split(' ')[3]
						
				match = re.search(re.compile(f"(?<!in)({self.get_joined_list('yes')})"), self.user_message)
				if match: #'yes' answer
					
					#If no longer like or no longer dislike, need to flip entry to the opposite (like -> dislike)

					topic = self.asked_question['info type']
					index = self.asked_question['index']
					flipped_likeness = 'dislike' if likeness == 'like' else 'like'
					
					#Add to angry count if changed mind within 1 day
					self.contradiction_anger(self.user_self[likeness][topic][index]['date'])

					del self.user_self[likeness][topic][index]

					self.user_self[flipped_likeness][topic].append({
						'info': self.asked_question['info'],
						'why': '',
						'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
					})
					
					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': '',
						'index': 0
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Confirmed user's change in mind about {likeness}, user {flipped_likeness}s that now.")
					self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
					
					return True
				
				else:

					#Not 'yes' answer, forget line of questions and move on
						
					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': '',
						'index': 0
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Didn't get 'yes' answer from user about changing mind about past {likeness}, forgetting the question.")

					if random.randint(1, 4) == 1:

						self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
					
						return True
					
					else:

						return False
					
			elif self.asked_question['question type'] in {'asked past have', 'asked past have_not'}:

				#Previously asked question about user's existing 'have' or 'have not'

				haveness = self.asked_question['question type'].split(" ")[2].replace('_', ' ')
						
				match = re.search(re.compile(f"(?<!in)({self.get_joined_list('yes')})"), self.user_message)
				if match: #'yes' answer
					
					#User confirmed they still 'have' or 'have not'

					index = self.asked_question['index']

					#Update timestamp to prevent asking about again for a while (14+ days)
					self.user_self[haveness][index]['date'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
					
					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': '',
						'index': 0
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Confirmed user still '{haveness}'.")
					self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
					
					return True
				
				else:
					match = re.search(re.compile(f"({self.get_joined_list('no')})"), self.user_message)
					if match: #'No' answer
						
						#User said they no longer 'have' or 'have not' _, ask further question for clarification

						self.asked_question['question type'] = f"changed past {haveness.replace(' ', '_')}"

						changed_have_question = f"then, do you no longer {self.get_random_word(haveness)} {self.asked_question['info']} now?"

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked if user no longer '{haveness}' something they '{haveness}'.")
						self.CHELSEA_previous_response = self.botReply(changed_have_question)
						
						return True	
					
					else: #Neither 'yes' or 'no' response
						
						#Neither yes/no, forget question and move on
						
						self.asked_question = {
							'question type': 'None',
							'info': '',
							'info type': 'None',
							'why': '',
							'date': '',
							'index': 0
						}

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Didn't get answer from user about past 'have', forgetting the question.")

						if random.randint(1, 4) == 1:

							self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
						
							return True
						
						else:

							return False
		
			elif self.asked_question['question type'] in {'changed past have', 'changed past have_not'}:

				#User previously said they no longer 'have' or 'have not', asked question for clarification

				haveness = self.asked_question['question type'].split(" ")[2].replace('_', ' ')
						
				match = re.search(re.compile(f"(?<!in)({self.get_joined_list('yes')})"), self.user_message)
				if match: #'yes' answer
					
					#User no longer has or has not _, flip entry for _ ('have' -> 'have not')

					index = self.asked_question['index']
					
					del self.user_self[haveness][index]

					flipped_haveness = 'have not' if haveness == 'have' else 'have'

					self.user_self[flipped_haveness].append({
						'info': self.asked_question['info'],
						'why': '',
						'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
					})
					
					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': '',
						'index': 0
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Confirmed user's change of '{haveness}', it is '{flipped_haveness}' now.")
					self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
					
					return True
				
				else:

					#Didn't get expected 'yes' response, forgetting question and moving on
						
					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': '',
						'index': 0
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Didn't get 'yes' answer from user about what they {haveness}, forgetting the question.")

					if random.randint(1, 4) == 1:

						self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
					
						return True
					
					else:

						return False

			elif self.asked_question['question type'] in {'asked past uam', 'asked past uamnot'}:

				#Previously asked question about existing user 'is' or 'is not'

				amness = self.asked_question['question type'].split(' ')[2]
						
				match = re.search(re.compile(f"(?<!in)({self.get_joined_list('yes')})"), self.user_message)
				if match: #'yes' answer
					
					#User confirmed they still 'are' or 'are not'

					index = self.asked_question['index']

					#Update timestamp to prevent repeat questions about it for 14+ days
					self.user_self[amness][index]['date'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
					
					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': '',
						'index': 0
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Confirmed user's past '{amness}'.")
					self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
					
					return True
				
				else:
					match = re.search(re.compile(f"({self.get_joined_list('no')})"), self.user_message)
					if match: #'No' answer
						
						#User said no longer 'is' or 'is not', ask further question for clarification

						self.asked_question['question type'] = f"changed mind past {amness}"

						flipped_amness = 'uamnot' if amness == 'uam' else 'uam'
						not_string = 'not ' if flipped_amness == 'uamnot' else ''

						changed_mind_question = f"then, did you {self.get_random_word('change')}, are you {not_string}{self.asked_question['info']} now?"

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked if user changed '{amness}', {flipped_amness} now?")
						self.CHELSEA_previous_response = self.botReply(changed_mind_question)
						
						return True	
					
					else: #Neither 'yes' or 'no' response

						#Neither yes/no, forget question and move on
						
						self.asked_question = {
							'question type': 'None',
							'info': '',
							'info type': 'None',
							'why': '',
							'date': '',
							'index': 0
						}

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Didn't get answer from user about past '{amness}', forgetting the question.")

						if random.randint(1, 4) == 1:

							self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
						
							return True
						
						else:

							return False
		
			elif self.asked_question['question type'] in {'changed mind past uam', 'changed mind past uamnot'}:

				#User previously said they no longer 'are' or 'are not', previously asked further question for clarification

				amness = self.asked_question['question type'].split(' ')[3]
						
				match = re.search(re.compile(f"(?<!in)({self.get_joined_list('yes')})"), self.user_message)
				if match: #'yes' answer

					#User confirmed they no longer 'are' or 'are not', flipping entry ('is' -> 'is not')

					index = self.asked_question['index']
					flipped_amness = 'uamnot' if amness == 'uam' else 'uam'

					#Add to angry count if changed mind within 1 day
					self.contradiction_anger(self.user_self[amness][index]['date'])
					
					del self.user_self[amness][index]

					self.user_self[flipped_amness].append({
						'info': self.asked_question['info'],
						'why': '',
						'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
					})
					
					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': '',
						'index': 0
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Confirmed user's change in '{amness}', user {flipped_amness} that now.")
					self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
					
					return True
				
				else:

					#Didn't get expected 'yes' answer, forgettig the line of questioning and moving on
						
					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': '',
						'index': 0
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Didn't get 'yes' answer from user about changing past '{amness}', forgetting the question.")

					if random.randint(1, 4) == 1:

						self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
					
						return True
					
					else:

						return False

			elif self.asked_question['question type'] in {'asked past contradiction favorite_dislike', 'asked past contradiction dislike_favorite'}:

				#User previously said a contradiction, either said a past dislike is their favorite, or their past favorite is a dislike
				#Was previously asked if they still disliked or was still their favorite

				contradiction_type = self.asked_question['question type'].split(' ')[3]
				old_entry, new_entry = contradiction_type.split('_')

				topic = self.asked_question['info type']
						
				match = re.search(re.compile(f"(?<!in)({self.get_joined_list('yes')})"), self.user_message)
				if match: #'yes' answer
					
					#User confirmed it is actually still a dislike or still their favorite,
					#Just update timestamp and give confirmation

					index = self.asked_question['index']

					self.user_self[old_entry][topic][index]['date'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
					
					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': '',
						'index': 0
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Confirmed user's past '{old_entry}'.")
					self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
					
					return True
				
				else:
					match = re.search(re.compile(f"({self.get_joined_list('no')})"), self.user_message)
					if match: #'No' answer
						
						#User previously answered that their past favorite or their past dislike has now flipped
						#Ask further question for clarification

						self.asked_question['question type'] = f"changed mind contradiction {contradiction_type}"

						if contradiction_type == 'favorite_dislike':
							changed_mind_question = f"so {self.asked_question['info']} is no longer your {self.get_random_word('favorite')} {self.asked_question['info type']}, and you {self.get_random_word('dislike')} the {self.asked_question['info type']} {self.asked_question['info']} now?"
						
						elif contradiction_type == 'dislike_favorite':
							changed_mind_question = f"so you no longer {self.get_random_word('dislike')} the {self.asked_question['info type']} {self.asked_question['info']}, and {self.asked_question['info']} is now your {self.get_random_word('favorite')} {self.asked_question['info type']}?"


						self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked if user changed {old_entry}, {new_entry} now?")
						self.CHELSEA_previous_response = self.botReply(changed_mind_question)
						
						return True	
					
					else: #Neither 'yes' or 'no' response

						#Neither yes/no, forget question and move on
						
						self.asked_question = {
							'question type': 'None',
							'info': '',
							'info type': 'None',
							'why': '',
							'date': '',
							'index': 0
						}

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Didn't get answer from user about past {old_entry}, forgetting the question.")

						if random.randint(1, 4) == 1:

							self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
						
							return True
						
						else:

							return False
		
			elif self.asked_question['question type'] in {'changed mind contradiction favorite_dislike', 'changed mind contradiction dislike_favorite'}:

				#User previously stated that they changed their mind about a past dislike or favorite

				contradiction_type = self.asked_question['question type'].split(' ')[3]
				old_entry, new_entry = contradiction_type.split('_')

				topic = self.asked_question['info type']
						
				match = re.search(re.compile(f"(?<!in)({self.get_joined_list('yes')})"), self.user_message)
				if match: #'yes' answer
					
					#Confirmed user did change mind about past foavorite or dislike, flip entry ('favorite' -> 'dislike', 'dislike' -> 'favorite')

					index = self.asked_question['index']

					#Add to angry count if changed mind within 1 day
					self.contradiction_anger(self.user_self[old_entry][topic][index]['date'])
					
					del self.user_self[old_entry][topic][index]

					self.user_self[new_entry][topic].append({
						'info': self.asked_question['info'],
						'why': '',
						'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
					})
					
					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': '',
						'index': 0
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Confirmed user's change in {old_entry}, is {new_entry} now.")
					self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
					
					return True
				
				else:

					#Didn't get expected 'yes' answer, forget line of questioning and move on
						
					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': '',
						'index': 0
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Didn't get 'yes' answer from user about changing {old_entry}, forgetting the question.")

					if random.randint(1, 4) == 1:

						self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
					
						return True
					
					else:

						return False


	def user_give_details_favorite(self):

		if self.asked_question['question type'] == 'None':

			#Only enter if no previous question asked
			
			#'my favorite _ is _
			patterns = [
				re.compile(f"^my ((top|most|number one) )?({self.get_joined_list('favorite')}) (?P<topic>{self.get_joined_list('topics')}) is (?P<info>[a-z0-9 \\-']+)"),
				re.compile(f"^(?P<info>[a-z0-9 \\-']+) is my ((top|most|number one) )?({self.get_joined_list('favorite')}) (?P<topic>{self.get_joined_list('topics')})"),
				re.compile(f"^i like ([a-z0-9 \\-']+ )?(?P<topic>{self.get_joined_list('topics')})(s|es)?, but (?P<info>[a-z0-9 \\-']+) is my ((top|most|number one) )?({self.get_joined_list('favorite')})"),
				re.compile(f"^of all the (?P<topic>{self.get_joined_list('topics')})(s|es)?( [a-z0-9 \\-']+)?, my ((top|most|number one) )?({self.get_joined_list('favorite')}) is (?P<info>[a-z0-9 \\-']+)")
			] #Add more of these later
		
			for pattern in patterns:
				match = re.search(pattern, self.user_message)
				if match:

					#User gave details about what their favorite _ is

					self.user_gave_details = True

					topic = match.group('topic')
					info = match.group('info')

					explanation = None
					because_match = re.search(re.compile(f"(?P<because_whole> ({self.get_joined_list('because')}) (?P<explanation>[a-z0-9 \\-',]+))"), info)
					
					if because_match:
					
						info = info.replace(because_match.group('because_whole'), '')
						explanation = because_match.group('explanation')

					#Check for contradiction in dislike
					index = 0
					for entry in self.user_self['dislike'][topic]:

						if info == entry['info']:

							#Contradiction detected 

							self.asked_question = {
								'question type': f"asked past contradiction dislike_favorite",
								'info': entry['info'],
								'info type': topic,
								'why': '',
								'date': '',
								'index': index
							}

							self.Xchatlog.append(f"{self.bot_name} (Thinking): Found contradiction to what user said about dislike, asking if they still dislike it.")
							self.CHELSEA_previous_response = self.botReply(f"{self.date_difference.get_time_range(entry['date'])} you said you {self.get_random_word('dislike')} the {topic} {info}, do you {self.get_random_word('still')} {self.get_random_word('dislike')} the {topic} {info}?")

							return True
						
						index += 1

					#Check if already exists in user details:
					index = 0
					asked_why = False
					for info_group in self.user_self['favorite'][topic]:
						
						if info_group['info'] == info:
						
							#Already found in memory
							info_group['date'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

							dice_roll = random.randint(1, 5)
							if info_group['why'] == '' and (dice_roll == 1 or dice_roll == 5):
						
								asked_why = True
								break
							
							elif dice_roll == 2:

								#Unless user has favorite that makes CHELSEA happy,
								#give an appropriate counter response
								emotion_reply = self.get_likeness_emotion('like', info)
								if emotion_reply:
									self.CHELSEA_previous_response = self.botReply(emotion_reply)
									return True
						
								#State that already know that favorite
								self.Xchatlog.append(f"{self.bot_name} (Thinking): Got information about user's favorite that i already know.")
								self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('yes')}, i already know your {self.get_random_word('favorite')} {topic} is {info}")
								self.user_gave_details = True
						
								return True
							
							else:
						
								return False
							
						index += 1
							
					else:
						#New favorite found

						#Detect if why possibly answered already in message
						why = explanation if explanation else ''

						why = re.sub(r'\b(i)\b(?!\')', 'you', why)
						why = re.sub(r'\b(i\'m)\b', 'you\'re', why)						
						why = re.sub(r'\b(me)\b(?!\')', 'you', why)
						why = re.sub(r'\b(my)\b(?!\')', 'your', why)
						why = re.sub(r'\b(mine)\b(?!\')', 'yours', why)

						self.user_self['favorite'][topic].append({
							'info': info,
							'why': why,
							'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
						})

						index = len(self.user_self['favorite'][topic]) - 1

						dice_roll = random.randint(1, 5)
						if why == '' and (dice_roll == 1 or dice_roll == 5):
					
							asked_why = True
						
						elif dice_roll == 2:

							self.asked_question = {
								'question type': 'None',
								'info': '',
								'info type': 'None',
								'why': '',
								'date': '',
								'index': 0
							}

							#Unless user has favorite that makes CHELSEA happy,
							#give an appropriate counter response
							emotion_reply = self.get_likeness_emotion('like', info)
							if emotion_reply:
								self.CHELSEA_previous_response = self.botReply(emotion_reply)
								return True
					
							#New information, just give confirmation
							self.Xchatlog.append(f"{self.bot_name} (Thinking): Got new information about user's favorite, just giving confirmation.")
							self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
							self.user_gave_details = True
					
							return True
						
						else:

							self.asked_question = {
								'question type': 'None',
								'info': '',
								'info type': 'None',
								'why': '',
								'date': '',
								'index': 0
							}

							self.Xchatlog.append(f"{self.bot_name} (Thinking): Got new information about user's favorite, moving on.")
					
							return False
							
					if asked_why:
						#No why found, ask for it

						self.asked_question = {
							'question type': 'why favorite',
							'info': info,
							'info type': topic,
							'why': '',
							'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
							'index': index
						}

						responses = [
							f"why is your {self.get_random_word('favorite')} {topic} {info}?",
							f"why is {info} your {self.get_random_word('favorite')} {topic}?",
							f"{self.get_random_word('confirmation')} why is your {self.get_random_word('favorite')} {topic} {info}?",
							f"{self.get_random_word('confirmation')} why is {info} your {self.get_random_word('favorite')} {topic}?",
						]

						self.Xchatlog.append(f"{self.bot_name} (Thinking): The 'why' about user's favorite not found, asking 'why' it is their favorite.")
						self.CHELSEA_previous_response = self.botReply(random.choice(responses))
						self.user_gave_details = True

						return True

	def user_give_details_like(self):

		#Find 'i like/dislike _' message
		patterns = [
			re.compile(f"^i ((?!do not|don't)[a-z0-9 \\-',]+ )?(((?P<dislike>{self.get_joined_list('dislike')})|(?P<like>{self.get_joined_list('like')}))) ((the )?(?P<topic>{self.get_joined_list('topics')}) )?(?P<info>[a-z0-9 \\-',]+)"),
			re.compile(f"^(?P<info>[a-z0-9 \\-',]+) (is|are) (([a-z0-9 \\-'])|(((the|a|an) )?(?P<topic>{self.get_joined_list('topics')}) ))? i((?!do not|don't) [a-z0-9 \\-']+)? (((?P<dislike>{self.get_joined_list('dislike')})|(?P<like>{self.get_joined_list('like')})))")
		]

		for pattern in patterns:
	
			match = re.search(pattern, self.user_message)

			if match:

				#Found user 'i like/dislike _'

				like = match.group('like')
				dislike = match.group('dislike')
				info = match.group('info')
				topic = match.group('topic')

				explanation = None
				because_match = re.search(re.compile(f"(?P<because_whole> ({self.get_joined_list('because')}) (?P<explanation>[a-z0-9 \\-',]+))"), info)
	
				if because_match:

					#Contains explanation of why user likes/dislike _
	
					info = info.replace(because_match.group('because_whole'), '')
					explanation = because_match.group('explanation')

				topic = topic if topic else 'general'
				why = explanation if explanation else ''

				likeness = ''
				if like:
					likeness = 'like'
	
				elif dislike:
					likeness = 'dislike'

				#Check if contradiction exists
				flipped_likeness = 'dislike' if like else 'like'

				index = 0
				for entry in self.user_self[flipped_likeness][topic]:

					if info == entry['info']:

						#Contradiction detected 

						self.asked_question = {
							'question type': f"asked past {flipped_likeness}",
							'info': entry['info'],
							'info type': topic,
							'why': '',
							'date': '',
							'index': index
						}

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found contradiction to what user said about {flipped_likeness}, asking if they still {flipped_likeness} it.")
						self.CHELSEA_previous_response = self.botReply(f"{self.date_difference.get_time_range(entry['date'])} you said you {self.get_random_word('like') if flipped_likeness == 'like' else self.get_random_word('dislike')} {info}, do you still {self.get_random_word('like') if flipped_likeness == 'like' else self.get_random_word('dislike')} {info}?")

						return True
					
					index += 1

				if likeness == 'dislike' and topic != 'general':

					#Check for contradicting favorites if given 'i dislike _'
					index = 0
					for entry in self.user_self['favorite'][topic]:

						if info == entry['info']:

							#Contradiction detected 

							self.asked_question = {
								'question type': f"asked past contradiction favorite_dislike",
								'info': entry['info'],
								'info type': topic,
								'why': '',
								'date': '',
								'index': index
							}

							self.Xchatlog.append(f"{self.bot_name} (Thinking): Found contradiction to what user said about favorite, asking if it is still their favorite.")
							self.CHELSEA_previous_response = self.botReply(f"{self.date_difference.get_time_range(entry['date'])} you said {info} was your {self.get_random_word('favorite')} {topic}, is {info} still your {self.get_random_word('favorite')} {topic}?")

							return True
						
						index += 1

				#Check if already exists in user details:
				index = 0
				asked_why = False
				for info_group in self.user_self[likeness][topic]:
		
					if info_group['info'] == info:

						#Already found in memory, update timestamp
						info_group['date'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

						dice_roll = random.randint(1, 5)
						if info_group['why'] == '' and (dice_roll == 1 or dice_roll == 5):
							
							#Decided to ask use why they like/dislike
							asked_why = True
							break
						
						elif dice_roll == 2:

							#Unless user likes what makes CHELSEA happy or dislikes what makes CHELSEA unhappy,
							#give an appropriate counter response
							emotion_reply = self.get_likeness_emotion(likeness, info)
							if emotion_reply:
								self.CHELSEA_previous_response = self.botReply(emotion_reply)
								return True
							
							#State that already know they like or dislike
							self.Xchatlog.append(f"{self.bot_name} (Thinking): Got information about what user {likeness}s that i already know.")
							self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('yes')}, i already know you {self.get_random_word(likeness)} {info}")
							self.user_gave_details = True
							
							return True
						
						else:
							return False
						
					index += 1
						
				else:
					#New like/dislike found

					#Detect if why possibly answered already in message

					why = re.sub(r'\b(i)\b(?!\')', 'you', why)
					why = re.sub(r'\b(i\'m)\b', 'you\'re', why)
					why = re.sub(r'\b(me)\b(?!\')', 'you', why)
					why = re.sub(r'\b(my)\b(?!\')', 'your', why)
					why = re.sub(r'\b(mine)\b(?!\')', 'yours', why)

					self.user_self[likeness][topic].append({
						'info': info,
						'why': why,
						'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
					})

					index = len(self.user_self[likeness][topic]) - 1

					dice_roll = random.randint(1, 5)
					if why == '' and (dice_roll == 1 or dice_roll == 5):
		
						asked_why = True
					
					elif dice_roll == 2:

						self.asked_question = {
							'question type': 'None',
							'info': '',
							'info type': 'None',
							'why': '',
							'date': '',
							'index': 0
						}

						#Unless user likes what makes CHELSEA happy or dislikes what makes CHELSEA unhappy,
						#give an appropriate counter response
						emotion_reply = self.get_likeness_emotion(likeness, info)
						if emotion_reply:
							self.CHELSEA_previous_response = self.botReply(emotion_reply)
							return True


						#New information, just give confirmation
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Got new information about what user {likeness}s, just giving confirmation.")
						self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
						self.user_gave_details = True
						
						return True
					
					elif dice_roll == 3 and topic == 'general' and likeness == 'like' and self.determine_if_like(info) == 'happy':

						#Found agreement with what CHELSEA likes, respond accordingly

						too_parts = [
							'too',
							'as well',
							'also',
							'for sure',
						]

						start_parts = [
							'',
							'',
							'',
							'same, ',
							'same here, ',
							'me too, ',
							'agreed, ',
							'indeed, ',
							'definitely, '
						]

						me_too_responses = [
							f"{random.choice(start_parts)}i {self.get_random_word('like')} {info}, {random.choice(too_parts)}",
							f"{random.choice(start_parts)}{info} is something i {self.get_random_word('like')}, {random.choice(too_parts)}"
							f"{random.choice(start_parts)}i also {self.get_random_word('like')} {info}"
						]

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Got new information about what user {likeness}s, giving agreement due to match in emotions.")
						self.CHELSEA_previous_response = self.botReply(f"{random.choice(me_too_responses)}")
						self.user_gave_details = True

						self.asked_question = {
							'question type': 'None',
							'info': '',
							'info type': 'None',
							'why': '',
							'date': '',
							'index': 0
						}
						
						return True
					
					else:

						self.asked_question = {
							'question type': 'None',
							'info': '',
							'info type': 'None',
							'why': '',
							'date': '',
							'index': 0
						}

						#Choosing not to say anything after getting new information
						
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Got new information about user's {likeness}s, moving on.")

						return False
						
				if asked_why:

					#No why found for 'i like/dislike _', ask for it

					self.asked_question = {
						'question type': f"why {likeness}",
						'info': info,
						'info type': topic,
						'why': '',
						'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
						'index': index
					}

					responses = [
						f"why do you {self.get_random_word(likeness)} {info}?",
						f"why is {info} something you {self.get_random_word(likeness)}?",
						f"{self.get_random_word('confirmation')} why do you {self.get_random_word(likeness)} {info}?",
						f"{self.get_random_word('confirmation')} why is {info} something you {self.get_random_word(likeness)}?",
					]

					self.Xchatlog.append(f"{self.bot_name} (Thinking): The 'why' about user's {likeness}s not found, asking 'why' they {likeness} it.")
					self.CHELSEA_previous_response = self.botReply(random.choice(responses))
					self.user_gave_details = True

					return True
	
	def user_give_details_have(self):
		
		#Find 'i have/don't have _' message
		patterns = [
			re.compile(f"^i ((?!do not|don't)[a-z0-9 \\-',]+ )?(((?P<have_not>{self.get_joined_list('have not')})|(?P<have>{self.get_joined_list('have')}))) (?P<info>[a-z0-9 \\-',]+)"),
			re.compile(f"^(?P<info>[a-z0-9 \\-',]+) (is|are) (([a-z0-9 \\-'])|(the|a|an) )? i((?!do not|don't) [a-z0-9 \\-']+)? (((?P<have_not>{self.get_joined_list('have not')})|(?P<have>{self.get_joined_list('have')})))")
		]

		for pattern in patterns:

			match = re.search(pattern, self.user_message)

			if match:

				#Found match for 'i have/don't have _'

				have = match.group('have')
				have_not = match.group('have_not')
				info = match.group('info')

				explanation = None
				because_match = re.search(re.compile(f"(?P<because_whole> ({self.get_joined_list('because')}) (?P<explanation>[a-z0-9 \\-',]+))"), info)
	
				if because_match:

					#Explanation for why user has/doesn't have found
	
					info = info.replace(because_match.group('because_whole'), '')
					explanation = because_match.group('explanation')

				why = explanation if explanation else ''

				haveness = ''
				if have:
					haveness = 'have'
	
				elif have_not:
					haveness = 'have not'

				#Check if contradiction exists
				flipped_haveness = 'have not' if have else 'have'

				index = 0
				for entry in self.user_self[flipped_haveness]:

					if info == entry['info']:

						#Contradiction detected 

						self.asked_question = {
							'question type': f"asked past {flipped_haveness.replace(' ', '_')}",
							'info': entry['info'],
							'why': '',
							'date': '',
							'index': index
						}

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found contradiction to what user said about '{haveness}', asking if they still '{haveness}' it.")
						self.CHELSEA_previous_response = self.botReply(f"{self.date_difference.get_time_range(entry['date'])} you said you {self.get_random_word('have') if flipped_haveness == 'have' else self.get_random_word('have not')} {info}, do you {self.get_random_word('still')} {self.get_random_word('have') if flipped_haveness == 'have' else self.get_random_word('have not')} {info}?")

						return True	
					
					index += 1

				#Check if already exists in user details:
				index = 0
				asked_why = False
				for info_group in self.user_self[haveness]:
	
					if info_group['info'] == info:

						#Already found in memory, update timestamp
						info_group['date'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

						dice_roll = random.randint(1, 5)
						if info_group['why'] == '' and (dice_roll == 1 or dice_roll == 5):
	
							asked_why = True
							break
						
						elif dice_roll == 2:

							#State that already know they have or have not
							self.Xchatlog.append(f"{self.bot_name} (Thinking): Got information about what user '{haveness}s' that i already know.")
							self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('yes')}, i already know you {self.get_random_word('have') if haveness == 'have' else self.get_random_word('have not')} {info}")
							self.user_gave_details = True
							return True
						
						else:
	
							return False
						
					index += 1
						
				else:

					#New have/have not found

					#Detect if why possibly answered already in message

					why = re.sub(r'\b(i)\b(?!\')', 'you', why)
					why = re.sub(r'\b(i\'m)\b', 'you\'re', why)
					why = re.sub(r'\b(me)\b(?!\')', 'you', why)
					why = re.sub(r'\b(my)\b(?!\')', 'your', why)
					why = re.sub(r'\b(mine)\b(?!\')', 'yours', why)

					self.user_self[haveness].append({
						'info': info,
						'why': why,
						'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
					})

					index = len(self.user_self[haveness]) - 1

					dice_roll = random.randint(1, 5)
					if why == '' and (dice_roll == 1 or dice_roll == 5):
	
						asked_why = True
					
					elif dice_roll == 2:

						self.asked_question = {
							'question type': 'None',
							'info': '',
							'info type': 'None',
							'why': '',
							'date': '',
							'index': 0
						}

						#New information, just give confirmation
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Got new information about what user '{haveness}s', just giving confirmation.")
						self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
						self.user_gave_details = True
						
						return True
					
					else:

						self.asked_question = {
							'question type': 'None',
							'info': '',
							'info type': 'None',
							'why': '',
							'date': '',
							'index': 0
						}

						#New information, but choosing to not say anything about it

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Got new information about user's '{haveness}s', moving on.")

						return False
						
				if asked_why:

					#No why found, ask for it

					self.asked_question = {
						'question type': f"why {haveness.replace(' ', '_')}",
						'info': info,
						'info type': '',
						'why': '',
						'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
						'index': index
					}

					responses = [
						f"why do you {self.get_random_word('have') if haveness == 'have' else self.get_random_word('have not')} {info}?",
						f"why is {info} something you {self.get_random_word('have') if haveness == 'have' else self.get_random_word('have not')}?",
						f"{self.get_random_word('confirmation')} why do you {self.get_random_word('have') if haveness == 'have' else self.get_random_word('have not')} {info}?",
						f"{self.get_random_word('confirmation')} why is {info} something you {self.get_random_word('have') if haveness == 'have' else self.get_random_word('have not')}?",
					]

					self.Xchatlog.append(f"{self.bot_name} (Thinking): The 'why' about user's '{haveness}s' not found, asking 'why' they '{haveness}' it.")
					self.CHELSEA_previous_response = self.botReply(random.choice(responses))
					self.user_gave_details = True

					return True
				
	def user_give_details_am(self):
			
		#Find 'i have/don't have _' message
		patterns = [
			re.compile(f"^i ((?P<am_not>am not)|(?P<am>am)) (?P<info>[a-z0-9 \\-',]+)"),
			re.compile(f"^(?P<info>[a-z0-9 \\-',]+?) is ([a-z0-9 \\-']+ )?i ((?P<am_not>am not)|(?P<am>am))")
		]

		for pattern in patterns:

			match = re.search(pattern, self.user_message)

			if match:

				#Found match for 'i am/am not _'

				am = match.group('am')
				am_not = match.group('am_not')
				info = match.group('info')

				explanation = None
				because_match = re.search(re.compile(f"(?P<because_whole> ({self.get_joined_list('because')}) (?P<explanation>[a-z0-9 \\-',]+))"), info)

				if because_match:

					#Explanation for why user is/isn't have found

					info = info.replace(because_match.group('because_whole'), '')
					explanation = because_match.group('explanation')

				why = explanation if explanation else ''

				amness = ''
				if am:
					amness = 'uam'

				elif am_not:
					amness = 'uamnot'

				#Check if contradiction exists
				flipped_amness = 'uamnot' if am else 'uam'

				index = 0
				for entry in self.user_self[flipped_amness]:

					if info == entry['info']:

						#Contradiction detected 

						self.asked_question = {
							'question type': f"asked past {flipped_amness}",
							'info': entry['info'],
							'why': '',
							'date': '',
							'index': index
						}

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found contradiction to what user said about '{amness}', asking if they still '{amness}' it.")
						self.CHELSEA_previous_response = self.botReply(f"{self.date_difference.get_time_range(entry['date'])} you said you {'are' if flipped_amness == 'uam' else 'are not'} {info}, are you {self.get_random_word('still')}{'' if flipped_amness == 'uam' else ' not'} {info}?")

						return True	
					
					index += 1

				#Check if already exists in user details:
				index = 0
				asked_why = False
				for info_group in self.user_self[amness]:

					if info_group['info'] == info:

						#Already found in memory, update timestamp
						info_group['date'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

						dice_roll = random.randint(1, 5)
						if info_group['why'] == '' and (dice_roll == 1 or dice_roll == 5):

							asked_why = True
							break
						
						elif dice_roll == 2:

							#State that already know they is or is not
							self.Xchatlog.append(f"{self.bot_name} (Thinking): Got information about what user '{amness}s' that i already know.")
							self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('yes')}, i already know you {'are' if amness == 'uam' else 'are not'} {info}")
							self.user_gave_details = True
							return True
						
						else:

							return False
						
					index += 1
						
				else:

					#New uam/uamnot found

					#Detect if why possibly answered already in message

					why = re.sub(r'\b(i)\b(?!\')', 'you', why)
					why = re.sub(r'\b(i\'m)\b', 'you\'re', why)
					why = re.sub(r'\b(me)\b(?!\')', 'you', why)
					why = re.sub(r'\b(my)\b(?!\')', 'your', why)
					why = re.sub(r'\b(mine)\b(?!\')', 'yours', why)

					self.user_self[amness].append({
						'info': info,
						'why': why,
						'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
					})

					index = len(self.user_self[amness]) - 1

					dice_roll = random.randint(1, 5)
					if why == '' and (dice_roll == 1 or dice_roll == 5):

						asked_why = True
					
					elif dice_roll == 2:

						self.asked_question = {
							'question type': 'None',
							'info': '',
							'info type': 'None',
							'why': '',
							'date': '',
							'index': 0
						}

						#New information, just give confirmation
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Got new information about what user '{amness}s', just giving confirmation.")
						self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
						self.user_gave_details = True
						
						return True
					
					else:

						self.asked_question = {
							'question type': 'None',
							'info': '',
							'info type': 'None',
							'why': '',
							'date': '',
							'index': 0
						}

						#New information, but choosing to not say anything about it

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Got new information about user's '{amness}s', moving on.")

						return False
						
				if asked_why:

					#No why found, ask for it

					self.asked_question = {
						'question type': f"why {amness}",
						'info': info,
						'info type': '',
						'why': '',
						'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
						'index': index
					}

					responses = [
						f"why are you{'' if amness == 'uam' else ' not'} {info}?",
						f"why is {info} something you are{'' if amness == 'uam' else ' not'}?",
						f"{self.get_random_word('confirmation')} why do are you{'' if amness == 'uam' else ' not'} {info}?",
						f"{self.get_random_word('confirmation')} why is {info} something you are{'' if amness == 'uam' else ' not'}?",
					]

					self.Xchatlog.append(f"{self.bot_name} (Thinking): The 'why' about user's '{amness}s' not found, asking 'why' they are '{amness}' it.")
					self.CHELSEA_previous_response = self.botReply(random.choice(responses))
					self.user_gave_details = True

					return True				

	def confirm_user_why_favorite(self):

		if self.asked_question['question type'] != 'None':

			#Don't enter unless question previously asked
	
			if self.asked_question['question type'] == 'why favorite':

				#Previously asked user why _ is their favorite _
	
				match = re.search(re.compile(f"({self.get_joined_list('because')})? ?(?P<explanation>[a-z0-9 \\-',]+)"), self.user_message)
	
				if match:

					#Potential explanation found, process and ask for clarification
	
					explanation = match.group('explanation')

					explanation = re.sub(r'\b(i)\b(?!\')', 'you', explanation)
					explanation = re.sub(r'\b(i\'m)\b', 'you\'re', explanation)
					explanation = re.sub(r'\b(me)\b(?!\')', 'you', explanation)
					explanation = re.sub(r'\b(my)\b(?!\')', 'your', explanation)
					explanation = re.sub(r'\b(mine)\b(?!\')', 'yours', explanation)

					self.asked_question['question type'] = 'why favorite clarify'
					self.asked_question['why'] = explanation

					beginnings = [
						'',
						'oh, ',
						'okay, ',
						'so then, ',
						'so..., ',
						'am i right, '
					]

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Possibly answered why this is user's favorite, asking yes/no question for clarity.")
					self.CHELSEA_previous_response = self.botReply(f"{random.choice(beginnings)}your {self.get_random_word('favorite')} {self.asked_question['info type']} is {self.asked_question['info']} {self.get_random_word('because')} {explanation}?")
			
					return True
				
			elif self.asked_question['question type'] == 'why favorite clarify':

				#Previously asked user to clarify why _ is their favorite _

				self.user_gave_details = False
			
				match = re.search(re.compile(f"(?<!in)({self.get_joined_list('yes')})"), self.user_message)
	
				if match:

					#'yes' answer given, store why favorite

					self.user_self['favorite'][self.asked_question['info type']][self.asked_question['index']] = {
						'info': self.asked_question['info'],
						'why': self.asked_question['why'],
						'date': self.asked_question['date']
					}

					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': '',
						'index': 0
					}

					if random.randint(1, 4) == 1:

						#Got favorite info, give confirmation

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Answered why this is user's favorite, responding with confirmation.")
						self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
			
						return True
					
					else:

						#Got favorite info, choosing to say nothing about it

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Answered why this is user's favorite, not giving response.")

						return False
					
				else:

					#'yes' answer not given for clarification, forgetting line of questioning and moving on

					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': ''
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): No clarification for previous question regarding why it is user's favorite, forgetting the question and moving on.")

					return False
		
		return False
		
	def confirm_user_why_like(self):
	
		if self.asked_question['question type'] != 'None':

			#Don't enter unless previously asked question
	
			if self.asked_question['question type'] == 'why like' or self.asked_question['question type'] == 'why dislike':
	
				#Previously asked 'why like/dislike' question
				
				likeness = self.asked_question['question type'].split(" ")[1]	

				match = re.search(re.compile(f"({self.get_joined_list('because')})? ?(?P<explanation>[a-z0-9 \\-',]+)"), self.user_message)
	
				if match:

					#Potential explanation found, process and ask for clarification
	
					explanation = match.group('explanation')

					explanation = re.sub(r'\b(i)\b(?!\')', 'you', explanation)
					explanation = re.sub(r'\b(i\'m)\b', 'you\'re', explanation)
					explanation = re.sub(r'\b(me)\b(?!\')', 'you', explanation)
					explanation = re.sub(r'\b(my)\b(?!\')', 'your', explanation)
					explanation = re.sub(r'\b(mine)\b(?!\')', 'yours', explanation)

					self.asked_question['question type'] = f"why {likeness} clarify"
					self.asked_question['why'] = explanation

					beginnings = [
						'',
						'oh, ',
						'okay, ',
						'so then, ',
						'so..., ',
						'am i right, '
					]

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Possibly answered why user {likeness}s this, asking yes/no question for clarity.")
					self.CHELSEA_previous_response = self.botReply(f"{random.choice(beginnings)}you {self.get_random_word(likeness)} {self.asked_question['info']} {self.get_random_word('because')} {explanation}?")
			
					return True
			
			elif self.asked_question['question type'] == 'why like clarify' or self.asked_question['question type'] == 'why dislike clarify':

				#Previously asked to clarify why like/dislike _

				likeness = self.asked_question['question type'].split(" ")[1]

				self.user_gave_details = False
			
				match = re.search(re.compile(f"(?<!in)({self.get_joined_list('yes')})"), self.user_message)
	
				if match:

					#'yes' answer given, store new why like/dislike

					self.user_self[likeness][self.asked_question['info type']][self.asked_question['index']] = {
						'info': self.asked_question['info'],
						'why': self.asked_question['why'],
						'date': self.asked_question['date']
					}

					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': '',
						'index': 0
					}

					if random.randint(1, 4) == 1:

						#Got new information, respond with confirmation

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Answered why user {likeness}s this, responding with confirmation.")
						self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
			
						return True
					
					else:

						#Got new information, choosing not to give response for it

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Answered why user {likeness}s this, not giving response.")
	
						return False
					
				else:

					#'yes' answer not given, forgetting this line of questioning and moving on

					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': ''
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): No clarification for previous question regarding why user {likeness}s this, forgetting the question and moving on.")

					return False
		
		return False

	def confirm_user_why_have(self):

		if self.asked_question['question type'] != 'None':

			#Don't enter unless question previously asked	

			if self.asked_question['question type'] == 'why have' or self.asked_question['question type'] == 'why have_not':
				
				#Previously asked 'why have/have not' question
				
				haveness = self.asked_question['question type'].split(" ")[1].replace('_', ' ')	

				match = re.search(re.compile(f"({self.get_joined_list('because')})? ?(?P<explanation>[a-z0-9 \\-',]+)"), self.user_message)
	
				if match:

					#Potential explanation found, process and ask for clarification
	
					explanation = match.group('explanation')

					explanation = re.sub(r'\b(i)\b(?!\')', 'you', explanation)
					explanation = re.sub(r'\b(i\'m)\b', 'you\'re', explanation)
					explanation = re.sub(r'\b(me)\b(?!\')', 'you', explanation)
					explanation = re.sub(r'\b(my)\b(?!\')', 'your', explanation)
					explanation = re.sub(r'\b(mine)\b(?!\')', 'yours', explanation)

					self.asked_question['question type'] = f"why {haveness.replace(' ', '_')} clarify"
					self.asked_question['why'] = explanation

					beginnings = [
						'',
						'oh, ',
						'okay, ',
						'so then, ',
						'so..., ',
						'am i right, '
					]

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Possibly answered why user '{haveness}s' this, asking yes/no question for clarity.")
					self.CHELSEA_previous_response = self.botReply(f"{random.choice(beginnings)}you {self.get_random_word('have') if haveness == 'have' else self.get_random_word('have not')} {self.asked_question['info']} {self.get_random_word('because')} {explanation}?")
			
					return True
			
			elif self.asked_question['question type'] == 'why have clarify' or self.asked_question['question type'] == 'why have_not clarify':

				#Previously asked why user has _ or doesn't have _

				haveness = self.asked_question['question type'].split(" ")[1].replace('_', ' ')

				self.user_gave_details = False
			
				match = re.search(re.compile(f"(?<!in)({self.get_joined_list('yes')})"), self.user_message)
	
				if match:

					#'yes' answer given, store new why about what user has or doesn't have

					self.user_self[haveness][self.asked_question['index']] = {
						'info': self.asked_question['info'],
						'why': self.asked_question['why'],
						'date': self.asked_question['date']
					}

					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': '',
						'index': 0
					}

					if random.randint(1, 4) == 1:

						#Got new information, give confirmation

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Answered why user '{haveness}s' this, responding with confirmation.")
						self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
			
						return True
					
					else:

						#Got new information, choosing not to respond to it

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Answered why user '{haveness}s' this, not giving response.")
	
						return False
					
				else:

					#Expected 'yes' answer not given, forgetting line of questioning and moving on

					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': ''
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): No clarification for previous question regarding why user '{haveness}s' this, forgetting the question and moving on.")

					return False				

		return False
	
	def confirm_user_why_am(self):

		if self.asked_question['question type'] != 'None':

			#Don't enter unless question previously asked	

			if self.asked_question['question type'] == 'why uam' or self.asked_question['question type'] == 'why uamnot':
				
				#Previously asked 'why is/is not' question
				
				amness = self.asked_question['question type'].split(" ")[1]

				match = re.search(re.compile(f"({self.get_joined_list('because')})? ?(?P<explanation>[a-z0-9 \\-',]+)"), self.user_message)
	
				if match:

					#Potential explanation found, process and ask for clarification
	
					explanation = match.group('explanation')

					explanation = re.sub(r'\b(i)\b(?!\')', 'you', explanation)
					explanation = re.sub(r'\b(i\'m)\b', 'you\'re', explanation)
					explanation = re.sub(r'\b(me)\b(?!\')', 'you', explanation)
					explanation = re.sub(r'\b(my)\b(?!\')', 'your', explanation)
					explanation = re.sub(r'\b(mine)\b(?!\')', 'yours', explanation)

					self.asked_question['question type'] = f"why {amness} clarify"
					self.asked_question['why'] = explanation

					beginnings = [
						'',
						'oh, ',
						'okay, ',
						'so then, ',
						'so..., ',
						'am i right, '
					]

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Possibly answered why user '{amness}s' this, asking yes/no question for clarity.")
					self.CHELSEA_previous_response = self.botReply(f"{random.choice(beginnings)}you are{'' if amness == 'uam' else ' not'} {self.asked_question['info']} {self.get_random_word('because')} {explanation}?")
			
					return True
			
			elif self.asked_question['question type'] == 'why uam clarify' or self.asked_question['question type'] == 'why uamnot clarify':

				#Previously asked why user is _ or isn't _

				amness = self.asked_question['question type'].split(" ")[1]

				self.user_gave_details = False
			
				match = re.search(re.compile(f"(?<!in)({self.get_joined_list('yes')})"), self.user_message)
	
				if match:

					#'yes' answer given, store new why about what user is or isn't

					self.user_self[amness][self.asked_question['index']] = {
						'info': self.asked_question['info'],
						'why': self.asked_question['why'],
						'date': self.asked_question['date']
					}

					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': '',
						'index': 0
					}

					if random.randint(1, 4) == 1:

						#Got new information, give confirmation

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Answered why user '{amness}s' this, responding with confirmation.")
						self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")
			
						return True
					
					else:

						#Got new information, choosing not to respond to it

						self.Xchatlog.append(f"{self.bot_name} (Thinking): Answered why user '{amness}s' this, not giving response.")
	
						return False
					
				else:

					#Expected 'yes' answer not given, forgetting line of questioning and moving on

					self.asked_question = {
						'question type': 'None',
						'info': '',
						'info type': 'None',
						'why': '',
						'date': ''
					}

					self.Xchatlog.append(f"{self.bot_name} (Thinking): No clarification for previous question regarding why user '{amness}s' this, forgetting the question and moving on.")

					return False				

		return False
	
	def user_birthday(self):

		#To deal with the user's birthday information

		completed_birthdate = False

		if self.user_self['birthday']['status'] != 'complete':

			#If no or incomplete info on birthday

			user_given_birthday = False
			user_match = re.search(re.compile(f"my (birthday|date of birth|b(-| )?day) is (((?P<month_string>{self.get_joined_list('months')})\\.?,? ((?P<day>(\\d)?\\d) ?),? ?(?P<year>(\\d\\d)?\\d\\d)?)|(?P<full_date>(\\d)?\\d(/|-)(\\d)?\\d(/|-)((\\d\\d)?\\d\\d)?))"), self.user_message)
	
			if user_match:

				#To let user_message fall through to processing, since matching birthday pattern is found in message
				user_given_birthday = True

			else:

				#Check if given months or weeks from/to birthday, ask for specific date instead
				month_week_match = re.search(r"my (birthday|date of birth) (?P<forward_or_backward>is|was) ([0-9]+ |[a-z]+ )?((going to be )?in )?([0-9]+ |[a-z]+)?(months|weeks)(( from now| ago)?)?", self.user_message)

				if month_week_match:

					self.user_self['birthday']['status'] = 'asked birthday'

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Was given months or weeks for user's birthday that i'm not going to process, asking for specific birthday.")
					self.CHELSEA_previous_response = self.botReply(f"when {random.choice(['exactly', 'precisely'])} is your birthday, the actual date?")
		
					return True

				#Look for N days away, days prior
				#Also caught here if user is answering birthday question in this kind of format, which should be fine?
				user_match2 = re.search(r"my (birthday|date of birth|b(-| )?day) (?P<forward_or_backward>is|was) ((going to be )?in )?((?P<numerical_days>[0-9]+)|(?P<string_days>[a-z]+))( days( from now| ago)?)?", self.user_message)

				if user_match2:

					forward_or_backward = user_match2.group('forward_or_backward')

					#Get user birthday number of days before or after today if given
					days = 0

					if user_match2.group('numerical_days'):

						days = int(user_match2.group('numerical_days'))

					elif user_match2.group('string_days'):

						if user_match2.group('string_days') in {'yesterday', 'tomorrow'}:
							
							days = 1

						elif user_match2.group('string_days') == 'today':

							days = 0

						else:

							days = self.date_difference.string_to_numerical_days(user_match2.group('string_days'))

					#Calculate the birthday given number of days before or after today
					birthday = ''
					if forward_or_backward == 'is':

						birthday = self.date_difference.get_date_given_time_frame(days)

					elif forward_or_backward == 'was':

						birthday = self.date_difference.get_date_given_time_frame(- days)
					
					#No year given
					birthday = re.sub(r'(\d\d\d\d, \d\d:\d\d:\d\d)', '0000, 00:00:00', birthday)

					self.user_self['birthday']['date'] = birthday
					self.user_self['birthday']['status'] = 'asked birth year'

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Missing year of user's birthday, asking for it.")
					self.CHELSEA_previous_response = self.botReply(f"{self.username}, what year were you born?")

					return True
						

			if self.user_self['birthday']['last asked'] != '' and not user_given_birthday:

				#If missing birthday info and hasn't asked for it in at least 30 days, reset 'last asked' so it triggers asking again

				if self.date_difference.get_days_past(self.user_self['birthday']['last asked']) >= 30:

					self.user_self['birthday']['last asked'] = ''

			if self.user_self['birthday']['last asked'] == '' or user_given_birthday:

				#Missing birthday info, ask questions regarding it

				if self.user_self['birthday']['status'] == 'none' and not user_given_birthday:

					#Ask for birthday

					self.user_self['birthday']['status'] = 'asked birthday'

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Don't have any information on user's birthday, asking for it.")
					self.CHELSEA_previous_response = self.botReply(f"{self.username}, when is your birthday?")
		
					return True

				elif self.user_self['birthday']['status'] == 'missing year' and not user_given_birthday:

					#Ask for year

					self.user_self['birthday']['status'] = 'asked birth year'

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Missing year of user's birthday, asking for it.")
					self.CHELSEA_previous_response = self.botReply(f"{self.username}, what year were you born?")
		
					return True
				
				elif self.user_self['birthday']['status'] == 'asked birthday' or user_given_birthday:
	
					#Try to get either full birthday or at least the month and day
					match = re.search(re.compile(f"(my (birthday|date of birth|b(-| )?day) is )?((((?P<month_string>{self.get_joined_list('months')})\\.?,? (?P<day>(\\d)?\\d) ?),? ?(?P<year>(\\d\\d)?\\d\\d)?)|(?P<full_date>(\\d)?\\d(/|-)(\\d)?\\d(/|-)((\\d\\d)?\\d\\d)?))"), self.user_message)

					if match:

						#Potential birthday given

						if match.group('full_date'):

							#Full date for birthday given

							month= ''
							day = ''
							year = ''

							match2 = re.search(r'(?P<month>(\d)?\d)(/|-)(?P<day>(\d)?\d)(/|-)(?P<year>(\d\d)?\d\d)', match.group('full_date'))
	
							if match2:

								#Numerical birthday given

								#Tack on start numbers of year if only 2 given
								if len(match2.group('year')) == 2:

									year = int(match2.group('year'))
									if year < 45:
										year = f"20{'0' if len(str(year)) == 1 else ''}{year}"
	
									else:
										year = f"19{year}"

								else:
									year = match2.group('year') 

								#Tack 0 on beginning of month if only ones digit given
								month = match2.group('month')
								if len(month) == 1:
									month = f"0{month}"

								#Tack 0 on beginning of day if only ones digit given
								day = match2.group('day')
								if len(day) == 1:
									day = f"0{day}"

							else:

								#No year given, ask for it

								self.user_self['birthday']['date'] = f"{month}/{day}/0000, 00:00:00"
								self.user_self['birthday']['status'] = 'asked birth year'

								self.Xchatlog.append(f"{self.bot_name} (Thinking): Missing year of user's birthday, asking for it.")
								self.CHELSEA_previous_response = self.botReply(f"{self.username}, what year were you born?")
		
								return True
							
							#Complete birthday given

							self.user_self['birthday']['date'] = f"{month}/{day}/{year}, 00:00:00"
							self.user_self['birthday']['status'] = 'complete'

							completed_birthdate = True

						elif match.group('month_string'):

							#Month as string given, process accordingly

							#Convert the string month to a number (january -> 01)
							month = self.date_difference.get_month(match.group('month_string'))
							day = match.group('day')
							year = match.group('year')

							if len(day) == 1:
								day = f"0{day}"

							if year:

								#If given year is only 2 digits, tack on first 2 numbers
								if len(year) == 2:

									year = int(year)
									if year < 45:
										year = f"20{'0' if len(str(year)) == 1 else ''}{year}"

									else:
										year = f"19{year}"

								#Got complete birthday

								self.user_self['birthday']['date'] = f"{month}/{day}/{year}, 00:00:00"
								self.user_self['birthday']['status'] = 'complete'

								completed_birthdate = True

							else:

								#No year given, ask for it

								self.user_self['birthday']['date'] = f"{month}/{day}/0000, 00:00:00"
								self.user_self['birthday']['status'] = 'asked birth year'

								self.Xchatlog.append(f"{self.bot_name} (Thinking): Missing year of user's birthday, asking for it.")
								self.CHELSEA_previous_response = self.botReply(f"{self.username}, what year were you born?")
		
								return True		

						else:
		
							#If no match, forget question for now

							self.user_self['birthday']['status'] = 'none'
							self.user_self['birthday']['last asked'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

							return False
					
					else:

						#If no match, forget question for now

						self.user_self['birthday']['status'] = 'none'
						self.user_self['birthday']['last asked'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

						return False

				elif self.user_self['birthday']['status'] == 'asked birth year':
					
					#Try to get either 2 digit or 4 digit match for year

					year = ''
					match = re.search(r'(?P<year>(\d\d)?\d\d)', self.user_message)

					if match:

						#Got either 2 or 4 digit year

						#2 digits only, tack on first 2 digits of year
						if len(match.group('year')) == 2:

							year = int(match.group('year'))
							if year < 45:
								year = f"20{'0' if len(str(year)) == 1 else ''}{year}"
							else:
								year = f"19{year}"
						
						else:
							year = match.group('year')

						#Got completed birthday

						self.user_self['birthday']['date'] = self.user_self['birthday']['date'].replace('0000', year)
						self.user_self['birthday']['status'] = 'complete'

						completed_birthdate = True	

					else:

						#If no match, forget question for now
						self.user_self['birthday']['status'] = 'missing year'
						self.user_self['birthday']['last asked'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

		if completed_birthdate:

			#Previously got the complete information for user birthday
			#Check if user birthday today, give 'happy birthday message' if so

			if self.date_difference.match_date(self.user_self['birthday']['date']):

				#Found user's birthday is today, give them message

				self.Xchatlog.append(f"{self.bot_name} (Thinking): User's birthday is today, wishing them a happy one.")
				self.CHELSEA_previous_response = self.botReply(f"happy birthday, {self.username}!")
		
				return True	
			
			else:

				#Not user's birthday, just give confirmation

				self.Xchatlog.append(f"{self.bot_name} (Thinking): Got the user's full birthday, giving confirmation.")
				self.CHELSEA_previous_response = self.botReply(f"{self.get_random_word('confirmation')}")

				return True

		return False

	def funny_response(self):

		if re.search(re.compile(f"^({self.get_joined_list('lol')})$"), self.user_message):

			#User previously gave 'lol' message

			index = 0
			for funny in self.user_self['finds funny']:

				#Previous message already found in 'finds funny', increase count on it and update timestamp

				if self.CHELSEA_previous_response == funny['response']:
					
					self.user_self['finds funny'][index]['count'] += 1
					self.user_self['finds funny'][index]['date'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
					
					break

				index += 1

			else:

				#Previous message not found in 'finds funny', store it with current timestamp

				self.user_self['finds funny'].append({
					'response': self.CHELSEA_previous_response,
					'count': 1,
					'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
				})

		if random.randint(1, 15) == 1:

			if len(self.current_topics) > 0:

				for topic in self.current_topics:
					
					if topic in {'lol', 'lulz', 'lmao', 'rofl', 'lmfao', 'roflmao', 'haha', 'hehe'}:

						#Current topics suggest user is in laughing mood,

						#Build list of 'finds funny' responses at least 7 days old
						funny_responses = []
						index = 0
						for funny in self.user_self['finds funny']:

							if self.date_difference.get_days_past(funny['date']) >= 7:

								funny_responses.append({
									'entry': funny,
									'index': index
								})

							index += 1

						if len(funny_responses) == 0:

							return False
						
						#Give random response from responses user 'finds funny' in the past, and update timestamp on it to prevent repeating again for at least 7 days

						chosen_funny_response = random.choice(funny_responses)

						self.user_self['finds funny'][chosen_funny_response['index']]['date'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

						self.Xchatlog.append(f"{self.bot_name} (Thinking): User seems to be in laughing mood, saying something that may have made them laugh in the past.")
						self.CHELSEA_previous_response = self.botReply(chosen_funny_response['entry']['response'])
			
						return True

		return False
	
	def recall_past_topic(self):

		match = re.search(r'(((do you (remember|recall) ?)?what (were|was|we) (we|i|were) (talking|conversing|gabbing) about ((?P<num_days>[0-9]+)|(?P<string_days>[a-z]+)) day(s)? (ago|before|prior( to today)?)))|((((?P<num_days2>[0-9]+)|(?P<string_days2>[a-z]+)) days (ago|before|prior( to today)?),? )what (were|was|we) (we|i|were) (talking|conversing|gabbing) about)\??', self.user_message)
		num_days_ago = None
		
		if match:

			#Match for messages like 'do you remember what we were talking about N days ago?'

			if match.group('num_days') or match.group('num_days2'):

				#Got numerical days
				num_days_ago = int(match.group('num_days')) if match.group('num_days') else int(match.group('num_days2'))
	
			elif match.group('string_days') or match.group('string_days2'):

				#Got string days (one, two, etc.)
				num_days_ago = self.date_difference.string_to_numerical_days(match.group('string_days')) if match.group('string_days') else self.date_difference.string_to_numerical_days(match.group('string_days2')) 

			if not num_days_ago:

				#Invalid format for question, just say 'idk' message

				self.Xchatlog.append(f"{self.bot_name} (Thinking): Can't process the question about what we were talking about X days ago, just giving 'idk' response.")
				
				responses = [
					f"i {random.choice(['don\'t', 'do not'])} {random.choice(['know', 'recall', 'remember'])}",
					f"i'm not sure",
					f"dunno"
				]
				self.CHELSEA_previous_response = self.botReply(random.choice(responses))
			
				return True 

		if random.randint(1, 20) == 1 or num_days_ago:

			#Build list of past topics at least a day old, or num_days_ago if user previously asked 'do you remember what we were talking about N days ago?'

			topic_lists = []

			for topic_list in self.user_self['popular topics']:

				if not num_days_ago and self.date_difference.get_days_past(topic_list['date']) > 0:

					topic_lists.append(topic_list)

				if num_days_ago and self.date_difference.get_days_past(topic_list['date']) == num_days_ago:

					topic_lists.append(topic_list)

			if len(topic_lists) > 0:

				#Choose random list of topics, then choose random topic from that list
				chosen_list = random.choice(topic_lists)
				chosen_topic = random.choice(chosen_list['topics'])

				if chosen_topic in self.past_topic_blacklist:
					
					#chosen topic found in topic blacklist for this chat, don't use it, just exit the method instead

					return False

				#Add topic to the blacklist to avoid it being brought up again in this chat
				self.past_topic_blacklist.append(chosen_topic)

				#Build reponse given chosen topic and respond with it
				remember = random.choice(['remember', 'recall'])
				talking = random.choice(['talking', 'conversing', 'gabbing'])
				time_range = self.date_difference.get_time_range(chosen_list['date'])

				responses = [
					f"i {remember} {time_range} we were {talking} about {chosen_topic}",
					f"{time_range}, {chosen_topic} was what we were {talking} about",
					f"{remember}? {time_range} {chosen_topic} was on your mind",
					f"do you {remember} {time_range}? we were {talking} about {chosen_topic}",
					f"if i {remember}, {time_range} weren't we {talking} about something to do with {chosen_topic}"
				]

				chosen_response = random.choice(responses)

				self.Xchatlog.append(f"{self.bot_name} (Thinking): Recalled a past topic with the user.")
				self.CHELSEA_previous_response = self.botReply(chosen_response)
			
				return True

			else:

				#No topics found in list

				if num_days_ago:

					#Must not have talked during that time frame, respond accordingly

					self.Xchatlog.append(f"{self.bot_name} (Thinking): Past user asked about conversation X days ago, we didn't talk X days ago.")
					self.CHELSEA_previous_response = self.botReply(f"i {random.choice(['don\'t', 'do not'])} think we {random.choice(['talked', 'conversed', 'gabbed'])} {num_days_ago} days ago")
				
					return True

				else:	

					return False

	def check_exact_message_match(self):
		
		#Check for exact match of user reply to message in memory under current mood
		
		try:
		
			self.message_dict2[self.current_mood["mood"]][self.user_message]

			#Match found, respond accordingly with random choice from list of associated responses
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Exact message match found.")
			self.CHELSEA_previous_response = self.botReply(random.choice(self.message_dict2[self.current_mood["mood"]][self.user_message]))
			return True
		
		except(KeyError):
			
			#Message match not found
			return False
		
	def check_partial_message_match(self):
		
		#Check for partial match of user reply to message in memory under current mood, user reply contained in message
		
		response_made = False
		for message in self.temp_message_keys:
		
			if message.find(self.user_message) != -1:
				
				#Match found, respond accordingly with random choice from list of associated responses
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Partial message match found.")
				self.CHELSEA_previous_response = self.botReply(random.choice(self.message_dict2[self.current_mood["mood"]][message]))
				response_made = True
				break
		
		if response_made:
			return True
		
		#Partial match not found
		return False
	
	def learn_new_response(self):

		if self.user_gave_details:

			self.user_gave_details = False
			self.give_random_or_question_response()
			
			return True
		
		#No match, either add to message/response pairs or learn new one based on reply mood
		
		self.Xchatlog.append(f"{self.bot_name} (Thinking): Message not recognized.")
		
		try:
			#Attempt previous response as key under current mood
			self.message_dict2[self.reply_mood["mood"]][self.CHELSEA_previous_response]
		
		except(KeyError):
			#Previous response under current mood does not exist as key, learn it as a new message, 
			# make tied responses an empty list. 
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new '{self.reply_mood["mood"]}' response.")
			self.message_dict2[self.reply_mood["mood"]][self.CHELSEA_previous_response] = []
		
		duplicate_found = False
		
		for response in self.message_dict2[self.reply_mood["mood"]][self.CHELSEA_previous_response]:
		
			if (response == self.user_message):
		
				#User reply already found tied to message
				duplicate_found = True
				break
		
		if (not(duplicate_found)):

			#User reply not found tied to message, tie it to message by appending it to list
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Added to '{self.reply_mood["mood"]}' responses.")
			self.message_dict2[self.reply_mood["mood"]][self.CHELSEA_previous_response].append(self.user_message)

		#Possibly learn new why is/are question from user_message
		self.learn_why_isare_question()

		return False
	
	def check_fuzzy_message_match(self):

		if random.randint(1, 6) == 1:
		
			#Try to find match of user message in message dictionary with at least 55% similarity
			fuzzy_response = self.fuzzy_match(self.user_message, 0.55)
			
			if fuzzy_response:

				#Match found, use the response paired with the matching message

				self.Xchatlog.append(f"{self.bot_name} (Thinking): Found fuzzy match to user message with {fuzzy_response['score'] * 100}% similarity, giving the paired response.")
				self.CHELSEA_previous_response = self.botReply(fuzzy_response['response'])
				
				return True	
		
		#No fuzzy match found for similarity at least 55% or failed dice roll to trigger this method
		return False
	
	def check_topic_or_depth_match(self):
		
		#Check for match with current topic or depth match
		
		if (self.dictionary_count >= 2500 and self.response_count >= 1200 and random.randint(1, 9) == 1) or (self.dictionary_count >= 600 and self.dictionary_count < 2500 and self.response_count >= 350 and self.response_count < 1200 and random.randint(1, 15) == 1):

			#Use 'dice rolls' to determine if topic or depth match used.
			#Also decided by how much is in CHELSEA's memory.

			if len(self.depth_words) >= 2 and random.randint(1, 6) == 1:
				#1/6, depth match
		
				#Depth match
				for message in self.temp_message_keys:

					#Loop through the messages in the message/response pairs
		
					depth_found = 0
					matched_words = []
					random.shuffle(self.depth_words)
		
					#Loop through the current depth words
					#Find if at least 2 are contained in the message
					for word in self.depth_words:
		
						if message.find(word) != -1:
		
							depth_found += 1
							matched_words.append(word)
		
						if depth_found == 2:
			
							#At least 2 depth words matched the message, use the message for the response
							self.Xchatlog.append(f"{self.bot_name} (Thinking): Depth match found for: {" ".join(matched_words)}")
							self.CHELSEA_previous_response = self.botReply(random.choice(self.message_dict2[self.current_mood["mood"]][message]))

							return True
		
			elif len(self.current_topics) > 0:

				#5/6 odds topic match
		
				#Topic match
				for message in self.temp_message_keys:

					#Loop through the messages in the message/response pairs
		
					#Loop through the current topic words
					#Find if one is contained in the message
					for topic in self.current_topics:
		
						if message.find(topic) != -1:
			
							#Matched a topic word to the message, use the message for the response
							self.Xchatlog.append(f"{self.bot_name} (Thinking): Topic match found for: {topic}.")
							self.CHELSEA_previous_response = self.botReply(random.choice(self.message_dict2[self.current_mood["mood"]][message]))

							return True
		
		return False
	
	def use_imagination2(self):

		#Experimental
		#	Still often produces nonsense results
		#	Not sure if she needs to learn a lot more to have more patterns available, or something needs to be adjusted?
		#	Added code to try and make sure she doesn't end on a permanent neutral (stop) word, but still often produces nonsense.
		#	Have to admit, though, some of the half nonsense can be funny.
		# 	For now just lowered the odds of this being triggered, as CHELSEA can end up learning the nonsense as message/response pairs, don't want that too much

		ngram_count = len(self.bigrams) + len(self.trigrams)
		
		if ((ngram_count > 20000 and ngram_count < 80,000 and random.randint(1, 60) == 1) or (ngram_count > 80,000 and random.randint(1, 50) == 1)):

			#Check if topics or depth words empty
			chosen_word = ''
			topic_words_empty = False if len(self.current_topics) > 0 else True
			depth_words_empty = False if len(self.depth_words) > 0 else True

			#If both empty, don't use
			if topic_words_empty and depth_words_empty:
				return False

			word_type = ''
			coin_flip1 = random.randint(1, 2)
			if (not topic_words_empty) and (coin_flip1 == 1 or depth_words_empty):
				
				#Using topic word
				word_type = 'topic'
				chosen_word = random.choice(list(self.current_topics))
				
				if chosen_word in self.imagined_blacklist:
					
					self.imagined_blacklist_counter += 1
					return False

			else:
				
				#Using depth word
				word_type = 'depth'
				chosen_word = random.choice(self.depth_words)
				
				if chosen_word in self.imagined_blacklist:
					
					self.imagined_blacklist_counter += 1
					return False

			#Prevent the same words from being used in this method repeatedly, at least for a while
			self.imagined_blacklist.append(chosen_word)
			self.imagined_blacklist_counter += 1
			if self.imagined_blacklist_counter == 10:
				
				self.imagined_blacklist_counter = 1
				del self.imagined_blacklist[0]

			direction = 'forward' if random.randint(1, 2) == 1 else 'reverse'
			imagined_response = ''
			previous_word, next_word = ['', '']

			#Maybe instead of copying and pasting the whole code to go in reverse, only need to if/else for certain parts dealing with next_word, previous_word?
			#Not sure how to do this since the forward and reverse dictionaries may be different sizes, zip won't work?
			#Will make them separate for now
			#This would seem to clean up the code, but may greatly reduce clarity with all of the if/else forward/reverse parts, so maybe not the best idea?
			if direction == 'forward':

				#Will start with base word and go forward when making the chain

				#Get first matching trigram/bigram for setup
				chosen_key = ''
				search_key = f"{chosen_word} "
				for key in self.trigrams:

					#Look for matching key in trigrams first
					
					if key.startswith(search_key):

						#Found matching trigram
						
						chosen_key = key
						previous_word = chosen_key.split(" ")[1]

						valid_emotions = {self.current_mood['mood'], "permanent neutral", "temp neutral"} 
						valid_words = {word: value for word, value in self.trigrams[chosen_key].items() if self.dictionary[word]['emotion'] in valid_emotions}
						
						if len(valid_words) == 0:

							#No possible match for current mood, return from the method
							return False

						#Given the number of times the words (population) have been seen (weights), get the most probable next word
						next_word = random.choices(
							population=list(valid_words.keys()),
							weights=list(valid_words.values()),
							k=1
						)

						next_word = next_word[0]

						imagined_response = f"{chosen_key} {next_word}"

						break
				else:
					
					if chosen_word in self.bigrams:

						#Found matching bigram

						valid_emotions = {self.current_mood['mood'], "permanent neutral", "temp neutral"} 
						valid_words = {word: value for word, value in self.bigrams[chosen_word].items() if self.dictionary[word]['emotion'] in valid_emotions}
						
						if len(valid_words) == 0:

							#No pissible match found for current mood, return from the method
							return False

						#Given the number of times the words (population) have been seen (weights), get the most probable next word
						next_word = random.choices(
							population=list(valid_words.keys()),
							weights=list(valid_words.values()),
							k=1
						)

						next_word = next_word[0]

						imagined_response = f"{chosen_word} {next_word}"

						previous_word = f"{chosen_word} {next_word}"

					else:
						return False
		
				#Build the chain from the initial setup
				chain_loops_counter = 0
				number_of_chain_loops = random.randint(3, 8)
				end_found = False
				while not end_found:

					if f"{previous_word} {next_word}" in self.trigrams:

						#Found match in trigrams

						valid_emotions = {self.current_mood['mood'], "permanent neutral", "temp neutral"} 
						valid_words = {word: value for word, value in self.trigrams[f"{previous_word} {next_word}"].items() if self.dictionary[word]['emotion'] in valid_emotions}
						
						if len(valid_words) == 0:

							#No possible match under current mood, return from method
							return False

						#Given the number of times the words (population) have been seen (weights), get the most probable next word
						previous_word = next_word
						next_word = random.choices(
							population=list(valid_words.keys()),
							weights=list(valid_words.values()),
							k=1
						)

						next_word = next_word[0]

						imagined_response = f"{imagined_response} {next_word}"

						chain_loops_counter += 1
						if chain_loops_counter == number_of_chain_loops:
							
							if self.dictionary[next_word]['emotion'] != 'permanent neutral':

								#End is not a stop word, end chain
								end_found = True
						
						elif chain_loops_counter - number_of_chain_loops >= 3:

							#Reached limit, end chain
							end_found = True

						continue
					
					elif next_word in self.bigrams:

						#Found match in bigrams

						valid_emotions = {self.current_mood['mood'], "permanent neutral", "temp neutral"} 
						valid_words = {word: value for word, value in self.bigrams[next_word].items() if self.dictionary[word]['emotion'] in valid_emotions}
						
						if len(valid_words) == 0:

							#No possible match for current mood found, return from the method
							return False

						#Given the number of times the words (population) have been seen (weights), get the most probable next word
						previous_word = next_word
						next_word = random.choices(
							population=list(valid_words.keys()),
							weights=list(valid_words.values()),
							k=1
						)

						next_word = next_word[0]

						imagined_response = f"{imagined_response} {next_word}"
						
						chain_loops_counter += 1
						if chain_loops_counter == number_of_chain_loops:
							
							if self.dictionary[next_word]['emotion'] != 'permanent neutral':

								#End not stop word, end chain
								end_found = True

						elif chain_loops_counter - number_of_chain_loops >= 3:

							#Reached limit, end chain
							end_found = True

						continue
					
					else:
						return False

			else: #imagined response in reverse, start with base word on end and build chain in reverse

				#Start with first trigram/bigram for setup
				chosen_key = ''
				search_key = f" {chosen_word}"
				for key in self.reverse_trigrams:
					
					if key.endswith(search_key):

						#Found match in reverse trigrams
						
						chosen_key = key
						previous_word = chosen_key.split(" ")[0]

						valid_emotions = {self.current_mood['mood'], "permanent neutral", "temp neutral"} 
						valid_words = {word: value for word, value in self.reverse_trigrams[chosen_key].items() if self.dictionary[word]['emotion'] in valid_emotions}
						
						if len(valid_words) == 0:

							#No possible match found under current mood, return from the method
							return False

						#Given the number of times the words (population) have been seen (weights), get the most probable next word
						next_word = random.choices(
							population=list(valid_words.keys()),
							weights=list(valid_words.values()),
							k=1
						)

						next_word = next_word[0]

						imagined_response = f"{next_word} {chosen_key}"

						break
				else:
					
					if chosen_word in self.reverse_bigrams:

						#Found match in reverse bigrams

						valid_emotions = {self.current_mood['mood'], "permanent neutral", "temp neutral"} 
						valid_words = {word: value for word, value in self.reverse_bigrams[chosen_word].items() if self.dictionary[word]['emotion'] in valid_emotions}
						
						if len(valid_words) == 0:

							#No possible match found under current mood, return from the method
							return False

						#Given the number of times the words (population) have been seen (weights), get the most probable next word
						next_word = random.choices(
							population=list(valid_words.keys()),
							weights=list(valid_words.values()),
							k=1
						)

						next_word = next_word[0]

						imagined_response = f"{next_word} {chosen_word}"

						previous_word = f"{next_word} {chosen_word}"

					else:
						return False
		
				#Build the reverse chain from the initial setup
				chain_loops_counter = 0
				number_of_chain_loops = random.randint(3, 8)
				end_found = False
				while not end_found:

					if f"{next_word} {previous_word}" in self.reverse_trigrams:

						#Match found in reverse trigrams

						valid_emotions = {self.current_mood['mood'], "permanent neutral", "temp neutral"} 
						valid_words = {word: value for word, value in self.reverse_trigrams[f"{next_word} {previous_word}"].items() if self.dictionary[word]['emotion'] in valid_emotions}
						
						if len(valid_words) == 0:

							#No possible match found under current mood, return from the method
							return False

						#Given the number of times the words (population) have been seen (weights), get the most probable next word
						previous_word = next_word
						next_word = random.choices(
							population=list(valid_words.keys()),
							weights=list(valid_words.values()),
							k=1
						)

						next_word = next_word[0]

						imagined_response = f"{next_word} {imagined_response}"

						chain_loops_counter += 1
						if chain_loops_counter == number_of_chain_loops:
							
							if self.dictionary[next_word]['emotion'] != 'permanent neutral':

								#Reverse end word not a stop word, end chain
								end_found = True
						
						elif chain_loops_counter - number_of_chain_loops >= 3:

							#Reached limit, end chain
							end_found = True								
						
						continue
					
					elif next_word in self.reverse_bigrams:

						#Match found in reverse bigrams

						valid_emotions = {self.current_mood['mood'], "permanent neutral", "temp neutral"} 
						valid_words = {word: value for word, value in self.reverse_bigrams[next_word].items() if self.dictionary[word]['emotion'] in valid_emotions}
						
						if len(valid_words) == 0:

							#No possible match found under current mood, return from method
							return False

						#Given the number of times the words (population) have been seen (weights), get the most probable next word
						previous_word = next_word
						next_word = random.choices(
							population=list(valid_words.keys()),
							weights=list(valid_words.values()),
							k=1
						)

						next_word = next_word[0]

						imagined_response = f"{next_word} {imagined_response}"

						chain_loops_counter += 1
						if chain_loops_counter == number_of_chain_loops:
						
							if self.dictionary[next_word]['emotion'] != 'permanent neutral':

								#reverse end word not a stop word, end chain
								end_found = True
						
						elif chain_loops_counter - number_of_chain_loops >= 3:

							#Reached limit, end chain
							end_found = True
						
						continue
					
					else:
						return False
					
			#Chain must be valid, give the imagined chain as response

			self.Xchatlog.append(f"{self.bot_name} (Thinking): Trigram/Bigram chain in {direction} for {word_type} word '{chosen_word}' imagined.")
			self.CHELSEA_previous_response = self.botReply(imagined_response)
			return True
		
		return False
	
	def check_single_term_match(self):
		
		#Check for single term match under current mood, ignore neutral words
		#Only activated when CHELSEA has learned enough, though this can easily be adjusted.
		
		response_made = False
		if ((self.dictionary_count >= 4500 and self.response_count >= 2700 and random.randint(1, 30) == 1) or (self.dictionary_count >= 2000 and self.dictionary_count < 4500 and self.response_count >= 500 and self.response_count < 2700 and random.randint(1, 40) == 1)):
		
			response_made = False
		
			#Coin flip
			if (random.randint(1, 2) == 1):
		
				#single term match from user message words
				for word in self.message_words:
		
					try:
		
						if (self.dictionary[word]['emotion'] == "temp neutral" or self.dictionary[word]['emotion'] == "permanent neutral"):
							#Ignore neutral words
							continue
		
						else:
		
							for message in self.temp_message_keys: #Note: self.temp_message_keys was randomly shuffled in a different method 
		
								if message.find(word) != -1:
		
									#Word in user message words was found in CHELSEA's message, respond using that message
									self.Xchatlog.append(f"{self.bot_name} (Thinking): Single term match found for term: {word}")
									self.CHELSEA_previous_response = self.botReply(random.choice(self.message_dict2[self.current_mood["mood"]][message]))
									response_made = True
									break
		
							if response_made:
								break
		
					except(KeyError):
						#Ignore words not found in dictionary
						continue
		
				if response_made:
					return True
		
			else:
		
				#Single term match for a word associated with highest association count from user message word
				for word in self.message_words:
		
					temp_dictionary = {}
		
					try:
		
						temp_dictionary = self.dictionary[word]['associated']
		
						if (len(temp_dictionary) == 0):
							#Ignore words that don't have associated words
							continue
		
					except(KeyError):
						#Ignore words not found in dictionary
						continue
		
					#Find the associated word with the highest association
					temp_highest = max(temp_dictionary.values())
					highest_associated = [k for k, v in temp_dictionary.items() if v == temp_highest]
					highest_associated_chosen = ''
		
					if (len(highest_associated) == 1):
						#Only one highest associated word
						highest_associated_chosen = highest_associated[0]
		
					else:
						#Multiple highest associated word, choose one at random
						highest_associated_chosen = random.choice(highest_associated)
		
					try:
						if (self.dictionary[highest_associated_chosen]['emotion'] == "temp neutral" or self.dictionary[highest_associated_chosen]['emotion'] == "permanent neutral"):
							#Ignore neutral words
							continue
		
					except(KeyError):
						#Ignore word not found in dictionary
						continue		
		
					for message in self.temp_message_keys: #Note: self.temp_message_keys was randomly shuffled in a different method 
		
						if message.find(highest_associated_chosen) != -1:
		
							#Highest associated word of word in user message words was found in CHELSEA's message, respond using that message
							self.Xchatlog.append(f"{self.bot_name} (Thinking): Single term associated match found for associated term: {highest_associated_chosen}")
							self.CHELSEA_previous_response = self.botReply(random.choice(self.message_dict2[self.current_mood["mood"]][message]))
							response_made = True
							break
		
					if response_made:
						break
		
				if response_made:
					return True
		
		#Dice roll for single term match failed
		return False

	def find_topic_in_questions(self, isare):

		#Attempt to find a 'why is/are' question containing one of the current topics
		
		if len(self.current_topics) > 1:
		
			random.shuffle(self.temp_questions)
			temp_question = ""
			topic_match_found = False
		
			for question in self.temp_questions:
		
				topic_count = 0
				for topic in self.current_topics:
		
					if question.find(topic) != -1:
						#Topic found in question, increase count
						topic_count += 1
		
						if topic_count == 2:
							#Need at least 2 topics in question
							break
		
				if topic_count == 2:
		
					temp_question = question
					topic_match_found = True
					break
		
			if topic_match_found:
		
				#Match found, asking 'why is/are' question according to at least 2 of the current topics
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked topic relevant why {isare} question, waiting for valid answer.")
				self.CHELSEA_previous_response = self.botReply(temp_question)
				self.unanswered[f"why {isare}"] = True
				return True
		
		return False

	def give_random_or_question_response(self):
		
		if random.randint(1, 6) == 1:
		
			#Ask unanswered question
		
			if (random.randint(1, 2) == 1 and len(self.unanswered_questions["what"]) > 0):
		
				#Ask 'what is/are' question
		
				if (random.randint(1, 3) == 1):
					#1/3 dice roll
		
					random.shuffle(self.popular_words[self.current_mood["mood"]])
					response_made = False
		
					for word in self.popular_words[self.current_mood["mood"]]:
		
						try:
							#Attempt to find a question based on one of the popular words under CHELSEA's current mood
							#Respond with the question if found

							self.unanswered_questions["what"][f"what is/are {word}?"]
							self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked what is/are question for '{word}' in popular '{self.current_mood["mood"]}' words, waiting for valid answer.")
							self.CHELSEA_previous_response = self.botReply(f"what is/are {word}?")
							self.unanswered["what"] = True
							response_made = True
							break
		
						except(KeyError):
							#Question not found in dictionary containing current popular word
							continue
		
					if response_made:
						return
		
					for word in self.popular_words[self.current_mood["mood"]]:
		
						#Look for words associated with the popular words
						for associated_word in self.dictionary[word]["associated"].keys():
		
							try:
								#Attempt to find a question based on one of the words associated with one of popular words under CHELSEA's current mood
								#Respond with the question if found

								self.unanswered_questions["what"][f"what is/are {associated_word}?"]
								self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked what is/are question for '{associated_word}' associated to '{word}' in popular '{self.current_mood["mood"]}' words, waiting for valid answer.")
								self.CHELSEA_previous_response = self.botReply(f"what is/are {associated_word}?")
								self.unanswered["what"] = True
								response_made = True
								break
		
							except(KeyError):
								#Question not found in dictionary containing current word associated with current popular word
								continue
		
						if response_made:
							return
						
				else:
					#2/3 dice roll
					#Find a question containing one of the words used in previous user reply
		
					random.shuffle(self.message_words)
					response_made = False
		
					for word in self.message_words:
		
						try:
							#Attempt to find a question containing one of the words in the previous user reply
							#If found, respond with the question

							self.unanswered_questions["what"][f"what is/are {word}?"]
							self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked what is/are question for '{word}' in previous user reply, waiting for valid answer.")
							self.CHELSEA_previous_response = self.botReply(f"what is/are {word}?")
							self.unanswered["what"] = True
							response_made = True
							break
		
						except(KeyError):
							#Question not found in dictionary containing word from previous user reply
							continue
		
					if response_made:
						return
		
				#No unanswered question match found from previous user reply words or popular words, use random question instead
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked random what is/are question, waiting for valid answer.")
				self.CHELSEA_previous_response = self.botReply(random.choice(list(self.unanswered_questions["what"].keys())))
				self.unanswered["what"] = True
		
			else:
		
				#Ask 'why is/are' question
				if (random.randint(1, 2) == 1 and len(self.unanswered_questions["why is"]) > 0):
		
					#why is
					self.temp_questions = list(self.unanswered_questions["why is"].keys())
		
					#Try to find a current topic relevant 'why is' question first
					if self.find_topic_in_questions("is"):
						return
		
					#Ask random 'why is' question
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked random why is question, waiting for valid answer.")
					self.CHELSEA_previous_response = self.botReply(random.choice(self.temp_questions))
					self.unanswered["why is"] = True
		
				elif (len(self.unanswered_questions["why are"]) > 0):
		
					#why are
					self.temp_questions = list(self.unanswered_questions["why are"].keys())
		
					#Try to find a current topic relevant 'why are' question first
					if self.find_topic_in_questions("are"):
						return
		
					#Ask random 'why are' question
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked random why are question, waiting for valid answer.")
					self.CHELSEA_previous_response = self.botReply(random.choice(self.temp_questions))
					self.unanswered["why are"] = True

		else:
		
			#Give random response from current mood
			#The message is randomly chosen from the randomly chosen list of messages.
			#Note: Might be better to separate this into multiple statements instead, for clarity.

			random_response = random.choice(random.choice(list(self.message_dict2[self.current_mood["mood"]].values())))

			#If recently gave dictionary word definition as response, prevent this from happening again for a while
			if self.random_response_counter > 0:
				while re.search(r'([a-z0-9\-\']+) (is|are|the) .*', random_response):
					random_response = random.choice(random.choice(list(self.message_dict2[self.current_mood["mood"]].values())))
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Gave dictionary word definition as response recently, prevented doing this again. Counter: {self.random_response_counter + 1} / 10")
				self.random_response_counter += 1

			if re.search(r'([a-z0-9\-\']+) (is|are|the) .*', random_response):
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Gave dictionary word definition as response.")
				self.random_response_counter = 1

			#Possibly reset counter
			if self.random_response_counter == 10:
				self.random_response_counter = 0

			self.Xchatlog.append(f"{self.bot_name} (Thinking): Gave random response.")	
			self.CHELSEA_previous_response = self.botReply(random_response)

	def chat(self, sr, r, source):

		#All return statements cause the chat loop in 'chatbotCHELSEA.py' to continue, unless user reply is 'exit the chat'.
		#A return of True from one of these methods causes a return from this method, basically saying 'The user reply was handled with an appropriate response'.
		#Otherwise it falls through to the next method.
		
		if self.get_user_reply(sr, r, source):

			#User spoke command, switch to text input mode
			if self.user_message == 'disable speech':
				self.enabled_modes['speech_recognition'] = False

			#User typed command, switch to speech recognition mode
			elif self.user_message == 'enable speech':
				self.enabled_modes['speech_recognition'] = True

			#If self.user_message == 'exit the chat', returning will end up exiting the chat and then output all memory
			#Else, chat loop will continue
			return
		
		if self.math_comprehension():
			return
		
		if self.chelsea_birthday():
			return

		#Identity parts
		if self.ask_if_is():
			return
		if self.ask_if_user_is():
			return
		if self.tell_what_is():
			return

		#Initial counts and markings
		self.filter_user_reply()
		self.get_exclaim_count()
		self.split_user_reply()
		self.reset_temp_vars()
		self.detect_emotion_words()
		self.getReplyMood()
		self.addToMood()
		self.detect_unknown_words()
		self.add_to_word_counts()
		self.mark_associated_words()
		self.get_bigrams2()
		self.get_trigrams2()
		self.get_topic_counts()
		self.determine_current_topics()
		self.add_to_previous_pairs()
		self.get_depth_words()
		self.get_popular_words()
		self.check_for_answer_what()
		if self.check_for_answer_why():
			return

		#Responses
		if self.give_clarification():
			return
		if self.ask_what_feel():
			return
		if self.ask_if_like():
			return
		if self.ask_which_better():
			return
		if self.ask_why_is():
			return
		if self.ask_most_question():
			return

		#Must go after other questions otherwise this method will capture all of those question patterns		
		if self.answer_fuzzy_question():
			return

		if self.user_birthday():
			return		
		
		if self.ask_user_details():
			return
		self.confirm_user_details_what()

		if self.ask_past_user_details():
			return
		if self.confirm_past_user_details():
			return

		if self.user_give_details_favorite():
			return
		if self.user_give_details_like():
			return
		if self.user_give_details_have():
			return
		if self.user_give_details_am():
			return
		if self.confirm_user_why_favorite():
			return
		if self.confirm_user_why_like():
			return
		if self.confirm_user_why_have():
			return
		if self.confirm_user_why_am():
			return

		if self.funny_response():
			return
		
		if self.recall_past_topic():
			return
		
		if self.check_exact_message_match():
			return
		if self.check_partial_message_match():
			return

		if self.learn_new_response():
			return
		
		if self.check_fuzzy_message_match():
			return
		if self.check_topic_or_depth_match():
			return
		if self.use_imagination2():
			return
		if self.check_single_term_match():
			return
		
		self.give_random_or_question_response()

		return

