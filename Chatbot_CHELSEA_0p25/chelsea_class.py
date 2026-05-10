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

# Chatbot CHELSEA: CHat Emotion Logic SEnse Automator (0.25) (BETA)

import json
import os
import re
import random
from datetime import datetime
import subprocess
import sys
import time
from CHELSEA_MATH_LOGIC import CHELSEA_Math_Logic

class chelsea:
	def __init__(self, bot_name, speech_rec_enabled):
		self.bot_name = bot_name
		self.dictionary = {}
		self.bigram_dictionary = {}
		self.trigram_dictionary = {}
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
		self.MODEL_PATH = "/YOUR/PATH/.local/share/piper-tts/piper-voices/en_US-amy-low.onnx"
		self.piper_proc = None

		#See if speech recognition enabled or disabled
		self.speech_rec_enabled = speech_rec_enabled

	#Input memory
	def input_dictionary(self):

		#Load the dictionary of words with ties to emotions
		with open(f"{self.file_path}dictionary.json", 'r') as dictionary_file:
			self.dictionary = json.load(dictionary_file)
		
		self.dictionary_count = len(self.dictionary.keys())

	def input_bigram_dict(self):

		#Load the dictionary of bigrams (2 word groups)
		with open(f"{self.file_path}bigramDictionary.json", 'r') as bigram_dictionary_file:
			self.bigram_dictionary = json.load(bigram_dictionary_file)

	def input_trigram_dict(self):

		#Load the dictionary of trigrams (3 word groups)
		with open(f"{self.file_path}trigramDictionary.json", 'r') as trigram_dictionary_file:
			self.trigram_dictionary = json.load(trigram_dictionary_file)

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

		except(FileNotFoundError):

			#Self identity file doesn't exist, new chatbot
			self.chelsea_self = {"iam": [], "iamnot": []}

	def input_memory(self):

		#Input all memory from files
		self.input_dictionary()
		self.input_bigram_dict()
		self.input_trigram_dict()
		self.input_message_dictionary()
		self.input_unanswered_questions()
		self.input_self()

		#TTS_FLAG

		#Open the temp file for writing to with piper subprocess:
		self.temp_piper_output_file = open('temp_piper_output', 'wb', buffering=0)
		self.load_tts_subprocess()

		#Make sure voice model and other parts in piper are fully loaded before the initial message
		time.sleep(4)

	def input_user_self(self):

		#Get self.username
		self.botReply("What is your name?")
		self.username = input("")
		self.username = re.sub(r"( )", "_", self.username)

		#Input the user file for the current user, if it exists
		try: 

			with open(f"{self.file_path}{self.username}.json", 'r') as user_file:
				self.user_self = json.load(user_file)

		except(FileNotFoundError):

			#New user detected
			self.user_self = {'happy': 0, 'angry': 0, 'sad': 0, 'afraid': 0, 'uam': [], 'uamnot': []}

	def load_tts_subprocess(self):
		#Load the subprocesses for text-to-speech
		#TTS_FLAG

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
		#TTS_FLAG

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
		with open(f"{self.file_path}dictionary.json", 'w') as dictionary_file:
			json.dump(self.dictionary, dictionary_file, indent=4)

	def output_bigram_dict(self):
		with open(f"{self.file_path}bigramDictionary.json", 'w') as bigram_dictionary_file:
			json.dump(self.bigram_dictionary, bigram_dictionary_file, indent=4)

	def output_trigram_dict(self):
		with open(f"{self.file_path}trigramDictionary.json", 'w') as trigram_dictionary_file:
			json.dump(self.trigram_dictionary, trigram_dictionary_file, indent=4)
			
	def output_message_dictionary(self):
		with open(f"{self.file_path}messageDictionary2.json", 'w') as message_dictionary_file:
			json.dump(self.message_dict2, message_dictionary_file, indent=4)

	def output_unanswered_questions(self):
		with open(f"{self.file_path}unanswered_questions2.json", 'w') as unanswered_questions_file:
			json.dump(self.unanswered_questions, unanswered_questions_file, indent=4)

	def output_self(self):
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
		data_file.write(f"Words in emotion dictionary: {len(self.dictionary.keys())}\n")
		for emotion in self.nEmotions:
			data_file.write(f"Number of {emotion} words in dictionary: {len([word for word in self.dictionary.keys() if self.dictionary[word]["emotion"] == emotion])}\n")
		data_file.write("\n")

		#Output number of known bigrams or trigrams
		data_file.write(f"Number of seen bigrams: {len(self.bigram_dictionary.keys())}\n")
		data_file.write(f"Number of seen trigrams: {len(self.trigram_dictionary.keys())}\n\n")
		
		#Output number of message/response pairs in memory
		message_count = 0
		for emotion in self.nEmotions:
			message_count += len(self.message_dict2[emotion])
			data_file.write(f"Number of {emotion} message/response pairs: {len(self.message_dict2[emotion])}\n")
		data_file.write(f"Total message/response pairs: {message_count}")

		#Output number of unanswered questions
		data_file.write(f"\n\nNumber of unanswered 'what is/are' questions: {len(self.unanswered_questions["what"].keys())}")
		data_file.write(f"\nNumber of unanswered 'why is' questions: {len(self.unanswered_questions["why is"].keys())}")
		data_file.write(f"\nNumber of unanswered 'why are' questions: {len(self.unanswered_questions["why are"].keys())}")
		
		#Output current popular words
		for emotion in self.nEmotions:
			data_file.write(f"\n\nPopular {emotion} words: {", ".join(self.popular_words[emotion])}")
		data_file.close()

	def output_memory(self):

		#Output all memory to files
		self.output_dictionary()
		self.output_bigram_dict()
		self.output_trigram_dict()
		self.output_message_dictionary()
		self.output_unanswered_questions()
		self.output_self()
		self.output_chatlogs()
		self.output_chelsea_data()

	def output_user_self(self):

		#Output user profile

		#Get educated guess of user's mood
		user_emotions = {}
		for emotion in self.nEmotions:
			user_emotions[emotion] = self.user_self[emotion]
		user_overall_mood = self.getMood2(user_emotions, True)
		self.user_self['mood'] = f"{self.username} seems to be a(n) {user_overall_mood} person."
		
		#Output the user's details
		with open(f"{self.file_path}{self.username}.json", 'w') as user_file:
			json.dump(self.user_self, user_file, indent=4)
		
	#Other methods
	def addToMood(self):

		#Store previous mood to compare to next
		previous_mood = self.current_mood['mood']

		#Add the emotional values of the user reply to CHELSEA's emotional values
		for emotion in self.nEmotions:
			self.current_mood[emotion] += self.reply_mood[emotion]

		#Change mood, pitch, and speaking speed according to CHELSEA's emotional values
		temp_dict = { 'happy': self.current_mood['happy'], 'angry': self.current_mood['angry'], 'sad': self.current_mood['sad'], 'afraid': self.current_mood['afraid'] }
		self.current_mood["mood"] = self.getMood2(temp_dict, True)
		self.current_mood["pitch"] = self.pitches[self.current_mood["mood"]]
		self.current_mood["speed"] = self.speeds[self.current_mood["mood"]]

		#Output her current mood to the extended chatlog
		self.Xchatlog.append(f"{self.bot_name} (Thinking): I feel {self.current_mood["mood"]}")

		#TTS_FLAG
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
		self.botReply(f"hello, {self.username}")

	def get_user_reply(self, sr, r, source):

		#STT_FLAG

		if not self.speech_rec_enabled:
			
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
	
	def ask_if_is(self):

		#Ask CHELSEA what CHELSEA is or is not
		match1 = re.search(r"what are you( not)?\?*$", self.user_message)
		if (match1):

			#'What are you...?' question format found

			if (not(match1.group(1)) and len(self.chelsea_self['iam']) != 0):

				#Asked 'what are you' question, give random answer from self memory
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Was asked what I am, have an answer.")
				self.botReply(f"I am {random.choice(self.chelsea_self['iam'])}")

				return True
			
			elif (match1.group(1) and len(self.chelsea_self['iamnot']) != 0):
			
				#Asked 'what are you not' question, give random answer from self memory
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Was asked what I am not, have an answer.")
				self.botReply(f"I am not {random.choice(self.chelsea_self['iamnot'])}")

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
				self.botReply(f"You are {re.sub(r"(your)", "my", random.choice(self.user_self['uam']))}")
				
				return True
			
			elif (match1.group(1) and len(self.user_self['uamnot']) != 0):

				#Asked 'what am i not' question, give random answer from user profile memory
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Was asked what user is not, have an answer.")
				self.botReply(f"You are not {re.sub(r"(your)", "my", random.choice(self.user_self['uamnot']))}")
				
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
	
	def tell_what_user_is(self):

		#Deal with current user's identity properties	

		match1 = re.search(r"^(?:i am|i'm) (not )?(.*)", self.user_message)

		if (match1):

			#'i am/i'm ...' message found
		
			if (not(match1.group(1))):

				#'not' not detected
		
				breakout = False
				for uam in self.user_self['uam']:
		
					if (uam == match1.group(2)):

						#Found agreement with 'i am'
		
						uam = re.sub(r"(your)", "my", uam)
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found agreement with 'User am'.")
						self.botReply(f"{random.choice(self.agree)}you are {uam}")
						breakout = True
						break
		
				#CHELSEA responded, return True
				if (breakout):
					return True
		
				for uamnot in self.user_self['uamnot']:
		
					if (uamnot == match1.group(2)):

						#Found disagreement with 'i am'
		
						uamnot = re.sub(r"(your)", "my", uamnot)
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found disagreement with 'User am'.")
						self.botReply(f"{random.choice(self.disagree)}you are not {uamnot}")
						breakout = True
						break
		
				#CHELSEA responded, return True
				if (breakout):
					return True
		
				#Neither agreement or disagreement, learn new property of user
				self.user_self['uam'].append(match1.group(2))	
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new 'User am'.")
		
			else:

				#'not' detected in message
		
				breakout = False
				for uamnot in self.user_self['uamnot']:
		
					if (uamnot == match1.group(2)):

						#Agreement with 'i am not' found
		
						uamnot = re.sub(r"(your)", "my", uamnot)
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found agreement with 'User am not'.")
						self.botReply(f"{random.choice(self.agree)}you are not {uamnot}")
						breakout = True
						break
		
				#CHELSEA responded, return True
				if (breakout):
					return True
		
				for uam in self.user_self['uam']:
		
					if (uam == match1.group(2)):

						#Disagreement with 'i am not' found
		
						uam = re.sub(r"(your)", "my", uam)
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Found disagreement with 'User am not'.")
						self.botReply(f"{random.choice(self.disagree)}you are {uam}")
						breakout = True
						break
		
				#CHELSEA responded, return True
				if (breakout):
					return True

				#Neither agreement or disagreement, learn new property of user 'not'		
				self.user_self['uamnot'].append(match1.group(2))		
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new 'User am not'.")
		
		#CHELSEA did not respond, return False		
		return False

	def filter_user_reply(self):
		
		#Filter certain chars from userMessage
		self.user_message = re.sub(r"([^a-z0-9, \"'\-\?!])", '', self.user_message)

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

					#Word not neutral, add 1 times exclaim count to reply mood and user mood
					self.reply_mood[self.dictionary[word]['emotion']] += (1 * self.exclaim_count)
					self.user_self[self.dictionary[word]['emotion']] += (1 * self.exclaim_count)

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

	def get_bigrams(self):
		#FLAG
		
		#Identify new bigrams or add to counts of existing ones, then sort bigram dictionary by highest 'seen' counts
		
		for n in range(len(self.message_words)):
		
			if n != len(self.message_words) - 1:

				#If at end of message words, no more bigrams to detect
		
				try:

					#If the bigram already exists in the dictionary, add to the count of times it has been seen
					self.bigram_dictionary[f"{self.message_words[n]} {self.message_words[n+1]}"]["seen"] += 1
		
				except(KeyError):
		
					#bigram doesn't already exist in the dictionary
					try:
		
						#Create new dictionary entry for the bigram
						self.bigram_dictionary[f"{self.message_words[n]} {self.message_words[n+1]}"] = {
							"seen": 1, 
							"emotions": [self.dictionary[self.message_words[n]]["emotion"], self.dictionary[self.message_words[n+1]]["emotion"]]
							}
		
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new bigram: '{self.message_words[n]} {self.message_words[n+1]}'")
		
					except(KeyError):
							#bigram word(s) not found in emotion dictionary, ignore
							continue
		
		#Sort bigram dictionary with the number of times the bigrams have been seen, most at top
		self.bigram_dictionary = dict(sorted(self.bigram_dictionary.items(), key=lambda item: item[1]["seen"], reverse=True))

	def get_trigrams(self):
		#FLAG
		
		#Identify new trigrams or add to counts of existing ones, then sort trigram dictionary by highest 'seen' counts
		
		for n in range(len(self.message_words)):
		
			if n != 0 and n != len(self.message_words) - 1:

				#If at end of message words, no more trigrams to detect
		
				try:
					#If trigram already in dictionary, add to count of times it has been seen
					self.trigram_dictionary[f"{self.message_words[n-1]} {self.message_words[n]} {self.message_words[n+1]}"]["seen"] += 1
		
				except(KeyError):
		
					#trigram not found in dictionary

					try:
		
						#Create new dictionary entry for trigram
						self.trigram_dictionary[f"{self.message_words[n-1]} {self.message_words[n]} {self.message_words[n+1]}"] = {
							"seen": 1, 
							"emotions": [self.dictionary[self.message_words[n-1]]["emotion"], self.dictionary[self.message_words[n]]["emotion"], self.dictionary[self.message_words[n+1]]["emotion"]]
							}
		
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Learned new trigram: '{self.message_words[n-1]} {self.message_words[n]} {self.message_words[n+1]}'")
		
					except(KeyError):
						#trigram word(s) not found in emotion dictionary, ignore
						continue
		
		#Sort trigram dictionary with the number of times the trigrams have been seen, most at top
		self.trigram_dictionary = dict(sorted(self.trigram_dictionary.items(), key=lambda item: item[1]["seen"], reverse=True))

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
		
		if (not(len(self.topics.keys()) == 0)):

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

	def answer_whq_question(self):
		
		#Check for possible matching answer to What Question in both keys and values under current mood
		response_made = False
		whq_match_object = re.search(r"what (is|are) ([a-z '\-]+)\?*$", self.user_message)

		self.temp_message_keys = list(self.message_dict2[self.current_mood["mood"]].keys())
		random.shuffle(self.temp_message_keys) #Note: This shuffled list is potentially re-used in other parts of the script
		
		if (whq_match_object):
			#Pattern 'what/why/etc is/are _1_?' found in user reply

			#Setup to look for pattern '_1_ is/are ___'
			temp_message_values = list(self.message_dict2[self.current_mood["mood"]].values())
			random.shuffle(temp_message_values)
			partial_message = f"{whq_match_object.group(2)} {whq_match_object.group(1)}"
			
			#Check values
			for message in temp_message_values:
		
				#Choose a random valid answer from list of responses
				message = random.choice(message)
		
				#Prevent duplicate response
				if (message == self.CHELSEA_previous_response):
					continue
		
				if message.find(partial_message) != -1:
					#Response contains '_1_ is/are ___'
					#Use response to answer question

					self.Xchatlog.append(f"{self.bot_name} (Thinking): WH-Q question match found in values.")
					self.CHELSEA_previous_response = self.botReply(message)
					response_made = True
					break
		
			if response_made:
				return True
		
			#Check keys
			for message in self.temp_message_keys:
		
				#Prevent duplicate response
				if (message == self.CHELSEA_previous_response):
					continue
		
				if message.find(partial_message) != -1:
					#Response contains '_1' is/are ___'
					#Use response to answer question

					self.Xchatlog.append(f"{self.bot_name} (Thinking): WH-Q question match found in keys.")
					self.CHELSEA_previous_response = self.botReply(message)
					response_made = True
					break
		
			if response_made:
				return True
		
		#User reply does not match pattern of asking 'what/why/etc' question
		return False
	
	def give_clarification(self):
		
		#Check for question about previous message meaning
		
		response_made = False
		meaning_match = re.search(r"(what (do you|does that) mean|(can you|(do you|can you) care to) clarify|i('m| am) confused|i do( not|n't) (understand|get( it)?)( what you mean| what (that|this) means)?|why (do|did) you (say|think) (that|this))\?*$", self.user_message)
		
		if (meaning_match):
			#Pattern asking for clarification on previous response found
			
			#Split previous response into list of qords and shuffle them
			previous_words = (re.sub(r"([^a-z0-9 '\-])", '', self.CHELSEA_previous_response)).split(" ")
			random.shuffle(previous_words)
		
			for message in self.temp_message_keys:
		
				#Prevent duplicate response
				if (message == self.CHELSEA_previous_response):
					continue
		
				match_count = 0
				match_words = []
		
				for word in previous_words:
		
					try:
						
						#Ignore neutral words
						if (self.dictionary[word]['emotion'] == "temp neutral" or self.dictionary[word]['emotion'] == "permanent neutral"):
							continue
		
					except(KeyError):
						continue
		
					if (len(match_words) != 0):
		
						#Skip word if it is repeated
						repeated_word = False
						for word2 in match_words:
		
							if (word == word2):
								repeated_word = True
		
						if (repeated_word):
							continue
		
					if (message.find(word) != -1):
		
						#Add to count and list of match words
						match_count += 1
						match_words.append(word)
		
					#Keep going if only 1 match word found
					if (match_count < 2):
						continue		
		
					else:
		
						#Response found that is relevant to the previous response
						#This is very loose, response just contains words used in prevous response, may not actually give clarifiction
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Previous words meaning match found for: {" & ".join(match_words)}")
						self.CHELSEA_previous_response = self.botReply(message)
						response_made = True
						break
		
				if response_made:
					break
		
			if response_made:
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
	
	def check_topic_or_depth_match(self):
		
		#Check for match with current topic or depth match (Coin flip)
		
		response_made = False
		if ((not(len(self.topics.keys()) == 0) and (self.dictionary_count >= 2500 and self.response_count >= 1200 and random.randint(1, 3) == 1)) or (not(len(self.topics.keys()) == 0) and (self.dictionary_count >= 600 and self.dictionary_count < 2500 and self.response_count >= 350 and self.response_count < 1200 and random.randint(1, 4) == 1))):
			#Use 'dice rolls' to determine if topic or depth match used.
			#Also decided by how much is in CHELSEA's memory.
			#The purpose is to avoid CHELSEA from using this until CHELSEA has learned more, 
			# otherwise it actually can prevent CHELSEA from learning new responses

			if (len(self.depth_words) >= 2 and random.randint(1, 2) == 1):
				#Coin flip, topic or depth match
		
				#Depth match
				for message in self.temp_message_keys:
					#Loop through the messages in the message/response pairs
		
					depth_found = 0
					two_matched = False
					matched_words = []
					random.shuffle(self.depth_words)
		
					#Loop through the current depth words
					#Find if at least 2 are contained in the message
					for word in self.depth_words:
		
						if message.find(word) != -1:
		
							depth_found += 1
							matched_words.append(word)
		
						if (depth_found == 2):
		
							two_matched = True
							break
		
					if (not(two_matched)):
						#Didn't get at least 2 matches, move on to the next message
						continue
		
					else:
		
						#At least 2 depth words matched the message, use the message for the response
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Depth match found for: {" ".join(matched_words)}")
						self.CHELSEA_previous_response = self.botReply(message)
						response_made = True
						break
		
				if response_made:
					return True
		
			else:	
		
				#Topic match
				for message in self.temp_message_keys:
					#Loop through the messages in the message/response pairs

					topics_found = True
		
					#Loop through the current topic words
					#Find if 1 is contained in the message
					for topic in self.current_topics:
		
						if message.find(topic) == -1:
		
							topics_found = False
							break
		
					if (not(topics_found)):
						#Didn't find a match, move on to the next message
						continue
		
					else:
		
						#Matched a topic word to the message, use the message for the response
						self.Xchatlog.append(f"{self.bot_name} (Thinking): Topic match found.")
						self.CHELSEA_previous_response = self.botReply(random.choice(self.message_dict2[self.current_mood["mood"]][message]))
						response_made = True
						break
		
				if response_made:
					return True
		
		return False
	
	def use_imagination(self):
		
		#FLAG
		#Highly Experimental, often produces nonsense responses.
		#The goal was for CHELSEA to use this to produce responses that are not actually in CHELSEA's memory,
		# hence 'use imagination'.
		#Expand on this further later on
		#Need to find method for changing bigram and trigram emotions after changes to emotion in dictionary words, avoid searching through all if possible
		
		ngram_count = len(self.bigram_dictionary.keys()) + len(self.trigram_dictionary.keys())
		
		if ((ngram_count > 1000 and ngram_count < 25,000 and random.randint(1, 11) == 1) or (ngram_count > 30,000 and random.randint(1, 9) == 1)):
			#Use dice roll and amoun in memory to determine if using.
			#Reason for doing it this way is to prevent CHELSEA from missing learning opportunities, especially when CHELSEA's memory is just starting out.
			# Using this ends up skipping over CHELSEA's message/response learning logic.

			if (len(self.trigram_dictionary.keys()) > 0 and random.randint(1, 3) == 1):
				#Use trigrams 1/3 of the time

				td_keys = list(self.trigram_dictionary.keys())
				word = ""
				word_type = "topic"

				#If current topic(s), coin flip to see if using one of them		
				if len(self.current_topics) > 0 and random.randint(1, 2) == 1:
					word = random.choice(self.current_topics)
		
				#Elif use a depth word instead if there are any current ones
				elif len(self.depth_words) > 0:
					word = random.choice(self.depth_words)
					word_type = "depth"
		
				#If no topic or depth words, return from the method
				else:
					return False
		
				#Create a chain of matching trigrams starting with the topic or depth word as a base
				imagined_message = [word]
				next = word
				index = 0
				
				#Decide if chain of trigrams is going in forward or reverse
				forward_chain = random.choice([False, True])
		
				for n in range(random.randint(6, 8)):
					#Get 6-8 matches
		
					for k in range(index, len(td_keys)):
		
						if forward_chain:
							#Find the next matching trigram going forward
							m1 = re.search(re.compile(f"^{next} ([a-z'-]+) ([a-z'-]+)$"), td_keys[k])
		
						else:
							#Find the next matching trigram going in reverse
							m1 = re.search(re.compile(f"^([a-z'-]+) ([a-z'-]+) {next}$"), td_keys[k])
		
						index = k
		
						if m1:
		
							if forward_chain:
								#For forward
		
								trigram_emotions = f"{" ".join(self.trigram_dictionary[next + " " + m1.group(1) + " " + m1.group(2)]["emotions"])}"
		
								if n == 0:
		
									#First word in first match doesn't need to match mood
									if not(re.search(re.compile(f"(.*) ({self.current_mood["mood"]}|permanent neutral|temp neutral) ({self.current_mood["mood"]}|permanent neutral|temp neutral)"), trigram_emotions)):
										continue
		
								else:
		
									#All other words do need to match mood
									if not(re.search(re.compile(f"({self.current_mood["mood"]}|permanent neutral|temp neutral) ({self.current_mood["mood"]}|permanent neutral|temp neutral) ({self.current_mood["mood"]}|permanent neutral|temp neutral)"), trigram_emotions)):
										continue
		
								imagined_message.append(m1.group(1))
								imagined_message.append(m1.group(2))
								next = m1.group(2)
		
							else:
								#For reverse

								trigram_emotions = f"{" ".join(self.trigram_dictionary[m1.group(1) + " " + m1.group(2) + " " + next]["emotions"])}"
		
								if n == 0:
		
									#First word in first match doesn't need to match mood
									if not(re.search(re.compile(f"({self.current_mood["mood"]}|permanent neutral|temp neutral) ({self.current_mood["mood"]}|permanent neutral|temp neutral) (.*)"), trigram_emotions)):
										continue
		
								else:
		
									#All other words do need to match mood or be neutral
									if not(re.search(re.compile(f"({self.current_mood["mood"]}|permanent neutral|temp neutral) ({self.current_mood["mood"]}|permanent neutral|temp neutral) ({self.current_mood["mood"]}|permanent neutral|temp neutral)"), trigram_emotions)):
										continue
		
								imagined_message.insert(0, m1.group(2))
								imagined_message.insert(0, m1.group(1))
								next = m1.group(1)
		
							break
		
						else:
							continue

				#Get the direction type for output to the eXtended chatlog
				direction_type = "forward"
				if not(forward_chain):
					direction_type = "reverse"
		
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Trigram chain for '{self.current_mood["mood"]}' words in {direction_type} for {word_type} word '{word}' imagined.")
				
				#Give the trigram chain as the response
				self.CHELSEA_previous_response = self.botReply(" ".join(imagined_message))
				return True
		
			elif (len(self.bigram_dictionary.keys()) > 0):
				#Use bigrams 2/3 of the time

				bd_keys = list(self.bigram_dictionary.keys())
				word = ""
				word_type = "topic"
		
				if len(self.current_topics) > 0 and random.randint(1, 2) == 1:
					#Coin flip decided to use a topic word, if there are any
					word = random.choice(self.current_topics)
		
				elif len(self.depth_words) > 0:
					#If any depth words, use one
					word = random.choice(self.depth_words)
					word_type = "depth"
		
				else:
					#No topic or depth words, return from the method
					return False
		
				#Create a chain of matching bigrams starting with the topic or depth word as a base
				imagined_message = [word]
		
				next = word
				index = 0
				forward_chain = random.choice([False, True])
		
				for n in range(random.randint(6, 8)):
					#Get 6-8 matches
		
					for k in range(index, len(bd_keys)):
		
						if forward_chain:
							#Create the chain going forward
							m1 = re.search(re.compile(f"^{next} ([a-z'-]+)$"), bd_keys[k])
		
						else:
							#Create the chain going in reverse
							m1 = re.search(re.compile(f"^([a-z'-]+) {next}$"), bd_keys[k])
		
						index = k
		
						if m1:
		
							if forward_chain:
								#Bigram chain going forward
		
								bigram_emotions = f"{" ".join(self.bigram_dictionary[next + " " + m1.group(1)]["emotions"])}"
		
								if n == 0:
		
									#First word in first match doesn't need to match mood
									if not(re.search(re.compile(f"(.*) ({self.current_mood["mood"]}|permanent neutral|temp neutral)"), bigram_emotions)):
										continue
		
								else:
		
									#Both words need to match current mood or be neutral
									if not(re.search(re.compile(f"({self.current_mood["mood"]}|permanent neutral|temp neutral) ({self.current_mood["mood"]}|permanent neutral|temp neutral)"), bigram_emotions)):
										continue
		
								imagined_message.append(m1.group(1))
		
							else:
								#Bigram chain going in reverse
		
								bigram_emotions = f"{" ".join(self.bigram_dictionary[m1.group(1) + " " + next]["emotions"])}"
		
								if n == 0:
		
									#First word in first match doesn't need to match mood
									if not(re.search(re.compile(f"({self.current_mood["mood"]}|permanent neutral|temp neutral) (.*)"), bigram_emotions)):
										continue
		
								else:
		
									#Both words need to match current mood or be neutral
									if not(re.search(re.compile(f"({self.current_mood["mood"]}|permanent neutral|temp neutral) ({self.current_mood["mood"]}|permanent neutral|temp neutral)"), bigram_emotions)):
										continue
		
								imagined_message.insert(0, m1.group(1))
		
							next = m1.group(1)
							break
		
						else:
							continue

				#Get direction type to output to eXtended chatlog
				direction_type = "forward"
				if not(forward_chain):
					direction_type = "reverse"
		
				#Give the bigram chain as the response
				self.Xchatlog.append(f"{self.bot_name} (Thinking): Bigram chain for '{self.current_mood["mood"]}' words in {direction_type} for {word_type} word '{word}' imagined.")
				self.CHELSEA_previous_response = self.botReply(" ".join(imagined_message))
		
				return True
		
		#Dice roll for using bigrams/trigrams failed
		return False
	
	def check_single_term_match(self):
		
		#Check for single term match under current mood, ignore neutral words
		#Only activated when CHELSEA has learned enough, though this can easily be adjusted.
		#The goal for that was that using this prevents CHELSEA from activating the learning method,
		# so it should be avoided while CHELSEA barely knows anything.
		
		response_made = False
		if ((self.dictionary_count >= 4500 and self.response_count >= 2700 and random.randint(1, 3) == 1) or (self.dictionary_count >= 2000 and self.dictionary_count < 4500 and self.response_count >= 500 and self.response_count < 2700 and random.randint(1, 4) == 1)):
		
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
		
						if (len(temp_dictionary.keys()) == 0):
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
	
	def learn_new_response(self):
		
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
		
			if (random.randint(1, 2) == 1 and len(list(self.unanswered_questions["what"].keys())) > 0):
		
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
				if (random.randint(1, 2) == 1 and len(list(self.unanswered_questions["why is"].keys())) > 0):
		
					#why is
					self.temp_questions = list(self.unanswered_questions["why is"].keys())
		
					#Try to find a current topic relevant 'why is' question first
					if self.find_topic_in_questions("is"):
						return
		
					#Ask random 'why is' question
					self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked random why is question, waiting for valid answer.")
					self.CHELSEA_previous_response = self.botReply(random.choice(self.temp_questions))
					self.unanswered["why is"] = True
		
				elif (len(list(self.unanswered_questions["why are"].keys())) > 0):
		
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
			self.Xchatlog.append(f"{self.bot_name} (Thinking): Gave random response.")	
			self.CHELSEA_previous_response = self.botReply(random.choice(random.choice(list(self.message_dict2[self.current_mood["mood"]].values()))))

	def chat(self, sr, r, source):

		#All return statements cause the chat loop in 'chatbotCHELSEA.py' to continue, unless user reply is 'exit the chat'.
		#Otherwise it falls through to the next method.
		#A return from one of these methods is basically saying 'The user reply was handled with an appropriate response'.
		
		if self.get_user_reply(sr, r, source):

			#User spoke command, switch to text input mode
			if self.user_message == 'disable speech':
				self.speech_rec_enabled = False

			#User typed command, switch to speech recognition mode
			elif self.user_message == 'enable speech':
				self.speech_rec_enabled = True

			#If self.user_message == 'exit the chat', returning will end up exiting the chat and then output all memory
			#Else, chat loop will continue
			return
		
		if self.math_comprehension():
			return

		#Identity parts
		if self.ask_if_is():
			return
		if self.ask_if_user_is():
			return
		if self.tell_what_is():
			return
		if self.tell_what_user_is():
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
		self.get_bigrams()
		self.get_trigrams()
		self.get_topic_counts()
		self.determine_current_topics()
		self.add_to_previous_pairs()
		self.get_depth_words()
		self.get_popular_words()
		self.check_for_answer_what()
		if self.check_for_answer_why():
			return

		#Reponses
		if self.answer_whq_question():
			return
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
		if self.check_exact_message_match():
			return
		if self.check_partial_message_match():
			return
		if self.use_imagination():
			#FLAG
			return
		if self.check_topic_or_depth_match():
			return
		if self.check_single_term_match():
			return
		self.learn_new_response()
		self.give_random_or_question_response()

		return

