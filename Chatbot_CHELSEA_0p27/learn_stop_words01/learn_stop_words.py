import nltk
from nltk.corpus import stopwords

# Ensure the dataset is downloaded (only needs to run once)
#nltk.download('stopwords')

# Get the list of English stop words
nltk_stop_words = set(stopwords.words('english'))

# Quick sanity check: it will contain strings like 'for', 'the', 'with', 'to'
print(f"Loaded {len(nltk_stop_words)} stop words.")

import json 

#Load the dictionary of words with ties to emotions
with open(f"dictionary.json", 'r') as dictionary_file:
	dictionary = json.load(dictionary_file)

words_relearned = 0
words_newly_learned = 0
for word in nltk_stop_words:
	if word in dictionary:
		# Update your tag to mark it as a stop word / permanent neutral
		if dictionary[word]["emotion"] != "permanent neutral":
			dictionary[word]["emotion"] = "permanent neutral"
			words_relearned += 1

	else:
		# If the word isn't in your memory yet, you can pre-seed it
		dictionary[word] = {
			"happy": 0,
			"angry": 0,
			"sad": 0,
			"afraid": 0,
			"emotion": "permanent neutral",
			"seen": 0,
			"associated": {}
		}
		words_newly_learned += 1

with open(f"dictionary.json", 'w') as dictionary_file:
	json.dump(dictionary, dictionary_file, indent=4)

print(f"Words Relearned: {words_relearned}, Words Newly Learned: {words_newly_learned}")

