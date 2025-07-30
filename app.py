
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

from openai_service import analyze_sentiment_and_get_reply
from email_service import send_email_notification

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    sentiment = db.Column(db.String(20), nullable=False)
    suggested_reply = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Review {self.id} by {self.customer_name}>'

@app.route('/webhook/review', methods=['POST'])
def handle_review_webhook():
    data = request.json
    if not data or 'customer_name' not in data or 'review_text' not in data:
        return jsonify({"error": "Invalid payload. Missing 'customer_name' or 'review_text'."}), 400

    customer_name = data['customer_name']
    review_text = data['review_text']
    rating = data.get('rating', None)

    sentiment, suggested_reply = analyze_sentiment_and_get_reply(customer_name, review_text)

    new_review = Review(
        customer_name=customer_name,
        review_text=review_text,
        rating=rating,
        sentiment=sentiment,
        suggested_reply=suggested_reply
    )
    db.session.add(new_review)
    db.session.commit()

    email_data = {
        "customer_name": customer_name,
        "review_text": review_text,
        "rating": rating,
        "sentiment": sentiment,
        "suggested_reply": suggested_reply
    }
    send_email_notification(email_data)

    return jsonify({
        "message": "Review processed successfully",
        "review_id": new_review.id,
        "sentiment": sentiment
    }), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
else:
    with app.app_context():
        db.create_all()
