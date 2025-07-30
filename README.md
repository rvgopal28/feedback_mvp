
# Hybrid MVP Feedback System

## Features
- Flask API with modular architecture
- SQLAlchemy ORM for database handling
- OpenAI GPT-3.5 Turbo for sentiment analysis
- Email notifications with rich formatting (MIMEMultipart)
- `.env` config management

## Setup Instructions
1. Clone the project and navigate into the directory.
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Create a `.env` file based on `.env.example` and fill in your credentials.
4. Run the Flask app:
```
python app.py
```
5. Test the API using:
```
python test_webhook.py
```
