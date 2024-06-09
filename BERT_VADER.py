import nltk
from nltk.corpus import wordnet as wn
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datasets import load_dataset

# Initialize NLTK's WordNet resources
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load the IMDb dataset
dataset = load_dataset("imdb")

# Initialize the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Initialize the list of default replacement candidates
default_replacements = {
    "bad": "not good",
    "terrible": "not great",
    "awful": "not good",
    "horrible": "not pleasant",
    "worst": "not the best",
    "hate": "dislike",
    "dislike": "not fond of",
    "poor": "not great",
    "ugly": "not attractive",
    "dreadful": "not good",
    "nasty": "not pleasant"
}

def find_more_positive_synonym(word):
    """Find synonyms with more positive sentiment scores"""
    if word.lower() in default_replacements:
        return default_replacements[word.lower()]

    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name().replace('_', ' ')
            if synonym.lower() != word.lower():
                synonyms.add(synonym)

    if not synonyms:
        return default_replacements.get(word.lower(), "not good")

    most_positive_word = word
    highest_sentiment = analyzer.polarity_scores(word)['compound']
    print(f"Original word: {word}, Original sentiment: {highest_sentiment}")  # Debug output

    for synonym in synonyms:
        sentiment = analyzer.polarity_scores(synonym)['compound']
        print(f"Synonym: {synonym}, Sentiment: {sentiment}")  # Debug output
        if sentiment > highest_sentiment and sentiment >= 0:
            highest_sentiment = sentiment
            most_positive_word = synonym

    if most_positive_word == word:
        most_positive_word = default_replacements.get(word.lower(), "not good")

    print(f"Chosen synonym: {most_positive_word}, Sentiment: {highest_sentiment}")  # Debug output
    return most_positive_word

def replace_negative_words(text):
    """Replace negative words in the given text with more positive synonyms"""
    words = text.split()
    new_words = words.copy()
    for i, word in enumerate(words):
        sentiment = analyzer.polarity_scores(word)['compound']
        if sentiment < 0:
            print(f"Negative word identified: {word}, Sentiment: {sentiment}")  # Debug output
            positive_synonym = find_more_positive_synonym(word)
            print(f"Replacing {word} with {positive_synonym}")  # Debug output
            new_words[i] = positive_synonym

    """Calculate the sentiment score of the input text"""
    score = analyzer.polarity_scores(text)['compound']
    return ' '.join(new_words), score

if __name__ == '__main__':
    # Example processing of a sample from the IMDb dataset
    sample_text = "The story was boring."
    updated_text = replace_negative_words(sample_text)
    print("Original Text:", sample_text)
    print("Updated Text:", updated_text)