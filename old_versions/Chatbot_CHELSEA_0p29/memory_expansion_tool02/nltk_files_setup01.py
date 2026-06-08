import nltk

# Ensure the required phonetic dictionary is downloaded
try:
	from nltk.corpus import cmudict
	self.pron_dict = cmudict.dict()
except LookupError:
	nltk.download('cmudict')
	from nltk.corpus import cmudict
	self.pron_dict = cmudict.dict()

# One-time download
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('wordnet')