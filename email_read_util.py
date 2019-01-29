import string
import email
import nltk

punctuations = list(string.punctuation)
stopwords = set(nltk.corpus.stopwords.words('english'))
stemmer = nltk.PorterStemmer()


# Собирает разные части письма в простой список строк
def flatten_to_string(parts):
    ret = []
    if type(parts) == str:
        ret.append(parts)
    elif type(parts) == list:
        for part in parts:
            ret += flatten_to_string(part)
    elif parts.get_content_type == 'text/plain':
        ret += parts.get_payload()
    return ret


# Извлекает тему и тело письма из одного email файла
def extract_email_text(path):
    # Загрузка файла по из указанного пути
    with open(path, errors='ignore') as f:
        msg = email.message_from_file(f)
    if not msg:
        return ""

    # Получение темы письма
    subject = msg['Subject']
    if not subject:
        subject = ""

    # Получение тела пиьсма
    body = ' '.join(m for m in flatten_to_string(msg.get_payload()) if type(m) == str)
    if not body:
        body = ""

    return subject + ' ' + body


# Преобразует email файл в массив из основ слов (https://ru.wikipedia.org/wiki/Стемминг)
def load(path):
    email_text = extract_email_text(path)
    if not email_text:
        return []

    # Преобразование текста в массив слов
    tokens = nltk.word_tokenize(email_text)

    # Удаление знаков препинания из массива токенов
    tokens = [i.strip("".join(punctuations)) for i in tokens if i not in punctuations]

    # Удаление стоп-слов и стемминг токенов (https://en.wikipedia.org/wiki/Stop_words)
    if len(tokens) > 2:
        return [stemmer.stem(w) for w in tokens if w not in stopwords]
    return []
