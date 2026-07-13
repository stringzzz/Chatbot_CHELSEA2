import re
import math

def CHELSEA_Math_Logic2(m1):

	word_to_symbol = { 
		'plus': '+',
		'added to': '+',
		'increased by': '+',
		'minus': '-',
		'subtracted by': '-',
		'decreased by': '-',
		'reduced by': '-',
		'multiplied by': '*',
		'times': '*',
		'divided by': '/' 
	}

	word_to_number = {
		'one': 1,
		'two': 2,
		'three': 3,
		'four': 4,
		'five': 5,
		'six': 6,
		'seven': 7,
		'eight': 8,
		'nine': 9,
		'ten': 10,
		'eleven': 11,
		'twelve': 12,
		'thirteen': 13,
		'fourteen': 14,
		'fifteen': 15,
		'sixteen': 16,
		'seventeen': 17,
		'eighteen': 18,
		'nineteen': 19,
		'twenty': 20,
		'thirty': 30,
		'forty': 40,
		'fifty': 50,
		'sixty': 60,
		'seventy': 70,
		'eighty': 80,
		'ninety': 90
	}

	message = m1.group(1)
	for word in word_to_symbol.keys():
		message = re.sub(word, word_to_symbol[word], message)
			
	if re.search(r"pow\((.*), (.*)\)", message):
		message = re.sub(r"(pow)", r"math.\1", message)
		
	if re.search(r"(log|sin|cos|tan)\((.*)\)", message):
		message = re.sub(r"(log|sin|cos|tan)", r"math.\1", message)

	match1 = True
	debug_count = 0
	while(match1):

		match1 = re.search(r"(?P<dashed_number>[a-zA-Z]+-[a-zA-Z]+)", message)

		if (match1):

			dashed_number = match1.group('dashed_number')
			
			if (dashed_number.find('-') != -1):

				for word in word_to_number:
					
					replaced_group = False 
					for word2 in word_to_number:
					
						if (word + '-' + word2 == dashed_number):
					
							message = message.replace(dashed_number, f"{word_to_number[word] + word_to_number[word2]}")
							replaced_group = True
							break
					
					if replaced_group:
						break
				
				if not replaced_group:
					break

	message = message.replace(' thousand', '000')
	message = message.replace(' hundred', '00')
		
	if re.search(r"( pi | e )", message):
		message = re.sub(r"( pi | e )", r" math.\1 ", message)
		
	if re.search(r"(\(-?\d+\.?\d*\)) *(math\.pi|math\.e)", message):
		message = re.sub(r"(\(-?\d+\.?\d*\)) *( math\.pi | math\.e )", r"\1 * \2", message)

	for word in word_to_number:
		message = message.replace(word, str(word_to_number[word]))
		
	####### Keep in case of problems					
	print("Debug1: " + message)
		
	try:
		test = eval(message)
		return (m1.group(1) + " equals " + str(test))
	except:
		return "Invalid expression!"	