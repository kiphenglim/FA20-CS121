""" Calls the Google Custom Search Site Restricted JSON API. A secret
file because it contains our application's secret key and also our API
key. """
import requests

### Google API helper ###
def get_images(query):
    """ Google API helper. Given a string query, returns a Google image search for that query. """
    results = []
    req = requests.get('https://www.googleapis.com/customsearch/v1?'+
                           'key=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA&cx=00000000000000000&' +
                           'searchType=image&num=3&q='+query).json()
    
    if 'searchInformation' in req and req["searchInformation"]["totalResults"] != "0":
        for img in req["items"]:
            results.append(img["link"])
            
    return results
                                                
