import constants 
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def match(query):
	maxmatch = 0
	for key in constants.EMISSIONS:
		if fuzz.ratio(query, key) > maxmatch:
			maxmatch = fuzz.ratio(query, key)
			match = key


	return constants.EMISSIONS[match]



print(match("maruti-suzuki"))


