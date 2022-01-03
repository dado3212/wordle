
import random, pickle
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

with open('valid_words', 'rb') as fp:
    valid_words = pickle.load(fp)

with open('valid_answers', 'rb') as fp:
    valid_answers = pickle.load(fp)

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
