import re
import random
from docx import Document
from hazm import Normalizer as HazmNormalizer, word_tokenize as hazm_word_tokenize, sent_tokenize as hazm_sent_tokenize, POSTagger as HazmPOSTagger, Lemmatizer as HazmLemmatizer

def clean_text(text):
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'http[s]?://\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def main():
    doc = Document('paragraphs.docx')
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    hazm_normalizer = HazmNormalizer()
    hazm_tagger = HazmPOSTagger(model='pos_tagger.model')
    hazm_lemmatizer = HazmLemmatizer()
    table = []
    all_sents = []
    for idx, para in enumerate(paragraphs):
        para_clean = clean_text(para)
        para_hazm = hazm_normalizer.normalize(para_clean)
        sents_hazm = hazm_sent_tokenize(para_hazm)
        words_hazm = hazm_word_tokenize(para_hazm)
        pos_hazm = hazm_tagger.tag(words_hazm)
        verbs_hazm = [w for w, t in zip(words_hazm, pos_hazm) if t == 'V']
        nouns_hazm = [w for w, t in zip(words_hazm, pos_hazm) if t == 'N']
        table.append({
            'paragraph': idx+1,
            'sentences_hazm': len(sents_hazm),
            'words_hazm': len(words_hazm),
            'verbs_hazm': len(verbs_hazm),
            'nouns_hazm': len(nouns_hazm),
        })
        all_sents.extend(sents_hazm)
    print('Para | Sents | Words_hazm | Verbs_hazm | Nouns_hazm')
    for row in table:
        print(f"{row['paragraph']:>4} | {row['sentences_hazm']:>5} | {row['words_hazm']:>10} | {row['verbs_hazm']:>10} | {row['nouns_hazm']:>10}")
    # 5 random sentences
    sample_sents = random.sample(all_sents, min(5, len(all_sents)))
    print('\nSample sentences analysis:')
    for sent in sample_sents:
        tokens_hazm = hazm_word_tokenize(sent)
        pos_hazm = hazm_tagger.tag(tokens_hazm)
        lemmas_hazm = [hazm_lemmatizer.lemmatize(w) for w in tokens_hazm]
        print('Sentence:', sent)
        print('Tokens:', tokens_hazm)
        print('POS_hazm:', pos_hazm)
        print('Lemmas_hazm:', lemmas_hazm)
        print('---')
    print('Task 2 done.')

if __name__ == '__main__':
    main()
