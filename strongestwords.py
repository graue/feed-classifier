import json
import math

# This script shows the words that most strongly predict an interesting
# story, and the words that most strongly predict a boring one.

with open('model.json') as fp:
    obj = json.load(fp)

MIN_OCCUR = 3

word_counts = obj['words']
words = filter(lambda w: word_counts[w][0] >= MIN_OCCUR, word_counts.keys())
words.sort(None, lambda w: word_counts[w][1] / float(word_counts[w][0]), True)

most_pos = int(min(5, math.ceil(len(words) / 2.0)))
most_neg = int(min(5, math.floor(len(words) / 2.0)))
print "most_pos={0}, most_neg={1}".format(most_pos,most_neg)

print "strongest positive words (with at least {0} occurrences):".format(
        MIN_OCCUR)
for w in words[:most_pos]:
    print "{0} {1}".format(word_counts[w][1] / float(word_counts[w][0]), w)

print "\nstrongest negative words (with at least {0} occurrences):".format(
        MIN_OCCUR)
for w in words[-most_neg:]:
    print "{0} {1}".format(word_counts[w][1] / float(word_counts[w][0]), w)
