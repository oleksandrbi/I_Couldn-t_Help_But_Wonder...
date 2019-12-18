#Yuliang Xue
#Description: Using Doc2Vec model with Gensim to do sentiment analysis on corpus.

#Dependencies:
#Install through pip
#1. tqdm - Make loop show progress bar (I haven't input this yet.)
#2. sklearn
#3. gensim

#Imports
# gensim modules
from gensim import utils
from gensim.models.doc2vec import TaggedDocument, LabeledSentence
from gensim.models import Doc2Vec

# numpy
import numpy

import smart_open

# random
from random import shuffle

# Used as classifier
from sklearn.linear_model import LogisticRegression

#Input format
#For this program, the input format should be txt. Each document should be on one line, separated by new lines.

#Iterator to process corpus
class LabeledLineSentence(object):
    def __init__(self, sources):
        self.sources = sources
        flipped = {}

        # make sure that keys are unique
        for key, value in sources.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                raise Exception('Non-unique prefix encountered')

    def __iter__(self):
        for source, prefix in self.sources.items():
            with smart_open.open(source) as fin:
                for item_no, line in enumerate(fin):
                    yield TaggedDocument(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])

    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with smart_open.open(source) as fin:
                for item_no, line in enumerate(fin):
                    self.sentences.append(TaggedDocument(utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences

#Set up sources for testing set, training set, and target set.
sources = {'test-neg.txt':'TEST_NEG', 'test-pos.txt':'TEST_POS', 'train-neg.txt':'TRAIN_NEG', 'train-pos.txt':'TRAIN_POS', 'train-unsup.txt':'TRAIN_UNS'}
sentences = LabeledLineSentence(sources)

#open file with Iterator and create model through doc2vec
#Parameters for doc2vec function
#min_count = Ignores all words with a total frequency lower than this.
#vector_size = Dimensionality of the feature vectors.
#sample = The threshold for configuring which higher-frequency words are randomly downsampled, useful range is (0, 1e-5).
#workers = Use these many worker threads to train the model
#epochs = number of iterations over the corpus.
model = Doc2Vec(min_count=1, window=10, vector_size=100, sample=1e-4, negative=5, workers=8)
model.build_vocab(sentences.to_array())

model.train(sentences.sentences_perm(), total_examples=model.corpus_count, epochs=model.epochs)

#Save and load current model
model.save('./imdb.d2v')
#model = Doc2Vec.load('./imdb.d2v')

print("---test---")
#Testing for finding most similar word.
print(model.wv.most_similar('good'))

#Sample vector for first sentence from negative training set
#model['TRAIN_NEG_0']

#The following code is used for building a classifier
train_arrays = numpy.zeros((25000, 100))
train_labels = numpy.zeros(25000)

#(12500 positive, 12500 negative) for training set
for i in range(12500):
    prefix_train_pos = 'TRAIN_POS_' + str(i)
    prefix_train_neg = 'TRAIN_NEG_' + str(i)
    train_arrays[i] = model[prefix_train_pos]
    train_arrays[12500 + i] = model[prefix_train_neg]
    train_labels[i] = 1
    train_labels[12500 + i] = 0

#Following is for building the testing vectors
test_arrays = numpy.zeros((25000, 100))
test_labels = numpy.zeros(25000)

for i in range(12500):
    prefix_test_pos = 'TEST_POS_' + str(i)
    prefix_test_neg = 'TEST_NEG_' + str(i)
    test_arrays[i] = model[prefix_test_pos]
    test_arrays[12500 + i] = model[prefix_test_neg]
    test_labels[i] = 1
    test_labels[12500 + i] = 0

#Test the classifier to check correct percentage
classifier = LogisticRegression()
classifier.fit(train_arrays, train_labels)

#print the score of the classifier
print(classifier.score(test_arrays, test_labels))
