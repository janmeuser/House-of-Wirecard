import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import json
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")

with open('Data/mmvor_search_results.json', 'r') as json_file:
    articles = json.load(json_file)

sia = SentimentIntensityAnalyzer()

# Zähler für positive, neutrale und negative Artikel
positive_count = 0
neutral_count = 0
negative_count = 0

skandal_date = datetime.strptime("25. Juni 2020", "%d. %B %Y")
user_input = input("Möchten Sie Artikel vor oder nach dem Skandal analysieren? Geben Sie 'vor' oder 'nach' ein: ")

# iteriere durch Artikel
for article in articles:
    article_date = datetime.strptime(article['date'], '%d. %B %Y um %H:%M Uhr')

    if (user_input == 'vor' and article_date < skandal_date) or (user_input == 'nach' and article_date >= skandal_date):
        title_sentiment = sia.polarity_scores(article['title'])
        short_text_sentiment = sia.polarity_scores(article['short_text'])

        article['title_sentiment'] = title_sentiment
        article['short_text_sentiment'] = short_text_sentiment

        # Klassifiziere den Artikel basierend auf dem compound-Score
        compound_score = title_sentiment['compound'] + short_text_sentiment['compound']

        if compound_score >= 0.05:
            article['sentiment'] = 'positive'
            positive_count += 1
        elif compound_score > -0.05 and compound_score < 0.05:
            article['sentiment'] = 'neutral'
            neutral_count += 1
        else:
            article['sentiment'] = 'negative'
            negative_count += 1

# Ausgabe der Ergebnisse
print(f"Positive Artikel: {positive_count}")
print(f"Neutrale Artikel: {neutral_count}")
print(f"Negative Artikel: {negative_count}")

with open('ergebnisse.json', 'w', encoding='utf-8') as json_file:
    json.dump(articles, json_file, ensure_ascii=False, indent=2)
