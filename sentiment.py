from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

def get_sentiment(user_message):

    try:
        result = classifier(user_message)[0]

        label = result["label"].lower()

        if "positive" in label:
            return "Positive"

        elif "negative" in label:
            return "Negative"

        else:
            return "Neutral"

    except Exception as e:
        print(e)
        return "Neutral"