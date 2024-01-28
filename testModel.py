import pickle
from collections import defaultdict
import nltk
from nltk.corpus import brown

def default_dict():
    return defaultdict(int)

class BiGramLanguageModel:
    def __init__(self):
        # Initialize data structures to store bi-gram frequencies
        self.bigram_counts = defaultdict(default_dict)
        self.unigram_counts = defaultdict(int)
        self.vocabulary = set()

    def train(self, corpus):
        # Train the bi-gram language model on a given corpus
        tokens = corpus.split()
        print(tokens)
        for i in range(len(tokens) - 1):
            current_word = tokens[i]
            next_word = tokens[i + 1]

            # Update bi-gram and unigram counts
            self.bigram_counts[current_word][next_word] += 1
            self.unigram_counts[current_word] += 1
            self.vocabulary.add(current_word)
            self.vocabulary.add(next_word)

    def train_nltk_corpus(self, corpus_name):
        # Train the model on an NLTK corpus
        corpus = " ".join(brown.words(categories=corpus_name))
        self.train(corpus)
        

    def calculate_probability(self, current_word, next_word):
        # Calculate the conditional probability P(next_word | current_word)
        if current_word in self.unigram_counts:
            if next_word in self.bigram_counts[current_word]:
                return self.bigram_counts[current_word][next_word] / self.unigram_counts[current_word]
            else:
                # Smoothing (optional): Add a small constant to handle unseen bi-grams
                return 1e-5
        else:
            # Handle unseen words by assigning a small probability
            return 1e-5

    def predict_next_word(self, current_word):
        # Predict the next word given the current word
        if current_word in self.bigram_counts:
            next_word_candidates = self.bigram_counts[current_word]
            # Choose the word with the highest probability
            next_word = max(next_word_candidates, key=lambda w: self.calculate_probability(current_word, w))
            return next_word
        else:
            # If the current word is not in the training data, return a placeholder
            return "<UNKNOWN>"
        
    def generate_candidates(self, input_word, num_candidates=5):
        # Generate candidate words based on the input word
        if input_word in self.vocabulary:
            next_word_candidates = self.bigram_counts[input_word]
            # Sort candidates by probability in descending order
            sorted_candidates = sorted(next_word_candidates, key=lambda w: self.calculate_probability(input_word, w), reverse=True)
            # Return the top N candidates
            return sorted_candidates[:num_candidates]
        else:
            return []

    def save_model(self, filename):
        # Save the model to a file using pickle
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load_model(cls, filename):
        # Load the model from a file using pickle
        with open(filename, 'rb') as file:
            loaded_model = pickle.load(file)
        return loaded_model

# Example usage:
nltk.download('brown')  # Download the Brown corpus if not already downloaded

# Train the model
model = BiGramLanguageModel()
model.train_nltk_corpus('news')

# Save the trained model
# model.save_model('bi_gram_model.pkl')

# Load the model at another place
loaded_model = BiGramLanguageModel.load_model('bi_gram_model.pkl')

# Predict using the loaded model
current_word_example = "This"
predicted_word = loaded_model.predict_next_word(current_word_example)
print(f"Given '{current_word_example}', the predicted next word is '{predicted_word}'.")
