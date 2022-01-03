from wordle import *
import random

# This is the dumb way to play
# Pick any word to guess
# Based on the results, filter out what isn't possible
# Keep guessing until you get the word
#
# We assume that we don't know which are valid answers for now
# Played 10000 games in 99.4 seconds and found the word in an average of 
# 5.8204 guesses, though the worst case took 15 guesses.
def play_dumb() -> int:
    goal_word = random.choice(valid_answers)

    guesses = 0
    possible_words = valid_words
    while (True):
        guesses += 1
        guess = random.choice(possible_words)
        scored_word = score_word(goal_word, guess)
        possible_words = [word for word in possible_words if matches_scored_word(word, scored_word) and word != guess]
        if (guess == goal_word):
            break
    return guesses

evaluate_method(10000, play_dumb)