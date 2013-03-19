import feedparser
from model import Model

FEED_URL = 'http://feeds.feedburner.com/newsyc20?format=xml'
MODEL_FILE = 'model.json'

model = Model(MODEL_FILE)
d = feedparser.parse(FEED_URL)

for story in [entry for entry in d.entries if not model.seen_id(entry.id)]:
    print story.title
    prediction = model.predict_story(story.title)

    action = 'x'
    while action not in ['y', 'n', 's', 'q']:
        if action == 'h' or action == '?':
            print ""
            print "y: yes, story is interesting"
            print "n: no, story is boring"
            print "s: skip classifying this story"
            print "q: quit"
            print "h: display help"
        action = raw_input("interesting? [ynsqh] ")

    if action == 'q':
        break

    if action == 's':
        continue

    interesting = (action == 'y')
    model.add_story(story.title, story.id, interesting)
    model.save_as(MODEL_FILE)

    if prediction is not None:
        print ("Cool. My predicted chance you would like this article was " +
               str(prediction))
