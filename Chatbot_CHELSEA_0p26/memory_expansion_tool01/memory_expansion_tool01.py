#   chatbotCHELSEA, an AI chatbot with simulated emotions, math logic, and some self identity (Main script for expanding on memory by answering 'what is/are' questions)
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

from chelsea_class import chelsea #type: ignore


#Create chelsea object (CHELSEA is NOT an object! >:/)
chatbot_chelsea =  chelsea("CHELSEA", False) #Input desired name in place of "CHELSEA"

#Input memory
print("Inputting memory...")
chatbot_chelsea.input_memory()
print("Memory input complete!\n")

#Q/A loop
LOOP_MAX = 10
TOTAL_QUESTIONS = 1
for loop in range(0, LOOP_MAX):

	question_list = list(chatbot_chelsea.unanswered_questions['what'].keys())
	for num in range(0, len(question_list)):

		print(f"Loop: {loop + 1} / {LOOP_MAX} Question: {num + 1} / {len(question_list)} Total Questions: {TOTAL_QUESTIONS}")
		TOTAL_QUESTIONS += 1

		chatbot_chelsea.chat(question_list[num])

#Output memory
print("\nOutputting memory...")
chatbot_chelsea.output_memory()
print("Memory output complete.\n")
