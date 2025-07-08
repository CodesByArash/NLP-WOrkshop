import pandas as pd
import re

df = pd.read_excel('QA.xlsx')

remove_phrases = [
    'سلام', 'درود', 'با سلام', 'با درود', 'عرض سلام', 'سلام عرض شد', 'سلام و عرض ادب',
    'سلام و احترام', 'با سلام و احترام', 'سلام وقت بخیر', 'وقت بخیر', 'صبح بخیر', 'عصر بخیر', 'روز بخیر',

    'عرض ادب', 'عرض ارادت', 'احترامات فراوان', 'ادب و احترام',

    'خسته نباشید', 'خسته نباشی', 'دست شما درد نکنه', 'زنده باشید', 'خدا قوت',

    'ممنون', 'ممنونم', 'خیلی ممنون', 'بسیار ممنونم', 'تشکر', 'تشکر فراوان', 'سپاس',
    'سپاسگزارم', 'بی‌نهایت سپاس', 'تشکر ویژه', 'سپاس بی‌کران', 'متشکرم', 'متشکر',

    'با تشکر', 'ارادتمند', 'با سپاس', 'باتشکر', 'موفق باشید', 'در پناه خدا', 'یا علی', 'خدانگهدار',

    'یه سوال داشتم', 'یه سوال دارم', 'سوال داشتم', 'سوال دارم', 'یه مورد', 'می‌خواستم بدونم',
    'امکانش هست بفرمایید', 'آیا امکانش هست بفرمایید', 'می‌تونید راهنمایی کنید',

    'سلام و وقت بخیر', 'سلام خسته نباشید', 'سلام عزیز', 'درود بر شما', 'سلام بر شما', 'سلام مهندس',
]
remove_regex = [
    r'کد ملی کاربر: \d{10}',
    r'کد ملی: \d{10}',
    r'^\s*[\u0600-\u06FF]+\s*[,،]?\s*',
    r'[.،!؟]*$'
]

def clean_text(text):
    if not isinstance(text, str):
        return text
    for phrase in remove_phrases:
        text = re.sub(rf'^\s*{phrase}[،, ]*', '', text)
        text = re.sub(rf'[،, ]*{phrase}[،, ]*', '', text)
    for pattern in remove_regex:
        text = re.sub(pattern, '', text)
    text = text.strip()
    return text

if 'question' in df.columns:
    df['cleaned'] = df['question'].apply(clean_text)
else:
    raise Exception("Column 'question' not found")

output_file = 'QA_cleaned.xlsx'
df.to_excel(output_file, index=False)
print(f'File {output_file} stored') 