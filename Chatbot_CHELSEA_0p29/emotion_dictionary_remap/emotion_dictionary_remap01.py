#pip3 install nrclex
#python -m textblob.download_corpora

#Final results: 
# Words altered: 1050 | Neutral words: 222 | Unchanged words: 9450 / 10722
# Refer to 'changed_words.txt' to see all of the words actually affected
# 'changed_words_to_lookup.txt' to see the actual values in the dictionary

import json
from nrclex import NRCLex

dictionary = {}
#Load the dictionary of words with ties to emotions
with open(f"dictionary.json", 'r') as dictionary_file:
	dictionary = json.load(dictionary_file)

text_object = NRCLex()

total_words = len(dictionary)
words_altered = 0
neutral_words = 0
unchanged_words = 0

changed_words = []

for word in list(dictionary.keys()):

	print(f"Words altered: {words_altered} | Neutral words: {neutral_words} | Unchanged words: {unchanged_words} / {total_words}")

	text_object.load_token_list([str(word)])
	frequencies = text_object.affect_frequencies

	if dictionary[word]['emotion'] == 'permanent neutral' or dictionary[word]['emotion'] == 'temp neutral':
		
		neutral_words += 1
		continue
	
	if frequencies['joy'] == 0.0 and frequencies['anger'] == 0.0 and frequencies['sadness'] == 0.0 and frequencies['fear'] == 0.0:
		
		unchanged_words += 1
		continue

	# 1. Reset all targets to 0 so we can rebuild them accurately
	dictionary[word]["happy"] = 0
	dictionary[word]["angry"] = 0
	dictionary[word]["sad"] = 0
	dictionary[word]["afraid"] = 0

	# 2. Proportionally distribute the 100 points based on the lexicon ratios
	if frequencies.get('joy', 0) > 0:
		dictionary[word]["happy"] = int(100 * frequencies['joy'])

	if frequencies.get('anger', 0) > 0:
		dictionary[word]["angry"] = int(100 * frequencies['anger'])		

	if frequencies.get('sadness', 0) > 0:
		dictionary[word]["sad"] = int(100 * frequencies['sadness'])

	if frequencies.get('fear', 0) > 0:
		dictionary[word]["afraid"] = int(100 * frequencies['fear'])

	# 3. Finally, set the dominant tag based on whichever value ended up highest

	# (This preserves your existing 'emotion' string flag)
	current_weights = {
		'happy': dictionary[word]["happy"], 
		'angry': dictionary[word]["angry"], 		
		'sad': dictionary[word]["sad"], 
		'afraid': dictionary[word]["afraid"]
	}
	dictionary[word]["emotion"] = max(current_weights, key=current_weights.get)

	words_altered += 1

	changed_words.append(word)

print(f"Words altered: {words_altered} | Neutral words: {neutral_words} | Unchanged words: {unchanged_words} / {total_words}")

with open(f"dictionary2.json", 'w') as dictionary_file:
	json.dump(dictionary, dictionary_file, indent=4)

with open(f"changed_words.txt", 'w') as words_file:
	words_file.write("\n".join(changed_words))	