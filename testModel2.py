import pickle
from collections import defaultdict

def default_dict():
    return defaultdict(int)

class BiGramLanguageModel:
    def __init__(self):
        # Initialize data structures to store bi-gram frequencies
        self.bigram_counts = defaultdict(default_dict)
        self.unigram_counts = defaultdict(int)
        self.vocabulary = set()

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

# Load the model using pickle
with open('bi_gram_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# Example usage:
current_word_example = "playing"
predicted_word = loaded_model.predict_next_word(current_word_example)
candidates = loaded_model.generate_candidates(current_word_example)
print(f"Given '{current_word_example}', the predicted next word is '{predicted_word}'.")
print(f"Given '{current_word_example}', the Candidate are '{candidates}'.")