from __future__ import division
import yaml

class NaiveBayesClassifier(yaml.YAMLObject):
    yaml_tag = u'!NaiveBayesClassifier'
    """
    attr_reader :num_categories, :prior_token_count, :prior_category_counts
    attr_accessor :category_names
    """
    """
     Parameters
     ----------
     num_categories: number of categories we want to classify.
     prior_category_counts: array of parameters for a Dirichlet
     prior that we place on the prior probabilities of each
     category. (In other words, these are "virtual counts" of the
     number of times we have seen each category previously.) Set the
     array to all 0's if you want to use maximum likelihood
     estimates. Defaults to uniform reals from the unit interval if
     nothing is set.

     prior_token_count: parameter for a beta prior that we place
     on p(token|category). (In other words, this is a "virtual
     count" of the number of times we have seen each token
     previously.) Set to 0 if you want to use maximum likelihood
     estimates.
    """
    def __init__(self, options):
        options = dict({"num_categories": 2,
                       "prior_token_count": 0.0001}.items() + options.items())
        self.num_categories = options[num_categories]
        self.prior_token_count = options[prior_token_count]
        random = [random.random() for _ in xrange(self.num_categories)]
        # self.prior_category_counts = options[prior_category_counts] || Array.new(self.num_categories) { rand }
        self.prior_category_counts = options["prior_category_counts"] if "prior_catecory counts" in options else random

        self.category_names = options["category_names"] if  "category_names" in options else [str(x) for  x in range(self.num_categories)]
      
           #|| (0..num_categories-1).map(&:to_s).to_a

        # `@token_counts[category][token]` is the (weighted) number of
        # times we have seen `token` with this category.
        # self.token_counts = Array.new(self.num_categories) do
        # Hash.new { |h, token| h[token] = 0 }
        self.token_counts = [defaultdict(0) for _ in range(self.num_categories)]

        # `@total_token_counts[category]` is always equal to
        # `@token_counts[category].sum`.
        self.total_token_counts = [0 for _ in range(self.num_categories)]

        # `@category_counts[category]` is the (weighted) number of training
        # examples we have seen with this category.
        self.category_counts =  [0 for _ in range(self.num_categories)]

      
        # Given a labeled training example (i.e., an array of tokens and its
        # probability of belonging to a certain category), update the parameters of the
        # Naive Bayes model.
        # Parameters
        # ----------
        # example: an array of tokens.
        # category_index: the index of
        # the category this example
        # belongs to.
        # probability: the probability
        # that the example belongs to
        # the category.
        #
        """
        def train(self, example, category_index, probability = 1):
            example.each do |token|
                self.token_counts[category_index][token] += probability
                self.total_token_counts[category_index] += probability
                                   end
        @category_counts[category_index] += probability
        end
        """

        # Performs a Naive Bayes EM algorithm with two classes.
        """
        def self.train_em(max_epochs, training_examples)
            prev_classifier = NaiveBayesClassifier.new
            max_epochs.times do
            classifier = NaiveBayesClassifier.new

            # E-M training
            training_examples.each do |example|
            # E-step: for each training example,
            # recompute its classification
            # probabilities.
            posterior_category_probs = prev_classifier.get_posterior_category_probabilities(example)

            # M-step:
            # for each category, recompute the probability of generatingeach token.
            posterior_category_probs.each_with_index do |p, category|
            classifier.train(example, category, p)
            end
            end
            prev_classifier = classifier
            # TODO:
            # add a convergence check, so we  can break out early  if  we  want.
            end
            return prev_classifier
            end
        """

    # Returns the *index* (not the name) of the category the tokens are
    # classified under.
    def classify(self, tokens):
        max_prob = -1
        max_category = -1

        if not tokens:
            # If the example is empty, find the category with the highest prior probability.
            """
            (0..@num_categories - 1).each do |i|
                 prior_prob = get_prior_category_probability(i)
                 max_prob, max_category = prior_prob, i if prior_prob > max_prob
            end
            """
            for i in range(self.num_categories):
                 prior_prob = self.get_prior_category_probability(i)
                 max_prob = prior_prob
                 max_category = i if prior_prob > max_prob else max_category
        else:
            # Otherwise, find the  category with the  highest posterior  probability.
            """
            get_posterior_category_probabilities(tokens).each_with_index do |prob, category|
            max_prob, max_category = prob, category if prob > max_prob
            """

            for category, prob in enumerate( self.get_posterior_category_probabilities(tokens)):
                max_prob, max_category = prob, category if prob > max_prob else max_category
        return max_category


    # Returns p(category | token), for each category, in an array.
    def get_posterior_category_probabilities(self, tokens):
        """
        unnormalized_posterior_probs = (0..@num_categories-1).map do |category|
            p = tokens.map { |token| get_token_probability(token, category) }.reduce(:*) # p(tokens | category)
            p * get_prior_category_probability(category) # p(tokens | category) * p(category)
        end
        """
        unnormalized_posterior_probs = []
        for category in range(self.num_categories):
            values = map(lambda token: self.get_token_probability(token, category), tokens)
            p = reduce (lambda x, y: x*y, values )
            unnormalized_posterior_probs.append(p)

        normalization = sum(unnormalized_posterior_probs)
        normalization = 1 if normalization == 0 else normalization
        """
        return unnormalized_posterior_probs.map{ |p| p / normalization }
        """
        #return map(lambda p, y: p / normalization, unnormalized_posterior_probs)
        return [p / normalization for p in unnormalized_posterior_probs ]


    # Returns p(token | category).
    def get_token_probability(self, token, category_index):
        denom = self.total_token_counts[category_index] + len(self.token_counts[category_index])* self.prior_token_count
        if denom == 0:
           return 0
        else:
            #((self.token_counts[category_index][token] || 0) + self.prior_token_count).to_f / denom
           val = (self.token_counts[category_index][token]) if token in self.token_counts[category_index] else 0
           return (val + self.prior_token_count) / denom

    # Returns p(category).
    def get_prior_category_probability(self, category_index):
        denom = sum(self.category_counts) +  sum(self.prior_category_counts)
        if denom == 0:
            return 0
        else:
            return (self.category_counts[category_index] + self.prior_category_counts[category_index]) / denom

