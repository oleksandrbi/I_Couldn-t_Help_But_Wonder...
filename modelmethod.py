from gensim import utils
from gensim.models.doc2vec import TaggedDocument, LabeledSentence
from gensim.models import Doc2Vec
import numpy
from nltk.tokenize import word_tokenize
from sklearn.linear_model import LogisticRegression

model = Doc2Vec.load('./imdb.d2v')
test = "this food is good, i had a great time"

def process(s):
    s_vector = model.infer_vector(word_tokenize(test))
    new_s = s_vector.reshape(1, -1)
    return new_s

#Process the string to a acceptable format for the classifier
test_case = model.infer_vector(word_tokenize(test))
new_test = test_case.reshape(1, -1)

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

classifier = LogisticRegression()
classifier.fit(train_arrays, train_labels)
print(classifier.predict(process(test)))
