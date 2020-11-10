"""
  Returns top prediction for user submitted image and probabilities of top 5
  predictions Includes functions for style, genre, and artist Called by
  front.py
"""

import decimal
from fastai.basic_train import load_learner
from fastai.vision import open_image

# Helper function used in all probability functions for correct rounding
# Faced errors when rounidng floats, this keeps precision and handles those cases


def correct_round(arr, num):
    newList = []
    for value in arr:
        d = decimal.Decimal(str(value))
        decimal.getcontext().prec = num
        newList.append(d*1)
    return newList


###STYLE###
# load the learner
style_learn = load_learner(path='./models', file='style_unfreeze_300.pkl')
style_classes = style_learn.data.classes


def predict_style_category(img_file):
    """ Given an image file, returns the top style prediction. """
    prediction = style_learn.predict(open_image(img_file))
    prediction_key = style_classes[prediction[1].item()]
    return "Predicted Category: " + str(prediction_key)


def predict_style_prob(img_file):
    """ Given an image file, returns the top five style predictions and their percent confidence.. """
    prediction = style_learn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    # format and round results
    prob_sorted = sorted(probs_list, key=lambda x: float(x), reverse=True)
    prob_rounded = correct_round(prob_sorted, 2)
    percent_dict = {
        c: str(100*prob_rounded[i]) + "%" for (i, c) in enumerate(style_classes)}
    percent_list = [str(i).replace(',', ':')
                    for i in list(percent_dict.items())]
    # only get the top 5 results and format as string
    top_five = str(percent_list[:5])
    special_chars = ['[', ']', "'", '"']
    for i in special_chars:
        top_five = top_five.replace(i, "")

    return "Top 5 Probabilities: " + top_five


##GENRE##
# load the learner
genre_learn = load_learner(path='./models', file='genreLRChanged.pkl')
genre_classes = genre_learn.data.classes


def predict_genre_category(img_file):
    """ Given an image file, returns the top genre prediction. """
    prediction = genre_learn.predict(open_image(img_file))
    prediction_key = genre_classes[prediction[1].item()]
    return "Predicted Category: " + str(prediction_key)


def predict_genre_prob(img_file):
    """ Given an image file, returns the top five genre predictions and their percent confidence. """
    prediction = genre_learn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    prob_sorted = sorted(probs_list, key=lambda x: float(x), reverse=True)
    # format and round results
    prob_rounded = correct_round(prob_sorted, 2)
    percent_dict = {
        c: str(100*prob_rounded[i]) + "%" for (i, c) in enumerate(genre_classes)}
    percent_list = [str(i).replace(',', ':')
                    for i in list(percent_dict.items())]
    # only get the top 5 results and format as string
    top_five = str(percent_list[:5])
    special_chars = ['[', ']', "'", '"']
    for i in special_chars:
        top_five = top_five.replace(i, "")

    return "Top 5 Probabilities: " + top_five


##ARTIST##
# load the learner
artist_learn = load_learner(path='./models', file='artistLR2.pkl')
artist_classes = artist_learn.data.classes


def predict_artist_category(img_file):
    """ Given an image, returns the top artist prediction. """
    print("prediction called *******")
    prediction = artist_learn.predict(open_image(img_file))
    prediction_key = artist_classes[prediction[1].item()]
    return "Predicted Category: " + str(prediction_key)


def predict_artist_prob(img_file):
    """ Given an image, returns the top five artist predictions and their percent confidence. """
    prediction = artist_learn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    prob_sorted = sorted(probs_list, key=lambda x: float(x), reverse=True)
    # format and round results
    prob_rounded = correct_round(prob_sorted, 2)
    percent_dict = {
        c: str(100*prob_rounded[i]) + "%" for (i, c) in enumerate(artist_classes)}
    percent_list = [str(i).replace(',', ':')
                    for i in list(percent_dict.items())]
    # only get the top 5 results and format as string
    top_five = str(percent_list[:5])
    special_chars = ['[', ']', "'", '"']
    for i in special_chars:
        top_five = top_five.replace(i, "")
    return "Top 5 Probabilities: " + top_five
