import sys
sys.path.append("./yaml")

import yaml
import NaiveBayesClassifier


class String:

    def __init__(self, text):
        self.text = text.lower()

    def find_ngrams(self, text, n):
        chars = zip(*[text[i:] for i in range(n)])
        return ["".join(txt) for txt in chars]
    
    'Returns a set of character n-grams computed from this string.'
    def to_ngrams(self, n):
        return self.find_ngrams(self.text, n)


class LanguageDetector(yaml.YAMLObject):
    yaml_tag = u'!LanguageDetector'
    
    """
    Gven a set of sentences in multiple languages,
    build a classifier to detect the majority language.
    """

    def __init__(self, options):
       
        options = dict({"ngram_size": 3}.items() + options.items())
        self.classifier = NaiveBayesClassifier(2)
        self.ngram_size = options["ngram_size"]

    """
    def initialize(options = {})
    options = {:ngram_size => 3}.merge(options)
    @ngram_size = options[:ngram_size]
    @classifier = NaiveBayesClassifier.new(:num_categories => 2)
    """
    """
    def train(max_epochs, training_sentences):
        classifier = NaiveBayesClassifier.train_em(max_epochs, training_sentences.map{ |sentence| sentence.to_ngrams(ngram_size) })
        classifier.category_names =
        if classifier.get_prior_category_probability(0) > @classifier.get_prior_category_probability(1)
            %w( majority minority )
        else
            %w( minority majority )
    """

    # Returns the (named) category the sentence belongs to.
    def classify(self, text):
        sentence = String(text)
        category_index = self.classifier.classify(sentence.to_ngrams(self.ngram_size))
        return self.classifier.category_names[category_index]

    def probabilities(self, sentence):
        classifier.get_posterior_category_probabilities(sentence.to_ngrams(self.ngram_size))
    """
    # Dumps the language model to a file.
    def yamlize(filename):
        File.open(filename, "w") do |f|
        f.puts self.to_yaml
    """

    # Loads the language model from a file.
    def load_yaml(filename):
        stream = open("english-tweet-detector.yaml", "r")
        return yaml.load(stream)
