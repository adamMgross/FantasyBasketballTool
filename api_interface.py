import urllib2
import json

# unpacks the JSON data from a given url and returns it as a dict
def fetch(url):
    #req = url_parser.open(url)
    #json_data = req.read()
    #return json.loads(json_data)
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'})
    response = urllib2.urlopen(req)
    json_data = response.read()
    return json.loads(json_data)

# unpacks the JSON data from a given url with the given access code
def fetch_with_access_code(url, access_code):
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'})
    req.add_header("Authorization", "Bearer " + access_code)
    response = urllib2.urlopen(req)
    json_data = response.read()
    return json.loads(json_data)
