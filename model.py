import math
import re
import json
from stopwords import stopwords


def extract_tokens(str):
    return set(filter(lambda w: w and w not in stopwords,
                      [w.lower() for w in re.split('[^\w0-9\.]', str)]))


class DuplicateStoryError(Exception):
    pass


class Model:
    def load_from(self, filename):
        try:
            with open(filename) as fp:
                obj = json.load(fp)
                self.words = obj['words']
                self.num_stories = int(obj['num_stories'])
                self.num_interesting = int(obj['num_interesting'])
                self.ids_seen = obj['ids_seen']
            self._loaded = True
            return True
        except IOError:
            return False

    def save_as(self, filename):
        with open(filename, 'w') as fp:
            obj = {
                'words': self.words,
                'num_stories': self.num_stories,
                'num_interesting': self.num_interesting,
                'ids_seen': self.ids_seen}
            json.dump(obj, fp)

    def __init__(self, filename=None):
        self._loaded = False
        if filename is not None:
            self.load_from(filename)
        if not self._loaded:
            # Set defaults for empty model
            self.words = {}
            self.num_stories = self.num_interesting = 0
            self.ids_seen = {}

    def _mark_id(self, new_id):
        """ Mark a story ID as seen, so it won't be double counted. """
        self.ids_seen[new_id] = 1

    def seen_id(self, id_to_check):
        return id_to_check in self.ids_seen

    def add_story(self, title, story_id, interesting):
        if self.seen_id(story_id):
            raise DuplicateStoryError("Tried to resubmit story: " + story_id)

        self._mark_id(story_id)
        self.num_stories += 1
        self.num_interesting += int(interesting)

        # update word counts for each unique word in title
        for word in extract_tokens(title):
            if word in stopwords:
                continue

            story_count = 1
            interesting_count = int(interesting)

            if word in self.words:  # word already has a count
                story_count += self.words[word][0]
                interesting_count += self.words[word][1]

            self.words[word] = (story_count, interesting_count)

    def _posterior_for(self, word):
        if word not in self.words or self.words[word][0] < 1:
            return None
        return self.words[word][1] / float(self.words[word][0])

    def predict_story(self, title):
        if self.num_stories < 10:
            return None  # not enough info to predict

        interesting_ratio = self.num_interesting / float(self.num_stories)

        words = extract_tokens(title)
        probs = filter(None, [self._posterior_for(word) for word in words])
        probs.sort(None, lambda p: abs(interesting_ratio - p))
        probs = probs[:12]
        if len(probs) < 2:
            return None  # not enough info to predict

        def make_nonzero(p):
            return 1 / float(self.num_stories + 1) if p == 0 else p

        sum_of_logs = sum([math.log(make_nonzero(p))
                           - math.log(make_nonzero(1 - p)) for p in probs])
        return 1.0 / (math.exp(sum_of_logs) + 1)
