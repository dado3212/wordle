
import random, pickle, time
from typing import List, Tuple, Callable

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
        if letter[1] == 0 and letter[0] in word:
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

def evaluate_method(total_games_to_play: int, method: Callable[[], int]):
    total_guesses = 0
    max = 0
    start = time.time()
    for _ in range(0, total_games_to_play):
        guesses = method()
        if guesses > max:
            max = guesses
        total_guesses += guesses

    print(
        ("Played {0} games in {1} seconds and found the word in an average of "+
        "{2} guesses, though the worst case took {3} guesses.").format(
            total_games_to_play,
            round(time.time() - start, 1),
            round(float(total_guesses) / total_games_to_play, 2),
            max
        )
    )

evaluate_method(10000, play_dumb)