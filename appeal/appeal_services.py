from django.shortcuts import get_object_or_404
from catboost import CatBoostClassifier
import re
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
import pickle
import numpy as np

from .models import Appeal, Category


def get_appeal_from_id(appeal_id):
    return get_object_or_404(Appeal, pk=appeal_id)


def set_category_for_appeal(form):
    form.instance.CategoryValue = Category.objects.get(
        pk=predict_category(form.instance.AppealContent)
    )
    form.save()


def predict_category(text):
    text = [text]

    preprocessed_text = text_preprocessing(text)
    with open("appeal/static/appeal/machine_learning/vectorizer.sav", "rb") as f:
        vector = pickle.load(f)
    vector_text = vector.transform(preprocessed_text)
    with open("appeal/static/appeal/machine_learning/reducer.sav", "rb") as f:
        reduce = pickle.load(f)
    reduced_data = reduce.transform(vector_text)
    with open("appeal/static/appeal/machine_learning/topic_modeler.sav", "rb") as f:
        topic = pickle.load(f)
    topic_model = topic.transform(vector_text)
    text_topic = np.column_stack((reduced_data, topic_model))
    with open("appeal/static/appeal/machine_learning/normalizer.sav", "rb") as f:
        norm = pickle.load(f)
    norm_data = norm.transform(text_topic)

    model = CatBoostClassifier()
    model.load_model('appeal/static/appeal/machine_learning/CB_classifier')
    category = model.predict(norm_data)
    return int(category[0][0])


def text_preprocessing(data):
    stopwords_rus = stopwords.words('russian')
    # расширяем набор стоп слов
    stopwords_rus.extend(
        ['большой', 'весь', 'всё', 'ещё', 'мочь', 'нибыть', 'свой', 'хороший', 'это']
    )
    morph = MorphAnalyzer()
    clean_texts = []
    for text in data:
        # к нижнему регистру
        text = text.lower()
        # ост только символы
        text = re.sub('[^а-я]', ' ', text)
        # пробелы
        text = re.sub(r'\s+', ' ', text, flags=re.I)
        text = text.split()
        words_list = []
        for word in text:
            # лемма слова
            lemma = morph.parse(word)[0]
            # стоп слова, ошибки в словах, аббревиатуры
            if lemma.normal_form not in stopwords_rus and 'UNKN' not in lemma.tag:
                words_list.append(lemma.normal_form)
        clean_texts.append(' '.join(words_list))
    return clean_texts
