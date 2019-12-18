# Runs every 4 hours for Program

from sqlMethods import *
from twitter_methods import *
from gensim import utils
from gensim.models.doc2vec import TaggedDocument, LabeledSentence
from gensim.models import Doc2Vec
import numpy
from nltk.tokenize import word_tokenize
from sklearn.linear_model import LogisticRegression


def process(model, s):
    s_vector = model.infer_vector(word_tokenize(s))
    new_s = s_vector.reshape(1, -1)
    return new_s


def main():
    print("Getting Tweets")
    tweets = getTweetsAndClean()
    print("Starting model")
    # Build models
    model = Doc2Vec.load('./imdb.d2v')
    test = 'The food is good '
    # Process the string to a acceptable format for the classifier
    test_case = model.infer_vector(word_tokenize(test))
    new_test = test_case.reshape(1, -1)

    # The following code is used for building a classifier
    train_arrays = numpy.zeros((25000, 100))
    train_labels = numpy.zeros(25000)

    # (12500 positive, 12500 negative) for training set
    for i in range(12500):
        prefix_train_pos = 'TRAIN_POS_' + str(i)
        prefix_train_neg = 'TRAIN_NEG_' + str(i)
        train_arrays[i] = model[prefix_train_pos]
        train_arrays[12500 + i] = model[prefix_train_neg]
        train_labels[i] = 1
        train_labels[12500 + i] = 0

    classifier = LogisticRegression()
    classifier.fit(train_arrays, train_labels)
    con = getConnection()
    print("Classifying Tweets")
    for tw in tweets:
        result = classifier.predict(process(model,tw['clean_text']))
        print(result[0])
        dbObj = {'tweet_id' : tw['tweet_id'],
                'sentiment' : int(result[0])}
        insert(con,'calced_tweet_sentiments',dbObj,False)
    con.commit()
    con.close()
    # do node stuff


if __name__ == '__main__':
    main()
