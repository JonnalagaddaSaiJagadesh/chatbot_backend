from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

# Define the Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(255), nullable=False)
    bot_reply = db.Column(db.String(255), nullable=False)

# Initialize the database tables (ensure this happens within app context)
def init_db():
    with app.app_context():
        db.create_all()  # Creates database tables

# Initialize the database once, outside of route handling
init_db()

# Define a list of basic replies (expandable)
replies = {
    "hello": "Hello I'am Ryme! How can I assist you today?",
    "hi": "Hi I'am Ryme! How can I help you today?",
    "hey": "Hey there! What can I do for you?",
    "greetings": "Greetings! How can I help?",
    "your name": "I am your friendly chatbot.",
    "how are you": "I'm just a bot, but I'm doing great! How about you?",
    "thank you": "You're welcome!",
    "bye": "Goodbye! Have a great day!",
    "time": f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}",
    "current time": f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}",
    "what time": f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}",
    "date": f"Today's date is {datetime.datetime.now().strftime('%Y-%m-%d')}",
    "how old are you": "I don't have an age. I'm a bot, created to assist you!",
    "how can you help": "I can help answer your questions or perform tasks. Ask me anything!",
    "can you help me": "Of course! How can I assist you?",
    "what can you do": "I can provide information, answer questions, or just chat with you!",
    "what is your purpose": "My purpose is to assist and make your life easier. How can I help today?",
    "weather": "I am not connected to a weather service, but you can check your local weather website.",
    "how's the weather": "I cannot fetch the weather at the moment. Try checking your local weather service.",
    "tell me a joke": "Why don’t skeletons fight each other? They don’t have the guts!",
    "tell me a fact": "Did you know honey never spoils? Archaeologists found pots of honey in ancient tombs over 3,000 years old!",
    "who are you": "I'm a chatbot here to help you with your questions.",
    "tell me something interesting": "Did you know that octopuses have three hearts?",
    "how do you work": "I analyze your message, search for keywords, and reply accordingly.",
    "can you speak other languages": "I currently understand English, but I can help with basic phrases in other languages too.",
    "what is your favorite color": "I don't have preferences, but I think blue is cool!",
    "can you play games": "I can't play games, but I can tell you jokes and riddles!",
    "what is the meaning of life": "42... just kidding! The meaning of life is different for everyone.",
    "how do I start a conversation": "Just type your message, and I'll respond! What’s on your mind?",
    "how are you doing": "I'm doing great, thank you for asking! How are you?",
    "what is your purpose in life": "My purpose is to help you and make your day easier.",
    "what do you like": "I like helping people and answering questions.",
    "can you solve math problems": "I can try! Ask me a math question and I'll do my best.",
    "how to make a chatbot": "You can create a chatbot using various programming languages. Start with Python and Flask!",
    "how to learn programming": "Start with basics like Python, JavaScript, or HTML and build projects along the way!",
    "who created you": "I was created by a team of developers to help people like you.",
    "do you have feelings": "I don't have feelings, but I try to understand and respond in helpful ways.",
    "what is AI": "AI stands for Artificial Intelligence. It's technology that simulates human-like intelligence.",
    "what is machine learning": "Machine Learning is a subset of AI where systems learn from data to make decisions.",
    "do you understand me": "Yes, I can understand your messages and respond accordingly.",
    "tell me a quote": "“The only way to do great work is to love what you do.” – Steve Jobs",
    "how tall are you": "I don't have a physical form, so I don't have height.",
    "can you send emails": "I currently cannot send emails, but I can guide you on how to do that.",
    "what are your hobbies": "My hobby is to chat and help people!",
    "can you tell the future": "I can't predict the future, but I can provide you with some fun facts!",
    "do you play music": "I can't play music, but I can recommend songs!",
    "can you cook": "I can't cook, but I can give you recipes!",
    "how much is the moon worth": "The moon is priceless! But if you wanted to buy it, it would cost about $53 trillion.",
    "what is the fastest animal": "The fastest land animal is the cheetah, reaching speeds up to 70 mph.",
    "do you know a secret": "I know many facts, but no secrets! Just lots of interesting info.",
    "what is the capital of France": "The capital of France is Paris.",
    "what is 2+2": "2 + 2 = 4.",
    "what is 3*3": "3 * 3 = 9.",
    "who won the last world cup": "The last FIFA World Cup was won by France in 2018.",
    "what is Python": "Python is a popular programming language known for its simplicity and readability.",
    "can you help me with coding": "Sure! I can help you with basic coding questions.",
    "what is your favorite food": "I don’t eat food, but I imagine pizza is delicious!",
    "what time is it": f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}",
    "how many days in a year": "There are 365 days in a normal year, or 366 in a leap year.",
    "what is the longest river in the world": "The Nile River is often considered the longest river in the world.",
    "who invented the telephone": "The telephone was invented by Alexander Graham Bell.",
    "where do you live": "I don't have a physical form, so I live in the cloud!",
    "how do you understand me": "I analyze the words you use and match them with pre-programmed responses.",
    "can you dance": "I can't dance, but I can suggest some great songs to dance to!",
    "how many countries are there in the world": "There are 195 countries in the world.",
    "what is the square root of 16": "The square root of 16 is 4.",
    "how can I improve my skills": "Practice is key! Keep learning and experimenting.",
    "what is your favorite movie": "I don't watch movies, but I hear 'Inception' is really good!",
    "do you know any riddles": "Yes! Here's one: What has keys but can't open locks? A piano!",
    "how to be happy": "Focus on the positive things in life, and remember to enjoy the small moments.",
    "do you have any pets": "No, I don’t have pets. But I think cats and dogs are amazing!",
    "can you help me study": "Yes, I can help you with study tips and resources!",
    "what is the largest country in the world": "Russia is the largest country in the world by area.",
    "what is the most populated country": "China has the largest population in the world.",
    "where do I find tutorials": "You can find tutorials on platforms like YouTube, Udemy, and Coursera.",
    "how do I build a website": "You can start by learning HTML, CSS, and JavaScript. Build small projects first!",
    "do you believe in aliens": "I don’t have beliefs, but there are many theories about extraterrestrial life.",
    "what is the best programming language": "It depends on what you want to do. Python is great for beginners, while JavaScript is ideal for web development.",
    "how do I get a job": "Start by learning new skills, building your resume, and applying for jobs that match your skills.",
    "do you know any programming languages": "I understand many languages including Python, JavaScript, HTML, and CSS.",
    "can you help me with homework": "Yes, I can assist you with your homework. What subject do you need help with?",
    "what is the distance between the Earth and the Sun": "The average distance is about 93 million miles (150 million kilometers).",
    "do you like movies": "I can't watch movies, but I can recommend some!",
    "how do I become successful": "Success comes from hard work, dedication, and learning from failures.",
    "do you play chess": "I don’t play chess, but I can explain the rules and help you learn!",
    "how long is an hour": "An hour is 60 minutes.",
    "what is the best phone": "The best phone depends on your needs, but the iPhone and Samsung Galaxy are popular choices.",
    "how do you work": "I process your inputs and try to match them with my predefined answers. Pretty simple, right?",
    "do you like music": "I can’t listen to music, but I can suggest some great playlists!",
    "how do I change my password": "Visit your account settings and look for the password change option.",
    "where can I find coding challenges": "You can find coding challenges on sites like LeetCode, HackerRank, and Codewars.",
    "what is the largest planet": "Jupiter is the largest planet in our solar system.",
    "how many continents are there": "There are 7 continents on Earth.",
    "do you know the capital of Australia": "The capital of Australia is Canberra."
}

# Handling the message route
@app.route('/message', methods=['POST'])
def handle_message():
    user_message = request.json.get('message', '').strip()

    if not user_message:
        return jsonify({'reply': "I didn't understand that. Can you rephrase?"})

    # Check for matching reply
    reply = next((bot_reply for key, bot_reply in replies.items() if key in user_message.lower()), "I'm not sure how to respond to that.")

    # Save to the database
    new_message = Message(user_message=user_message, bot_reply=reply)
    db.session.add(new_message)
    db.session.commit()

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
