# -*- coding: utf-8 -*-

"""
train_model.

| Trains a collection of new conjugation models.


| The conjugation data conforms to the JSON structure of the files in mlconjug3/data/conjug_manager/
| or to the XML schema defined by Verbiste.
| More information on Verbiste at https://perso.b2b2c.ca/~sarrazip/dev/conjug_manager.html

"""

import mlconjug3
import pickle
import pprint
import numpy as np
from functools import partial
from time import time
import joblib

from pathlib2 import Path

np.random.seed(42)

# Set a language to train the Conjugator on
langs = ('ro', 'it', 'en', 'es', 'fr', 'pt')

managers = (mlconjug3.Verbiste, mlconjug3.ConjugManager)
results = {}

for lang in langs:
    my_file = Path('raw_data/experiments/reduced_search/best_model_parameters_{0}.pkl'.format(lang))
    if not my_file.exists():
        continue
    else:
        # Loads best model parameters
        with open('raw_data/experiments/reduced_search/best_model_parameters_{0}.pkl'.format(lang),
                  'rb') as file:
            best_params = joblib.load(file)
    # Set a ngram range sliding window for the vectorizer
    ngrange = (2, 7)

    # Transforms dataset with CountVectorizer. We pass the function extract_verb_features to the CountVectorizer.
    vectorizer = mlconjug3.CountVectorizer(analyzer=partial(mlconjug3.extract_verb_features,
                                                            lang=lang,
                                                            ngram_range=ngrange),
                                           binary=True, lowercase=False)

    # Feature reduction
    feature_reductor = mlconjug3.SelectFromModel(mlconjug3.LinearSVC(penalty="l1",
                                                                     dual=False,
                                                                     verbose=0))

    # Prediction Classifier
    classifier = mlconjug3.SGDClassifier(verbose=0)

    # Initialize Data Set
    dataset = mlconjug3.DataSet(mlconjug3.Verbiste(language=lang).verbs)
    dataset.split_data(proportion=1)

    # Initialize Conjugator
    model = mlconjug3.Model(vectorizer, feature_reductor, classifier)
    model.pipeline.set_params(**best_params)
    conjugator = mlconjug3.Conjugator(lang, model)

    # Training and prediction
    # print('training {0} model on train set'.format(lang))
    # t0 = time()
    # conjugator.model.train(dataset.train_input, dataset.train_labels)
    # duration = round(time() - t0, 3)
    # print('{0} model trained on train set in {1} seconds.'.format(lang, duration))
    # predicted = conjugator.model.predict(dataset.test_input)
    # predicted2 = conjugator.model.predict(dataset.verbs_list)

    print('training {0} model on full data set'.format(lang))
    t0 = time()
    conjugator.model.train(dataset.verbs_list, dataset.templates_list)
    duration2 = round(time() - t0, 3)
    print('{0} model trained on full data set in {1} seconds.'.format(lang, duration2))
    predicted_full = conjugator.model.predict(dataset.verbs_list)

    # Assess the performance of the model's predictions
    # score = len([a == b for a, b in zip(predicted, dataset.test_labels) if a == b]) / len(predicted)
    # misses = len([a != b for a, b in zip(predicted, dataset.test_labels) if a != b])
    # entries = len(predicted)
    # print('The score of the {0} model trained on the train set is {1} with the {2} model on test set.'.format(lang, score, managers[0].__name__))
    #
    # score2 = len([a == b for a, b in zip(predicted2, dataset.templates_list) if a == b]) / len(predicted2)
    # misses2 = len([a == b for a, b in zip(predicted2, dataset.templates_list) if a != b])
    # entries2 = len(predicted2)
    # print('The score of the {0} model trained on the train set is {1} with the {2} model on full dataset.'.format(lang, score2, managers[0].__name__))

    score_full = len([a == b for a, b in zip(predicted_full, dataset.templates_list) if a == b]) / len(predicted_full)
    misses_full = len([a == b for a, b in zip(predicted_full, dataset.templates_list) if a != b])
    entries_full = len(predicted_full)
    print('The score of the {0} model trained on the full dataset is {1} with the {2} model.'.format(lang, score_full, managers[0].__name__))

    results[lang] = (duration2, ), (score_full, misses_full, entries_full)

    # Save trained model
    with open('raw_data/experiments/trained_model-{0}-final.pickle'.format(lang), 'wb') as file:
        pickle.dump(conjugator.model, file)
pprint.pprint(results)
