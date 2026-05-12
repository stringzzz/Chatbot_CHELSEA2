#   chatbotCHELSEA, an AI chatbot with simulated emotions, math logic, and some self identity (Main script)
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

import os
import sys
import speech_recognition as sr #type: ignore
from chelsea_class import chelsea #type: ignore

try:

	#Determine if speech recognition enabled or disabled from command line argument option
	#Use argument 'sr' to enable speech recognition else use text mode instead
	speech_rec_enabled = False
	if len(sys.argv) > 1 and sys.argv[1] == 'sr':
		speech_rec_enabled = True

	#Create chelsea object (CHELSEA is NOT an object! >:/)
	chatbot_chelsea =  chelsea("CHELSEA", speech_rec_enabled) #Input desired name in place of "CHELSEA"

	# Initialize recognizer
	r = sr.Recognizer()

	# Optional: Adjust for ambient noise to prevent false starts
	# This listens for 1 second to determine the ambient noise level
	with sr.Microphone() as source:
		
		# Customize the silence threshold (seconds of silence to end recording)
		r.pause_threshold = 1.5 # Default is 0.8

		os.system("clear")

		#Input memory
		print("Inputting memory...")
		chatbot_chelsea.input_memory()
		print("Memory input complete!\n")

		chatbot_chelsea.input_user_self()
		chatbot_chelsea.initial_greeting()

		#Chat loop
		while chatbot_chelsea.user_message != "exit the chat":
			chatbot_chelsea.chat(sr, r, source)

		#Output memory
		print("\nOutputting memory...")
		chatbot_chelsea.output_memory()
		chatbot_chelsea.output_user_self()
		print("Memory output complete.\n")

finally:
	chatbot_chelsea.temp_piper_output_file.close()
	chatbot_chelsea.close_tts_subprocess()