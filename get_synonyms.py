import spacy

nlp = spacy.load("en_core_web_sm")

def get_synonyms_spacy(word):
    doc = nlp(word)
    synonyms = [token.text for token in doc if token.has_vector]
    return synonyms

# Example usage:
word = "happy"
synonyms = get_synonyms_spacy(word)
print(synonyms)