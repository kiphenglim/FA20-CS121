"""
  Returns top prediction for user submitted image and probabilities of top 5
  predictions Includes functions for style, genre, and artist Called by
  front.py
"""

import decimal
from fastai.basic_train import load_learner
from fastai.vision import open_image


def correct_round(val, num):
    """ Helper function used in all probability functions """
    dec_form = decimal.Decimal(str(val))
    decimal.getcontext().prec = num
    return dec_form*1


###STYLE###
# load the learner
style_learn = load_learner(path='./models', file='style_unfreeze_300.pkl')
style_classes = style_learn.data.classes


def predict_style_category(img_file):
    """ Given an image file, returns the top style prediction. """
    prediction = style_learn.predict(open_image(img_file))
    prediction_key = style_classes[prediction[1].item()]
    return "Predicted Category: " + str(prediction_key).replace('_', ' ')


def predict_style_prob(img_file):
    """ Given an image file, returns the top five style predictions and their
    percent confidence.. """
    prediction = style_learn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    # format and round results
    probs_dict = {
        c: probs_list[i] for (i, c) in enumerate(style_classes)}
    sorted_dict = {
        k:str(100*correct_round(v, 2)) + "%" 
        for k,v in sorted(probs_dict.items(), key=lambda item: item[1], reverse=True)}
    percent_list = [str(i).replace(',', ':')
                    for i in list(sorted_dict.items())]
    # only get the top 5 results and format as string
    top_five = str(percent_list[:5])
    special_chars = ['[', ']', "'", '"']
    for i in special_chars:
        top_five = top_five.replace(i, "")

    return "Top 5 Probabilities: " + top_five.replace('_', ' ')


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
    """ Given an image file, returns the top five genre predictions and their
    percent confidence. """
    prediction = genre_learn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    # format and round results
    probs_dict = {
        c: probs_list[i] for (i, c) in enumerate(genre_classes)}
    sorted_dict = {
        k:str(100*correct_round(v, 2)) + "%" 
        for k,v in sorted(probs_dict.items(), key=lambda item: item[1], reverse=True)}
    percent_list = [str(i).replace(',', ':')
                    for i in list(sorted_dict.items())]
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
    # format and round results
    probs_dict = {
        c: probs_list[i] for (i, c) in enumerate(artist_classes)}
    sorted_dict = {
        k:str(100*correct_round(v, 2)) + "%" 
        for k,v in sorted(probs_dict.items(), key=lambda item: item[1], reverse=True)}
    percent_list = [str(i).replace(',', ':')
                    for i in list(sorted_dict.items())]
    # only get the top 5 results and format as string
    top_five = str(percent_list[:5])
    special_chars = ['[', ']', "'", '"']
    for i in special_chars:
        top_five = top_five.replace(i, "")
    return "Top 5 Probabilities: " + top_five
