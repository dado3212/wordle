
from typing import List, Tuple, Callable, Dict

Word = Tuple[str, Dict[str, bool]]
ScoredWord = Dict[int, List[Tuple[str, int]]]

def score_word(goal_word: Word, guess_word: Word) -> ScoredWord:
    answers: Dict[int, List[Tuple[str, int]]] = {2: [], 1: [], 0: []}
    for i in range(0, len(guess_word[0])):
        guessed_letter = guess_word[0][i]
        if guessed_letter == goal_word[0][i]:
            answers[2].append((guessed_letter, i))
        elif guessed_letter in goal_word[1]:
            answers[1].append((guessed_letter, i))
        else:
            answers[0].append((guessed_letter, i))
    return answers

def matches_scored_word(word: Word, scored_word: ScoredWord) -> bool:
    # Letter must not exist
    for l in scored_word[0]:
        if l[0] in word[1]:
            return False
    # Letter must exist
    for l in scored_word[1]:
        if l[0] not in word[1]:
            return False
    # Letter must exist in position
    for l in scored_word[2]:
        if word[0][l[1]] != l[0]:
            return False
    return True

def evaluate_method(total_games_to_play: int, method: Callable[[], int]):
    import time

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
            round(time.time() - start, 2),
            round(float(total_guesses) / total_games_to_play, 2),
            max
        )
    )

import pickle
with open('valid_words', 'rb') as fp:
    valid_words: List[Word] = pickle.load(fp)

with open('valid_answers', 'rb') as fp:
    valid_answers: List[Word] = pickle.load(fp)