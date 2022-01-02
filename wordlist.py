import requests, re, random
from typing import List, Tuple

ScoredWord = List[Tuple[str, int]]

def score_word(goal_word: str, guess_word: str) -> ScoredWord:
    answers: List[Tuple[str, int]] = []
    for i in range(0, len(guess_word)):
        guessed_letter = guess_word[i]
        if guessed_letter == goal_word[i]:
            answers.append((guessed_letter, 2))
        elif guessed_letter in goal_word:
            answers.append((guessed_letter, 1))
        else:
            answers.append((guessed_letter, 0))
    return answers

def matches_scored_word(word: str, scored_word: ScoredWord) -> bool:
    for letter in scored_word:
        if (letter[1]) == 't':
            return True
    return False

def filter_word_list(word_list: List[str], scored_word: ScoredWord) -> List[str]:
    # For each word, check if it matches
    return word_list

# This generates the potential wordlists, both for the known Wordle list, and
# a more broader set of 5 letter words

base_wordle_url = 'https://www.powerlanguage.co.uk/wordle/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
s = requests.Session() 
r = s.get(base_wordle_url, allow_redirects=True, headers=headers)

# Extract the javascript file
script_key = re.search('<script src="(main..*)">', r.text, re.IGNORECASE)
assert script_key is not None
script_key = script_key.group(1)
script_url = base_wordle_url + script_key

script = s.get(script_url, allow_redirects=True, headers=headers)

valid_answers = re.search(r'var Aa=\[(.*?)\]', script.text)
assert valid_answers is not None
valid_answers = valid_answers.group(1).split(',')
valid_answers = [x.strip('"') for x in valid_answers]
valid_words = re.search(r'La=\[(.*?)\]', script.text)
assert valid_words is not None
valid_words = valid_words.group(1).split(',')
valid_words = [x.strip('"') for x in valid_words]

print("Downloaded {0} answers out of {1} total valid words".format(len(valid_answers), len(valid_words)))

# This is the dumb way to play
# Pick any word to guess
# Based on the results, filter out what isn't possible
# Keep guessing until you get the word
#
# We assume that we don't know which are valid answers for now

goal_word = random.choice(valid_answers)

first_guess = random.choice(valid_words)
print("The goal word is: '{0}'".format(goal_word))
print("Guessing '{0}'".format(first_guess))
print(score_word(goal_word, first_guess))
