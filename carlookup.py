import constants
import oprix
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def search(query):
    try:
        img_results = oprix.search(query)
    except Exception as e:
        print(e)
        return '', {'average' : '118.1 g/km', 'range' : '118.1 g/km'}
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

    car = img_results['model']

    try:
        return (img_results['brand']+ '-' + car), constants.EMISSIONS[brand]['cars'][0][match]
    except:
        '', {'average' : '118.1 g/km', 'range' : '118.1 g/km'}

