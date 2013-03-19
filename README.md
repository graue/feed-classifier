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

I don't think it actually works yet.
My data size is small, but even so, the probability values
seem decidedly wonky.
