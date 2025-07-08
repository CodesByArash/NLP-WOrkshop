import re
from docx import Document
from hazm import Normalizer as HazmNormalizer, word_tokenize as hazm_word_tokenize, POSTagger as HazmPOSTagger

def remove_emojis(text):
    emoji_pattern = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def remove_emails_urls_html(text):
    text = re.sub(r'\S+@\S+', '', text)  
    text = re.sub(r'http[s]?://\S+', '', text)  
    text = re.sub(r'<.*?>', '', text)  
    return text

def clean_text(text):
    text = remove_emojis(text)
    text = remove_emails_urls_html(text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def main():
    doc = Document('persian_text.docx')
    text = '\n'.join([p.text for p in doc.paragraphs])
    text = clean_text(text)

    hazm_normalizer = HazmNormalizer()
    text_hazm = hazm_normalizer.normalize(text)

    hazm_tagger = HazmPOSTagger(model='pos_tagger.model')
    hazm_tokens = hazm_word_tokenize(text_hazm)
    hazm_pos = hazm_tagger.tag(hazm_tokens)

    with open('persian_text_cleaned_hazm.txt', 'w', encoding='utf-8') as f:
        f.write(text_hazm)
    print('hazm:', list(zip(hazm_tokens[:10], hazm_pos[:10])))
    print('Task 1 done. Cleaned text saved to persian_text_cleaned_hazm.txt')

if __name__ == '__main__':
    main()