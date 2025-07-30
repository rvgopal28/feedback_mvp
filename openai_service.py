
import openai
import os
import random

openai.api_key = os.getenv("OPENAI_API_KEY")

REPLY_TEMPLATES = {
    "Positive": [
        "Thank you so much for your kind words, {customer_name}! We're thrilled you had a great experience and hope to serve you again soon.",
        "We're so happy to hear you enjoyed your meal, {customer_name}! Your feedback made our day. Thank you!",
        "Thanks for the fantastic review, {customer_name}! We appreciate you taking the time to share your positive experience.",
    ],
    "Negative": [
        "Hello {customer_name}, we are very sorry to hear about your experience. This is not the standard we aim for, and we'd like to make things right. Please contact us at your convenience.",
        "We sincerely apologize that your experience did not meet expectations, {customer_name}. We value your feedback and will use it to improve. We hope you'll give us another chance.",
        "Thank you for bringing this to our attention, {customer_name}. We are truly sorry for the issues you faced and are looking into it immediately.",
    ]
}

def analyze_sentiment_and_get_reply(customer_name, review_text):
    prompt = f"""
    Analyze the sentiment of the following customer review.
    Respond with a single word: "Positive" or "Negative".

    Review: "{review_text}"
    Sentiment:
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5,
            temperature=0
        )
        sentiment = response.choices[0].message.content.strip()

        if sentiment not in ["Positive", "Negative"]:
            sentiment = "Negative"

    except Exception as e:
        print(f"Error in OpenAI API call: {e}")
        sentiment = "Negative"

    reply_template = random.choice(REPLY_TEMPLATES[sentiment])
    suggested_reply = reply_template.format(customer_name=customer_name)
    return sentiment, suggested_reply
