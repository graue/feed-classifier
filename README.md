# Feed Classifier

**Work in Progress**

This code implements a naive Bayesian classifier
to help you find interesting stories from an RSS feed.
(Currently, the Hacker News 20-point stories feed is hardcoded.)

To train the classifier, run

    python train.py

After training, you can get predictions on most/least
interesting stories by running

    python predict.py

My data size is small, so it's not possible to see how well
this works yet. You probably need to train it a lot.
