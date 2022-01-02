import requests, re, random

# This generates the potential wordlists, both for the known Wordle list, and
# a more broader set of 5 letter words

base_wordle_url = 'https://www.powerlanguage.co.uk/wordle/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
s = requests.Session() 
r = s.get(base_wordle_url, allow_redirects=True, headers=headers)

# Extract the javascript file
script_key = re.search('<script src="(main\..*)">', r.text, re.IGNORECASE).group(1)
script_url = base_wordle_url + script_key

script = s.get(script_url, allow_redirects=True, headers=headers)

valid_answers = re.search('var Aa=\[(.*?)\]', script.text).group(1).split(',')
valid_answers = [x.strip('"') for x in valid_answers]
valid_words = re.search('La=\[(.*?)\]', script.text).group(1).split(',')
valid_words = [x.strip('"') for x in valid_words]

print("Downloaded {0} answers out of {1} total valid words and selected '{2}'".format(len(valid_answers), len(valid_words), random.choice(valid_answers)))
