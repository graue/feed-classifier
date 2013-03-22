import sys
import feedparser
from model import Model

# Can be a file or URL
FEED_SOURCE = ('http://feeds.feedburner.com/newsyc20?format=xml'
               if len(sys.argv) < 2 else sys.argv[1])

MODEL_FILE = 'model.json'

model = Model(MODEL_FILE)
d = feedparser.parse(FEED_SOURCE)

predictions = [(s, model.predict_story(s.title)) for s in d.entries
                  if not model.seen_id(s.id)]
predictions = filter(lambda s: s[1] is not None, predictions)
predictions.sort(key=lambda s: s[1], reverse=True)

print "You'll probably like:\n"
for story, p in predictions[:5]:
    print u"{0} (p={1})".format(story.title, p)

print "\nYou probably won't like:\n"
for story, p in predictions[-5:]:
    print u"{0} (p={1})".format(story.title, p)
