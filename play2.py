from wordle import *
import random

# This is play1, but instead of choosing a random possible word, it ranks and
# chooses the best one. From now on, each of the play iterations should just
# be improving the scoring function for how to choose the best guess.
#
# Played 10000 games in 104.2 seconds and found the word in an average of 
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
            # Rank these choices by how many it reduces the possible words set by
            best_guesses = []
            best_guess_score = 1000
            for possible_guess in possible_words:
                # get every possible response
                score = 0.0
                for possible_goal in possible_answers:
                    scored_word = score_word(possible_goal, possible_guess)
                    new_possible_answers = [word for word in possible_answers if matches_scored_word(word, scored_word)]
                    score += len(new_possible_answers)
                score = score / len(possible_answers)
                if score < best_guess_score:
                    best_guess_score = score
                    best_guesses = [possible_guess]
                    print(best_guesses)
                    print(best_guess_score)
                elif score == best_guess_score:
                    best_guesses.append(possible_guess)
                    print(best_guesses)
                    print(best_guess_score)
            guess = random.choice(best_guesses)
            print("Guessing {0} from a set of {1} possible best guesses (scored {2})".format(guess, len(best_guesses), best_guess_score))
        scored_word = score_word(goal_word, guess)
        possible_words = [word for word in possible_words if matches_scored_word(word, scored_word) and word != guess]
        possible_answers = [word for word in possible_answers if matches_scored_word(word, scored_word) and word != guess]
        if (guess == goal_word):
            break
    return guesses

evaluate_method(1, play)