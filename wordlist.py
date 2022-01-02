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
    for i in range(0, len(scored_word)):
        letter = scored_word[i]
        if letter[1] == 2 and letter[0] != word[i]:
            return False
        if letter[1] == 1 and letter[0] not in word:
            return False
    return True

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
valid_words = valid_words + valid_answers
valid_words.sort()

print("Downloaded {0} answers out of {1} total valid words".format(len(valid_answers), len(valid_words)))

# This is the dumb way to play
# Pick any word to guess
# Based on the results, filter out what isn't possible
# Keep guessing until you get the word
#
# We assume that we don't know which are valid answers for now

goal_word = random.choice(valid_answers)
print("The goal word is: '{0}'".format(goal_word))

guesses = 0
possible_words = valid_words
while (True):
    guesses += 1
    guess = random.choice(possible_words)
    scored_word = score_word(goal_word, guess)
    possible_words = [word for word in valid_words if matches_scored_word(word, scored_word)]
    print("Guess #{0} is '{1}', reducing down to {2} still valid words.".format(guesses, guess, len(possible_words)))
    if (guess == goal_word):
        break
