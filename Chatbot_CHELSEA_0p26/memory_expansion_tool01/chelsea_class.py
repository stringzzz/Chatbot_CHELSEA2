#   chatbotCHELSEA, an AI chatbot with simulated emotions, math logic, and some self identity (chelsea class for expanding on memory by answering 'what is/are' questions)
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

# Chatbot CHELSEA: CHat Emotion Logic SEnse Automator (Class for Memory Expansion Tool)

import json
import re
import random
from datetime import datetime
import nltk
from nltk.corpus import wordnet
import inflect

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

		#See if speech recognition enabled or disabled
		self.speech_rec_enabled = speech_rec_enabled

		#QA_FLAG
		# Ensure the required phonetic dictionary is downloaded
		try:
			from nltk.corpus import cmudict
			self.pron_dict = cmudict.dict()
		except LookupError:
			nltk.download('cmudict')
			from nltk.corpus import cmudict
			self.pron_dict = cmudict.dict()

		# A set of all ARPAbet vowel phonemes (they always end with a digit 0, 1, or 2)
		self.VOWEL_PHONEMES = {'AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'EH', 'ER', 'EY', 'IH', 'IY', 'OW', 'OY', 'UH', 'UW'}


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
		self.Xchatlog.append(f"{self.bot_name} (Thinking):  seems to be {self.reply_mood["mood"]}")

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
		#self.speak_response(botResponse)
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

	def form_what_isare_question(self, question):
		
		self.Xchatlog.append(f"{self.bot_name} (Thinking): Asked '{question}' in previous user reply, waiting for valid answer.")
		self.CHELSEA_previous_response = self.botReply(f"{question}")
		self.unanswered["what"] = True


##################################################################################################
## The following code is outside of the copyright of this program up until 'END_EXTERNAL_CODE' ###
##################### It was actually written mostly by Google's Gemini AI #######################
##################################################################################################

	def get_article(self, word_or_definition):

		#QA_FLAG

		# Tag the word to find its Part of Speech
		tokens = nltk.word_tokenize(word_or_definition)
		tag = nltk.pos_tag(tokens)[0][1]

		# If the tag starts with 'VB', it's a verb
		if tag.startswith('VB'):
			if not tag.startswith("VBG"):
				return "to "
			else:
				return ""
			
		elif tag.startswith('NN'):
			
			# 1. Isolate the first word of the definition
			words = nltk.word_tokenize(word_or_definition.lower())
			if not words:
				return "a "
			
			first_word = words[0]

			# 2. Check the phonetic dictionary for the first word
			if first_word in self.pron_dict:
				# Get the first phoneme of the first pronunciation
				# (e.g., 'hour' -> ['AO1', 'ER0'], 'AO1' is the first phoneme)
				phonemes = self.pron_dict[first_word][0]
				first_sound = re.sub(r'\d', '', phonemes[0]) # Remove the stress digit (e.g., AO1 -> AO)
				
				if first_sound in self.VOWEL_PHONEMES:
					return "an "
				else:
					return "a "
				
		return ""

	def get_definition(self, word):

		#QA_FLAG

		p = inflect.engine()

		syns = wordnet.synsets(word)
		if syns:
			# Returns the first definition found

			# 2. Check Singular/Plural
			# singular_noun() returns False if it's already singular
			is_plural = p.singular_noun(word)
			
			is_are = "are" if is_plural else "is"

			cut_definition = re.sub(r'(:|;).*', '', syns[0].definition())

			article1 = self.get_article(word)
			article2 = self.get_article(cut_definition)

			if is_are == 'are':
				article1 = ''

			if cut_definition.startswith('the') or cut_definition.startswith('a'):
				article2 = ''

			return f"{article1}{word} {is_are} {article2}{cut_definition}"
		else:
			return False
		
##################################################################################################
################################### END_EXTERNAL_CODE ############################################
##################################################################################################		

	def chat(self, question):

		self.form_what_isare_question(question)

		print(question)

		#Get the word being asked about
		m1 = re.match(r'.* is/are (.*)[?!.]', question)
		word = m1.group(1)

		print(word)

		#Get the definition of the word, if it exists
		#If not, return so it moves on to the next question
		temp = self.get_definition(word)
		if temp:
			self.user_message = temp.lower()
		else:
			return
		
		self.Xchatlog.append(f"Answer: {self.user_message}")
		print(self.user_message)
		print("")

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
		if self.ask_why_is():
			return
		
		self.learn_new_response()

		return

