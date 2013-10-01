#import sys
#sys.path.append("./yaml")

#import yaml
#from LanguageDetector import LanguageDetector
#from NaiveBayesClassifier import NaiveBayesClassifier

#f = open('english-tweet-detector.yaml')
#settings = yaml.load(f)
#print(settings)

#e = settings.classify("pl")
#print e


#class LanguageDetector:
#    __init__(self, options)
from LanguageFilterControll import testIfEnglish

testIfEnglish("hubbabubba")
