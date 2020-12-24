from natasha import Doc, Segmenter
import pymorphy2


morph = pymorphy2.MorphAnalyzer()
segmenter = Segmenter()


def lemmatize(word: str):
    res = morph.parse(word)
    if len(res) > 0:
        return res[0].normal_form
    else:
        return None

def get_tokens(text: str):
    doc = Doc(text.lower())
    doc.segment(segmenter)
    print(doc.tokens)

    lemmas = []
    for token in doc.tokens:
        res = morph.parse(token.text)
        if len(res) > 0:
            lemma = res[0].normal_form
            lemmas.append(lemma)

    return set(lemmas)