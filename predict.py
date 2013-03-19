import feedparser
from model import Model

FEED_URL = 'http://feeds.feedburner.com/newsyc20?format=xml'
MODEL_FILE = 'model.json'

model = Model(MODEL_FILE)
d = feedparser.parse(FEED_URL)

predictions = [(s, model.predict_story(s.title)) for s in d.entries]
predictions = filter(lambda s: s[1] is not None, predictions)
predictions.sort(key=lambda s: s[1], reverse=True)

print "You'll probably like:\n"
for title in [s[0].title for s in predictions[:5]]:
    print u"{0} (p={1})".format(title, model.predict_story(title))

print "\nYou probably won't like:\n"
for title in [s[0].title for s in predictions[-5:]]:
    print u"{0} (p={1})".format(title, model.predict_story(title))
