# Задание №3: борьба со спамом

Вы научитесь:
 * Фильтровать спам.
 * Применять случайный лес и наивный байесовский классификатор.
 * Работать с текстовыми данным в ML.
 * Использовать корсс-валидацию.

## Фильтрация спама
Одна из прикладных задач в которой нало своё применение машинное обучение - это отсеивание спам-писем.
В задании необходимо будет разобраться в предложенном фильтре спама основанном на наивном байесовском классификаторе.
Подбробнее про применение байеса для фильтрации спама можно прочитать [тут](https://ru.wikipedia.org/wiki/Байесовская_фильтрация_спама)

Датасет, который будет использоваться в задании, это 2007 TREC Public Spam Corpus. Датасет содержит 75,419 слегка 
очищенных электронных писем, собранных с email-сервера в течение трёх месяцев 2007 года. Треть датасета составляют spam письма,
а оставшиеся - это хам, легитимные письма. Этот датасет был создан Text REtrieval Conference (TREC) Spam Track в 2007,
в рамках расширения возможностей по обнаружению спама.


## Наивный Баейс
Наивный байесовский алгоритм – это алгоритм классификации, основанный на теореме Байеса с допущением о независимости признаков.
Другими словами, НБА предполагает, что наличие какого-либо признака в классе не связано с наличием какого-либо другого признака.
Например, фрукт может считаться яблоком, если он красный, круглый и его диаметр составляет порядка 8 сантиметров.
Даже если эти признаки зависят друг от друга или от других признаков, в любом случае они вносят независимый вклад в вероятность того,
что этот фрукт является яблоком. В связи с таким допущением алгоритм называется «наивным».

Модели на основе НБА достаточно просты и крайне полезны при работе с очень большими наборами данных. При своей простоте НБА способен превзойти даже некоторые сложные алгоритмы классификации.

В библиотеке scikit-learn наивный байесовский классификатор реализован в классах 
 * naive_bayes.BernoulliNB,
 * naive_bayes.GaussianNB,
 * naive_bayes.MultinomialNB,
 * naive_bayes.ComplementNB,
 
 Пример использования можно увидеть в файле `spam-fighting.ipynb`

## Случайный лес
В библиотеке scikit-learn случайные леса реализованы в классах sklearn.ensemble.RandomForestClassifier (для классификации) и sklearn.ensemble.RandomForestRegressor (для регрессии). Обучение модели производится с помощью функции fit, построение прогнозов — с помощью функции predict. Число деревьев задается с помощью поля класса n_estimators. 

```python
import numpy as np
from sklearn.ensemble import RandomForestRegressor
X = np.array([[1, 2], [3, 4], [5, 6]])
y = np.array([-3, 1, 10])
clf = RandomForestRegressor(n_estimators=100)
clf.fit(X, y)
predictions = clf.predict(X)
```
## Кросс-валидация
Кросс-валидация заключается в разделении выборки на m непересекающихся блоков примерно одинакового размера, после чего выполняется m шагов.
На i-м шаге i-й блок выступает в качестве тестовой выборки, объединение всех остальных блоков — в качестве обучающей выборки.
Соответственно, на каждом шаге алгоритм обучается на некоторой обучающей выборке, после чего вычисляется его качество на тестовой выборке.
После выполнения m шагов мы получаем m показателей качества, усреднение которых и дает оценку кросс-валидации.
Подробнее вы можете прочитать про кросс-валидацию на Википедии (на русском или на английском) или в документации scikit-learn.

Технически кросс-валидация проводится в два этапа:

1. Создается генератор разбиений sklearn.model_selection.KFold, который задает набор разбиений на обучение и валидацию.
Число блоков в кросс-валидации определяется параметром n_splits. Обратите внимание, что порядок следования объектов в выборке
может быть неслучайным, это может привести к смещенности кросс-валидационной оценки. Чтобы устранить такой эффект,
объекты выборки случайно перемешивают перед разбиением на блоки. Для перемешивания достаточно передать генератору KFold параметр shuffle=True.
2. Вычислить качество на всех разбиениях можно при помощи функции sklearn.model_selection.cross_val_score.
В качестве параметра estimator передается классификатор, в качестве параметра cv — генератор разбиений с предыдущего шага.
С помощью параметра scoring можно задавать меру качества, по умолчанию в задачах классификации используется доля верных ответов (accuracy).
Результатом является массив, значения которого нужно усреднить.

## Извление признаков из текста

Введём несколько понятий необходимых для работы с текстовыми данными.

**N-грамма** — последовательность из n элементов. С семантической точки зрения, это может быть последовательность звуков, слогов, слов или букв.
На практике чаще встречается N-грамма как ряд слов, устойчивые словосочетания называют коллокацией.
Последовательность из двух последовательных элементов часто называют биграмма, последовательность из трёх элементов называется триграмма.
Не менее четырёх и выше элементов обозначаются как N-грамма, N заменяется на количество последовательных элементов.  

**Bag of Words** или мешок слов — это модель часто используемая при обработке текстов, представляющая собой неупорядоченный набор слов, входящих в обрабатываемый текст.
Часто модель представляют в виде матрицы, в которой строки соответствуют отдельному тексту, а столбцы — входящие в него слова.
Ячейки на пересечении являются числом вхождения данного слова в соответствующий документ. Данная модель удобна тем, что переводит человеческий язык слов в понятный для компьтера язык цифр.

Соотношение **TF к IDF** - статистический показатель, который используется преимущественно для оценивания важности (весомости) конкретного слова (термина) в контексте всего документа, входящего в общую коллекцию (базу).

Термин TF/IDF имеет англоязычное происхождение, где TF дословно означает частотность вхождения термина (от англ. словосочетания term frequency), а IDF расшифровывается, как обратная (инвертированная) частота документа (от англ. inverse document frequency). В соответствии с отношением TF/IDF весомость определенного слова (термина) прямо зависит от количества раз его использования в конкретном тексте и обратно зависима от числа использования данного слова в множестве остальных документов (текстов).

TF или частота слова - это отношение количества вхождения конкретного термина к суммарному набору слов в исследуемом тексте (документе). Этот показать отражает важность (весомость) слова в рамках определенной статьи/публикации.

IDF или обратная (инвертированная) частота документа - это инверсия частотности, с которой определенное слово фигурирует в коллекции текстов (документов). Благодаря данному показателю можно снизить весомость наиболее широко используемых слов (предлогов, союзов, общих терминов и понятий). Для каждого термина в рамках определенной базы текстов предусматривается лишь одно единственное значение IDF.

Показатель TF/IDF будет выше, если определенное слово с большой частотой используется в конкретном тексте, но редко - в других документах.

Мы будем использовать показатель TF/IDF векторном представлении слов, где каждым элементом вектора будет не частота появления слов в определённом тексте,
как в bag of words, а TF/IDF этого слова.

Примеры использования можно найти [тут](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)

## Инструкция по выполнениюю

 1. Откройте файл `spam=fighting.ipynb` и выполните инструкции в файле.
 Вспомогательный код можно найти в файле `email_read_util.py`.
 Расширение `.ipynb` говорит о том, что это файл Jupiter Notebook.
 Вы можете его выполнить на запущенном [локальном](https://jupyter-notebook.readthedocs.io/en/stable/)
 jupyter сервере или, вынеся код в отдельный `py` файл, запустить как обычный скрипт.
 
 2. Используйте кросс-валидацию для проверки результатов наивного байесовского клссификаторп.
 В роли метрики используйте `score.mean()`.
 
 3. Попробуйте выполнить атаку на байесовский фильтр, называемую [отравление Байеса](https://en.wikipedia.org/wiki/Bayesian_poisoning).
 Для этого возьмите одно из spam-писем из датасета и внесите в него изменения, так чтобы фильтр его принял за ham.
 Как результат приведите изначальное письмо и модифицированное. Посчитайте [расстояние Левенштейна](https://ru.wikipedia.org/wiki/Расстояние_Левенштейна) между ними.
 
 4. Используйте для загрузки датасета функцию `load(path)` из файла `email_read_util.py` вместо `extract_email_text(path)`.
 Функция `load(path)` осуществляет небольшую предобработку текста, заключающуюся в стемминге и удалении
 [стоп-слов](https://en.wikipedia.org/wiki/Stop_words). Сравните работу классфикатора на вашем модифицированном спам-письме.
 Предобработка текста в `load(path)` может занять длительное время.
 
 5. Используйте `CountVectorizer` построенный на бигрммах, а затем замените его на `TfidfVectorizer`.
 Сравните новые классификаторы, а также проверьте их работу на модифицированном письме.
 
 6. Замените наивный байесовский классификатор случайным лесом. Также используйте кросс-валидациб в качестве метрики.
 
 7. Проверьте, как себя поведёт новый классификатор на вашм модифицированном письме.
 