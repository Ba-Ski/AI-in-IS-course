# Задание №3: борьба со спамом

Вы научитесь:
 * Фильтровать спам.
 * Работать с текстовыми данным в ML.
 * Использовать корсс-валидацию.

## Классификация спама
https://ru.wikipedia.org/wiki/Байесовская_фильтрация_спама

## Наивный Баейс
Наивный байесовский алгоритм – это алгоритм классификации, основанный на теореме Байеса с допущением о независимости признаков. Другими словами, НБА предполагает, что наличие какого-либо признака в классе не связано с наличием какого-либо другого признака. Например, фрукт может считаться яблоком, если он красный, круглый и его диаметр составляет порядка 8 сантиметров. Даже если эти признаки зависят друг от друга или от других признаков, в любом случае они вносят независимый вклад в вероятность того, что этот фрукт является яблоком. В связи с таким допущением алгоритм называется «наивным».

В библиотеке scikit-learn наивный байесовский классификатор реализован в классах 
 * naive_bayes.BernoulliNB,
 * naive_bayes.GaussianNB,
 * naive_bayes.MultinomialNB,
 * naive_bayes.ComplementNB,
 
 Пример использования можно увидеть в файле `spam-fighting.ipynb`

Модели на основе НБА достаточно просты и крайне полезны при работе с очень большими наборами данных. При своей простоте НБА способен превзойти даже некоторые сложные алгоритмы классификации.

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
Кросс-валидация заключается в разделении выборки на m непересекающихся блоков примерно одинакового размера, после чего выполняется m шагов. На i-м шаге i-й блок выступает в качестве тестовой выборки, объединение всех остальных блоков — в качестве обучающей выборки. Соответственно, на каждом шаге алгоритм обучается на некоторой обучающей выборке, после чего вычисляется его качество на тестовой выборке. После выполнения m шагов мы получаем m показателей качества, усреднение которых и дает оценку кросс-валидации. Подробнее вы можете послушать про кросс-валидацию в видео "Проблема переобучения. Методология решения задач машинного обучения" из первого модуля, а также почитать на Википедии (на русском или на английском) или в документации scikit-learn.

Технически кросс-валидация проводится в два этапа:

1. Создается генератор разбиений sklearn.model_selection.KFold, который задает набор разбиений на обучение и валидацию. Число блоков в кросс-валидации определяется параметром n_splits. Обратите внимание, что порядок следования объектов в выборке может быть неслучайным, это может привести к смещенности кросс-валидационной оценки. Чтобы устранить такой эффект, объекты выборки случайно перемешивают перед разбиением на блоки. Для перемешивания достаточно передать генератору KFold параметр shuffle=True.
2. Вычислить качество на всех разбиениях можно при помощи функции sklearn.model_selection.cross_val_score. В качестве параметра estimator передается классификатор, в качестве параметра cv — генератор разбиений с предыдущего шага. С помощью параметра scoring можно задавать меру качества, по умолчанию в задачах классификации используется доля верных ответов (accuracy). Результатом является массив, значения которого нужно усреднить.

## Извление признаков из текста
https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction

## Инструкция по выполнениюю

 1. Открыть файл `spam=fighting.ipynb` и выполнить инструкции в файле.
 Вспомогательный код можно найти в фале `email_read_util.py`
 Расширение `.ipynb` говорит о том, что это файл Jupiter Notebook.
 Вы можете его выполнить на запущенном [локальном](https://jupyter-notebook.readthedocs.io/en/stable/) jupyter сервере
 или, вынеся код в отдельный `py` файл, запустить как обычный скрипт.
 2. Используйте кросс-валидацию для проверки результатов наивного байесовского клссификаторп.
 В роли метрики используйте `score.mean()`.
 3. Попробуйте выполнить атаку на байесовский фильтр, называемую [отравление Байеса](https://en.wikipedia.org/wiki/Bayesian_poisoning).
 Для этого возьмите один из spam писем из датасета и внесите в него изменения, чтобы фильтр его принял за ham.
 Как результат приведите изначальное письмо и модифицированное. Посчитайте расстояние Левенштейна между ними.
 4. Используйте `CountVectorizer` построенный на бигрммах, а затем замените его на TfidfVectorizer.
 Сравните новые классификаторы, а также проверьте их работу на модифицированном письме.
 4. Замените наивный байесовский классификатор случайным лесом. Также используйте кросс-валидациб в качестве метрики.
 5. Проверьте, как себя поведёт новый классификатор на вашм модифицированном письме.
 