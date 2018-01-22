import constants
import oprix
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def search(query):
    try:
        img_results = oprix.search(query)
    except:
        return None
    maxmatch = 0
    for key in constants.EMISSIONS:
        if fuzz.ratio(img_results['brand'], key) > maxmatch:
            maxmatch = fuzz.ratio(img_results['brand'], key)
            match = key

    brand = match

    maxmatch = 0
    for key in constants.EMISSIONS[match]['cars']:
        if fuzz.ratio(img_results['model'], key) > maxmatch:
            maxmatch = fuzz.ratio(img_results['model'], key)
            match = key

    car = match

    return constants.EMISSIONS[brand]['cars'][car]


print(search("http://d1arsn5g9mfrlq.cloudfront.net/sites/default/files/resize/remote/b16f3f72fbbe9aac21e8723dd85d2a32-720x471.jpg"))
