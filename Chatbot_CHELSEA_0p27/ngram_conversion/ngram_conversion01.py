import json
import os

bigrams1 = {}

#Load the dictionary of bigrams (2 word groups)
with open(f"bigramDictionary.json", 'r') as bigram_dictionary_file:
	bigrams1 = json.load(bigram_dictionary_file)

trigrams1 = {}

#Load the dictionary of trigrams (3 word groups)
with open("trigramDictionary.json", 'r') as trigram_dictionary_file:
	trigrams1 = json.load(trigram_dictionary_file)

bigrams2 = {}
reverse_bigrams2 = {}

bigram_count = 1
max_bigrams = len(bigrams1.keys())

for bigram in bigrams1.keys():
	
	os.system("clear")
	print(f"bigrams: {bigram_count} / {max_bigrams}")
	bigram_count += 1

	words = bigram.split(" ")
	
	if not words[0] in bigrams2:
		bigrams2[words[0]] = {}
	bigrams2[words[0]][words[1]] = bigrams1[bigram]["seen"]
	
	if not words[1] in reverse_bigrams2:
		reverse_bigrams2[words[1]] = {}
	reverse_bigrams2[words[1]][words[0]] = bigrams1[bigram]["seen"]
	
trigrams2 = {}
reverse_trigrams2 = {}

trigram_count = 1
max_trigrams = len(trigrams1.keys())

for trigram in trigrams1.keys():

	os.system("clear")
	print(f"trigrams: {trigram_count} / {max_trigrams}")
	trigram_count += 1

	words = trigram.split(" ")
	
	if not (words[0], words[1]) in trigrams2:
		trigrams2[f"{words[0]} {words[1]}"] = {}
	trigrams2[f"{words[0]} {words[1]}"][words[2]] = trigrams1[trigram]["seen"]

	if not (words[1], words[2]) in reverse_trigrams2:
		reverse_trigrams2[f"{words[1]} {words[2]}"] = {}
	reverse_trigrams2[f"{words[1]} {words[2]}"][words[0]] = trigrams1[trigram]["seen"]
	
with open(f"bigramDictionary2.json", 'w') as bigram_dictionary_file:
	json.dump(bigrams2, bigram_dictionary_file, indent=4)
	  
with open(f"reverseBigramDictionary2.json", 'w') as bigram_dictionary_file:
	json.dump(reverse_bigrams2, bigram_dictionary_file, indent=4)  

with open(f"trigramDictionary2.json", 'w') as trigram_dictionary_file:
	json.dump(trigrams2, trigram_dictionary_file, indent=4)
	  
with open(f"reverseTrigramDictionary2.json", 'w') as trigram_dictionary_file:
	json.dump(reverse_trigrams2, trigram_dictionary_file, indent=4)