import constants
import oprix
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def search(query):
    img_results = oprix.search(query)
    maxmatch = 0
    for key in constants.EMISSIONS:
        if fuzz.ratio(img_results['brand'], key) > maxmatch:
            maxmatch = fuzz.ratio(img_results['brand'], key)
            match = key

    brand = match

    maxmatch = 0
    for key in constants.EMISSIONS[match]['cars'][0]:
        if fuzz.ratio(img_results['model'], key) > maxmatch:
            maxmatch = fuzz.ratio(img_results['model'], key)
            match = key

    ans = constants.EMISSIONS[brand]['cars'][0][match]
    ans['name'] = (img_results['brand']+ '-' + img_results['model'])
    return ans 

        

