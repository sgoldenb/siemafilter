import sys
sys.path.append("./yaml")

import yaml
#import os
from LanguageDetector import LanguageDetector
from NaiveBayesClassifier import NaiveBayesClassifier

#path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'english-tweet-detector.yaml')
#path ="res_mods/0.8.8/scripts/client/messenger/gui/scaleform/channels/english-tweet-detector.yaml"

f = open("english-tweet-detector.yaml")
settings = yaml.load(f)


def testIfEnglish(text):
    return settings.classify(text) == "majority"

