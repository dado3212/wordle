from wordle import *
import random

# This is a slight improvement over play_dumb, because it keeps track of the
# valid guesses AND the valid answers. If it's eliminated all but one of the
# valid answers, it just guesses that. We're still allowing guessing things that
# aren't valid answers, but are valid guesses b/c in later iterations there may
# be more information from these versions.
#
# Played 10000 games in 61.26 seconds and found the word in an average of 
# 5.38 guesses, though the worst case took 15 guesses.
def play() -> int:
    goal_word = random.choice(valid_answers)

    guesses = 0
    possible_words = valid_words
    possible_answers = valid_answers
    while (True):
        guesses += 1
        if (len(possible_answers) == 1):
            guess = possible_answers[0]
        else:
            guess = random.choice(possible_words)
        scored_word = score_word(goal_word, guess)
        possible_words = [word for word in possible_words if matches_scored_word(word, scored_word) and word != guess]
        possible_answers = [word for word in possible_answers if matches_scored_word(word, scored_word) and word != guess]
        if (guess == goal_word):
            break
    return guesses

evaluate_method(10000, play)