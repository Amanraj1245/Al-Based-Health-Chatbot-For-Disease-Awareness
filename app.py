from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import re
from config import Config

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    if os.path.exists('.env'):
        load_dotenv()
        print("✅ Loaded environment variables from .env file")
except ImportError:
    pass  # python-dotenv not installed, skip

# Import AI Engine
from ai_engine.nlp_processor import NLPProcessor
from ai_engine.intent_classifier import IntentClassifier
from ai_engine.symptom_analyzer import SymptomAnalyzer
from ai_engine.conversation_manager import ConversationManager
from ai_engine.health_assessor import HealthAssessor
from ai_engine.recommendation_engine import RecommendationEngine
from ai_engine.chatbot_engine import ConversationalEngine
from ai_engine.ml_predictor import MLPredictor
from ai_engine.voice_assistant import voice_assistant
from ai_engine.image_analyzer import image_analyzer
from ai_engine.medication_manager import medication_manager
from ai_engine.gpt_healthcare_assistant import init_gpt_assistant, gpt_assistant
from ai_engine.medicine_database import get_medicine_database

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Initialize AI Engine Components
nlp_processor = NLPProcessor()
intent_classifier = IntentClassifier()
symptom_analyzer = SymptomAnalyzer()
conversation_manager = ConversationManager()
health_assessor = HealthAssessor()
recommendation_engine = RecommendationEngine()
conversational_engine = ConversationalEngine()
ml_predictor = MLPredictor()

# Initialize GPT Assistant (if API key is available)
gpt_enabled = False
api_key = os.getenv('OPENAI_API_KEY') or app.config.get('OPENAI_API_KEY')
if api_key and api_key != 'your-openai-api-key-here':
    try:
        init_gpt_assistant(api_key)
        gpt_enabled = True
        print("✅ GPT-4 Healthcare Assistant initialized successfully!")
    except Exception as e:
        print(f"⚠️ GPT Assistant not available: {e}")

# Store active chat sessions
active_sessions = {}

# Language translations
translations = {
    'en': {
        'home': 'Home',
        'login': 'Login',
        'register': 'Register',
        'logout': 'Logout',
        'chatbot': 'AI Chatbot',
        'symptoms': 'Symptom Checker',
        'medicines': 'Medicines',
        'appointments': 'Appointments',
        'records': 'Health Records',
        'emergency': 'Emergency',
        'health_tips': 'Health Tips',
        'history': 'Chat History',
        'welcome': 'Welcome to HealthCare Chatbot',
        'username': 'Username',
        'password': 'Password',
        'email': 'Email',
        'name': 'Full Name',
        'age': 'Age',
        'gender': 'Gender',
        'submit': 'Submit',
        'cancel': 'Cancel',
        'save': 'Save',
        'delete': 'Delete',
        'edit': 'Edit',
        'view': 'View',
        'download': 'Download',
        'upload': 'Upload',
        'search': 'Search',
        'send': 'Send',
        'type_message': 'Type your message...',
        'doctor_warning': 'Important: Please consult a doctor for proper diagnosis and treatment.',
        'emergency_call': 'Emergency Call',
        'ambulance': 'Ambulance',
        'hospital': 'Hospital',
        'book_appointment': 'Book Appointment',
        'select_date': 'Select Date',
        'select_time': 'Select Time',
        'specialty': 'Specialty',
        'doctor_name': 'Doctor Name',
        'status': 'Status',
        'pending': 'Pending',
        'confirmed': 'Confirmed',
        'completed': 'Completed',
        'cancelled': 'Cancelled',
        'file_name': 'File Name',
        'upload_date': 'Upload Date',
        'description': 'Description',
        'no_records': 'No records found',
        'chat_history': 'Chat History',
        'date': 'Date',
        'message': 'Message',
        'response': 'Response',
        'severity_low': 'Low',
        'severity_medium': 'Medium',
        'severity_high': 'High',
        'male': 'Male',
        'female': 'Female',
        'other': 'Other',
    },
    'hi': {
        'home': 'होम',
        'login': 'लॉग इन',
        'register': 'रजिस्टर',
        'logout': 'लॉग आउट',
        'chatbot': 'एआई चैटबॉट',
        'symptoms': 'लक्षण जांच',
        'medicines': 'दवाइयां',
        'appointments': 'अपॉइंटमेंट',
        'records': 'स्वास्थ्य रिकॉर्ड',
        'emergency': 'आपातकालीन',
        'health_tips': 'स्वास्थ्य सुझाव',
        'history': 'चैट इतिहास',
        'welcome': 'हेल्थकेयर चैटबॉट में आपका स्वागत है',
        'username': 'यूजरनेम',
        'password': 'पासवर्ड',
        'email': 'ईमेल',
        'name': 'पूरा नाम',
        'age': 'उम्र',
        'gender': 'लिंग',
        'submit': 'जमा करें',
        'cancel': 'रद्द करें',
        'save': 'सहेजें',
        'delete': 'हटाएं',
        'edit': 'संपादित करें',
        'view': 'देखें',
        'download': 'डाउनलोड',
        'upload': 'अपलोड',
        'search': 'खोजें',
        'send': 'भेजें',
        'type_message': 'अपना संदेश लिखें...',
        'doctor_warning': 'महत्वपूर्ण: कृपया उचित निदान और उपचार के लिए डॉक्टर से परामर्श करें।',
        'emergency_call': 'आपातकालीन कॉल',
        'ambulance': 'एम्बुलेंस',
        'hospital': 'अस्पताल',
        'book_appointment': 'अपॉइंटमेंट बुक करें',
        'select_date': 'तारीख चुनें',
        'select_time': 'समय चुनें',
        'specialty': 'विशेषज्ञता',
        'doctor_name': 'डॉक्टर का नाम',
        'status': 'स्थिति',
        'pending': 'लंबित',
        'confirmed': 'पुष्टि हुई',
        'completed': 'पूर्ण',
        'cancelled': 'रद्द',
        'file_name': 'फाइल का नाम',
        'upload_date': 'अपलोड की तारीख',
        'description': 'विवरण',
        'no_records': 'कोई रिकॉर्ड नहीं मिला',
        'chat_history': 'चैट इतिहास',
        'date': 'तारीख',
        'message': 'संदेश',
        'response': 'प्रतिक्रिया',
        'severity_low': 'कम',
        'severity_medium': 'मध्यम',
        'severity_high': 'उच्च',
        'male': 'पुरुष',
        'female': 'महिला',
        'other': 'अन्य',
    }
}

# Medical knowledge base for AI chatbot
medical_knowledge = {
    'fever': {
        'en': {
            'diseases': ['Viral Infection', 'Flu', 'Malaria', 'Typhoid', 'COVID-19'],
            'medicines': ['Paracetamol', 'Ibuprofen'],
            'severity': 'medium',
            'advice': 'Rest well, drink plenty of fluids. If fever persists for more than 3 days, consult a doctor.'
        },
        'hi': {
            'diseases': ['वायरल संक्रमण', 'फ्लू', 'मलेरिया', 'टाइफाइड', 'कोविड-19'],
            'medicines': ['पैरासिटामोल', 'इबुप्रोफेन'],
            'severity': 'medium',
            'advice': 'अच्छी तरह आराम करें, बहुत सारा तरल पदार्थ पिएं। यदि बुखार 3 दिनों से अधिक रहता है, तो डॉक्टर से परामर्श करें।'
        },
        'keywords_hi': ['bukhar', 'bukhaar', 'ताप', 'बुखार']
    },
    'headache': {
        'en': {
            'diseases': ['Tension Headache', 'Migraine', 'Sinusitis', 'Eye Strain'],
            'medicines': ['Paracetamol', 'Aspirin'],
            'severity': 'low',
            'advice': 'Take rest in a quiet, dark room. Stay hydrated. If severe or persistent, consult a doctor.'
        },
        'hi': {
            'diseases': ['तनाव सिरदर्द', 'माइग्रेन', 'साइनसाइटिस', 'आंखों की थकान'],
            'medicines': ['पैरासिटामोल', 'एस्पिरिन'],
            'severity': 'low',
            'advice': 'शांत, अंधेरे कमरे में आराम करें। हाइड्रेटेड रहें। यदि गंभीर या लगातार रहता है, तो डॉक्टर से परामर्श करें।'
        },
        'keywords_hi': ['sir dard', 'sar dard', 'सिरदर्द', 'सरदर्द']
    },
    'cough': {
        'en': {
            'diseases': ['Common Cold', 'Bronchitis', 'Allergies', 'Pneumonia'],
            'medicines': ['Cough Syrup', 'Honey', 'Warm Water Gargle'],
            'severity': 'low',
            'advice': 'Stay hydrated, use honey in warm water. If cough persists for more than a week or with blood, see a doctor.'
        },
        'hi': {
            'diseases': ['सामान्य सर्दी', 'ब्रोंकाइटिस', 'एलर्जी', 'निमोनिया'],
            'medicines': ['कफ सिरप', 'शहद', 'गर्म पानी से कुल्ला'],
            'severity': 'low',
            'advice': 'हाइड्रेटेड रहें, गर्म पानी में शहद का उपयोग करें। यदि खांसी एक सप्ताह से अधिक या खून के साथ रहती है, तो डॉक्टर से मिलें।'
        },
        'keywords_hi': ['khansi', 'kaansi', 'खांसी', 'कांसी']
    },
    'cold': {
        'en': {
            'diseases': ['Common Cold', 'Viral Infection', 'Allergies'],
            'medicines': ['Cetirizine', 'Paracetamol', 'Vitamin C'],
            'severity': 'low',
            'advice': 'Rest, drink warm fluids, and take steam inhalation.'
        },
        'hi': {
            'diseases': ['सामान्य सर्दी', 'वायरल संक्रमण', 'एलर्जी'],
            'medicines': ['सेटिरिजीन', 'पैरासिटामोल', 'विटामिन सी'],
            'severity': 'low',
            'advice': 'आराम करें, गर्म तरल पदार्थ पिएं, और भाप लें।'
        },
        'keywords_hi': ['sardi', 'zukam', 'सर्दी', 'जुकाम']
    },
    'stomach_pain': {
        'en': {
            'diseases': ['Indigestion', 'Gastritis', 'Food Poisoning', 'Appendicitis'],
            'medicines': ['Antacid', 'Meftal Spas'],
            'severity': 'medium',
            'advice': 'Avoid spicy food, drink plenty of water. If pain is severe or in lower right abdomen, seek immediate medical attention.'
        },
        'hi': {
            'diseases': ['अपच', 'गैस्ट्राइटिस', 'फूड पॉइजनिंग', 'एपेंडिसाइटिस'],
            'medicines': ['एंटासिड', 'मेफ्टाल स्पास'],
            'severity': 'medium',
            'advice': 'मसालेदार खाने से बचें, भरपूर पानी पिएं। यदि दर्द गंभीर है या निचले दाएं पेट में है, तो तुरंत चिकित्सा सहायता लें।'
        },
        'keywords_hi': ['pet dard', 'pet dard', 'पेट दर्द', 'पेट में दर्द']
    },
    'vomiting': {
        'en': {
            'diseases': ['Food Poisoning', 'Gastroenteritis', 'Motion Sickness'],
            'medicines': ['ORS', 'Domperidone'],
            'severity': 'medium',
            'advice': 'Stay hydrated with ORS. Eat light food. If vomiting persists, consult a doctor.'
        },
        'hi': {
            'diseases': ['फूड पॉइजनिंग', 'गैस्ट्रोएंटराइटिस', 'मोशन सिकनेस'],
            'medicines': ['ORS', 'डोम्पेरिडोन'],
            'severity': 'medium',
            'advice': 'ORS के साथ हाइड्रेटेड रहें। हल्का खाना खाएं। यदि उल्टी जारी रहती है, तो डॉक्टर से परामर्श करें।'
        },
        'keywords_hi': ['ulti', 'vomiting', 'उल्टी']
    },
    'diabetes': {
        'en': {
            'diseases': ['Type 1 Diabetes', 'Type 2 Diabetes'],
            'medicines': ['Metformin', 'Insulin (prescription only)'],
            'severity': 'high',
            'advice': 'Monitor blood sugar regularly. Follow diabetic diet. Consult endocrinologist for proper treatment.'
        },
        'hi': {
            'diseases': ['टाइप 1 डायबिटीज', 'टाइप 2 डायबिटीज'],
            'medicines': ['मेटफॉर्मिन', 'इंसुलिन (केवल डॉक्टर की सलाह पर)'],
            'severity': 'high',
            'advice': 'नियमित रूप से ब्लड शुगर की जांच करें। डायबिटिक डाइट का पालन करें। उचित उपचार के लिए एंडोक्रिनोलॉजिस्ट से परामर्श करें।'
        },
        'keywords_hi': ['diabetes', 'madhumeh', 'शुगर', 'मधुमेह', 'डायबिटीज']
    },
    'blood_pressure': {
        'en': {
            'diseases': ['Hypertension', 'Hypotension'],
            'medicines': ['Amlodipine', 'Losartan (prescription only)'],
            'severity': 'high',
            'advice': 'Monitor BP regularly. Reduce salt intake. Exercise regularly. Consult cardiologist.'
        },
        'hi': {
            'diseases': ['हाइपरटेंशन', 'हाइपोटेंशन'],
            'medicines': ['एम्लोडिपाइन', 'लोसार्टन (केवल डॉक्टर की सलाह पर)'],
            'severity': 'high',
            'advice': 'नियमित रूप से बीपी की जांच करें। नमक का सेवन कम करें। नियमित व्यायाम करें। कार्डियोलॉजिस्ट से परामर्श करें।'
        },
        'keywords_hi': ['bp', 'blood pressure', 'हाई बीपी', 'ब्लड प्रेशर', 'रक्तचाप']
    }
}

# Medicine database
medicines_db = {
    'paracetamol': {
        'en': {'name': 'Paracetamol', 'usage': 'Fever, mild pain', 'dosage': '500mg-1g every 4-6 hours', 'warning': 'Do not exceed 4g per day. Consult doctor if symptoms persist.'},
        'hi': {'name': 'पैरासिटामोल', 'usage': 'बुखार, हल्का दर्द', 'dosage': '500mg-1g हर 4-6 घंटे', 'warning': 'प्रतिदिन 4g से अधिक न लें। यदि लक्षण बने रहें तो डॉक्टर से परामर्श करें।'}
    },
    'ibuprofen': {
        'en': {'name': 'Ibuprofen', 'usage': 'Pain, inflammation, fever', 'dosage': '200-400mg every 4-6 hours', 'warning': 'Take with food. Avoid if you have stomach ulcers.'},
        'hi': {'name': 'इबुप्रोफेन', 'usage': 'दर्द, सूजन, बुखार', 'dosage': '200-400mg हर 4-6 घंटे', 'warning': 'खाने के साथ लें। यदि पेट में अल्सर है तो बचें।'}
    },
    'cetirizine': {
        'en': {'name': 'Cetirizine', 'usage': 'Allergies, cold, runny nose', 'dosage': '10mg once daily', 'warning': 'May cause drowsiness. Avoid driving.'},
        'hi': {'name': 'सेटिरिजीन', 'usage': 'एलर्जी, सर्दी, बहती नाक', 'dosage': '10mg दिन में एक बार', 'warning': 'नींद आ सकती है। गाड़ी चलाने से बचें।'}
    },
    'antacid': {
        'en': {'name': 'Antacid', 'usage': 'Acidity, heartburn, indigestion', 'dosage': 'As needed after meals', 'warning': 'Do not use for more than 2 weeks without doctor advice.'},
        'hi': {'name': 'एंटासिड', 'usage': 'एसिडिटी, छाती में जलन, अपच', 'dosage': 'जरूरत अनुसार खाने के बाद', 'warning': 'डॉक्टर की सलाह के बिना 2 सप्ताह से अधिक न लें।'}
    },
    'ors': {
        'en': {'name': 'ORS (Oral Rehydration Salts)', 'usage': 'Dehydration, diarrhea', 'dosage': 'Mix in clean water as per instructions', 'warning': 'Prepare fresh solution. Do not use after 24 hours.'},
        'hi': {'name': 'ORS (ओरल रिहाइड्रेशन सॉल्ट्स)', 'usage': 'डिहाइड्रेशन, दस्त', 'dosage': 'निर्देशों के अनुसार साफ पानी में मिलाएं', 'warning': 'ताजा घोल तैयार करें। 24 घंटे के बाद उपयोग न करें।'}
    }
}

# Health tips database
health_tips = {
    'diet': [
        {'en': 'Drink at least 8 glasses of water daily.', 'hi': 'रोजाना कम से कम 8 गिलास पानी पिएं।'},
        {'en': 'Eat a variety of fruits and vegetables every day.', 'hi': 'रोजाना विभिन्न प्रकार के फल और सब्जियां खाएं।'},
        {'en': 'Limit sugar and salt intake for better health.', 'hi': 'बेहतर स्वास्थ्य के लिए चीनी और नमक का सेवन सीमित करें।'},
        {'en': 'Include whole grains in your daily diet.', 'hi': 'अपने दैनिक आहार मेंwhole grains शामिल करें।'},
        {'en': 'Avoid processed and junk food.', 'hi': 'प्रोसेस्ड और जंक फूड से बचें।'}
    ],
    'exercise': [
        {'en': 'Exercise for at least 30 minutes daily.', 'hi': 'रोजाना कम से कम 30 मिनट व्यायाम करें।'},
        {'en': 'Take a 10-minute walk after meals.', 'hi': 'खाने के बाद 10 मिनट की टहलने जरूर जाएं।'},
        {'en': 'Stretch your body every morning.', 'hi': 'हर सुबह अपने शरीर को स्ट्रेच करें।'},
        {'en': 'Practice yoga for mental and physical health.', 'hi': 'मानसिक और शारीरिक स्वास्थ्य के लिए योग का अभ्यास करें।'},
        {'en': 'Take stairs instead of elevator when possible.', 'hi': 'जब भी संभव हो लिफ्ट के बजाय सीढ़ियों का उपयोग करें।'}
    ],
    'sleep': [
        {'en': 'Get 7-8 hours of sleep every night.', 'hi': 'हर रात 7-8 घंटे की नींद लें।'},
        {'en': 'Avoid using phone before bedtime.', 'hi': 'सोने से पहले फोन का उपयोग करने से बचें।'},
        {'en': 'Maintain a regular sleep schedule.', 'hi': 'नियमित नींद का समय बनाए रखें।'},
        {'en': 'Create a relaxing bedtime routine.', 'hi': 'आरामदायक सोने की दिनचर्या बनाएं।'},
        {'en': 'Keep your bedroom cool and dark for better sleep.', 'hi': 'बेहतर नींद के लिए अपने बेडरूम को ठंडा और अंधेरा रखें।'}
    ]
}

# Emergency helplines
emergency_helplines = {
    'en': [
        {'name': 'Emergency Services', 'number': '112', 'description': 'All-in-one emergency number'},
        {'name': 'Ambulance', 'number': '108', 'description': 'Free ambulance service'},
        {'name': 'Police', 'number': '100', 'description': 'Police emergency'},
        {'name': 'Fire', 'number': '101', 'description': 'Fire emergency'},
        {'name': 'Women Helpline', 'number': '1091', 'description': 'Women safety helpline'},
        {'name': 'Child Helpline', 'number': '1098', 'description': 'Child emergency helpline'},
        {'name': 'Poison Control', 'number': '1066', 'description': 'Poison emergency'},
    ],
    'hi': [
        {'name': 'आपातकालीन सेवाएं', 'number': '112', 'description': 'ऑल-इन-वन आपातकालीन नंबर'},
        {'name': 'एम्बुलेंस', 'number': '108', 'description': 'निःशुल्क एम्बुलेंस सेवा'},
        {'name': 'पुलिस', 'number': '100', 'description': 'पुलिस आपातकालीन'},
        {'name': 'अग्निशमन', 'number': '101', 'description': 'आग आपातकालीन'},
        {'name': 'महिला हेल्पलाइन', 'number': '1091', 'description': 'महिला सुरक्षा हेल्पलाइन'},
        {'name': 'बाल हेल्पलाइन', 'number': '1098', 'description': 'बाल आपातकालीन हेल्पलाइन'},
        {'name': 'विष नियंत्रण', 'number': '1066', 'description': 'विष आपातकालीन'},
    ]
}

# Doctor database
doctors_db = [
    {'id': 1, 'name': 'Dr. Rajesh Sharma', 'specialty': 'General Physician', 'experience': '15 years', 'hospital': 'City Hospital', 'timing': '9:00 AM - 5:00 PM'},
    {'id': 2, 'name': 'Dr. Priya Patel', 'specialty': 'Cardiologist', 'experience': '12 years', 'hospital': 'Heart Care Center', 'timing': '10:00 AM - 6:00 PM'},
    {'id': 3, 'name': 'Dr. Amit Kumar', 'specialty': 'Dentist', 'experience': '10 years', 'hospital': 'Smile Dental Clinic', 'timing': '9:30 AM - 7:00 PM'},
    {'id': 4, 'name': 'Dr. Sunita Gupta', 'specialty': 'Gynecologist', 'experience': '18 years', 'hospital': 'Women Wellness Center', 'timing': '10:00 AM - 4:00 PM'},
    {'id': 5, 'name': 'Dr. Vikram Singh', 'specialty': 'Orthopedic', 'experience': '14 years', 'hospital': 'Bone & Joint Hospital', 'timing': '9:00 AM - 5:00 PM'},
    {'id': 6, 'name': 'Dr. Neha Verma', 'specialty': 'Dermatologist', 'experience': '8 years', 'hospital': 'Skin Care Clinic', 'timing': '11:00 AM - 7:00 PM'},
    {'id': 7, 'name': 'Dr. Rahul Mehta', 'specialty': 'Pediatrician', 'experience': '11 years', 'hospital': 'Children Hospital', 'timing': '9:00 AM - 6:00 PM'},
    {'id': 8, 'name': 'Dr. Anjali Desai', 'specialty': 'ENT Specialist', 'experience': '13 years', 'hospital': 'ENT Care Center', 'timing': '10:00 AM - 5:00 PM'},
]

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    chat_history = db.relationship('ChatHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', backref='user', lazy=True, cascade='all, delete-orphan')
    health_records = db.relationship('HealthRecord', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(5), default='en')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)
    doctor_name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(50), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class HealthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper functions
def get_translation(key, lang='en'):
    return translations.get(lang, translations['en']).get(key, key)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def detect_language(text):
    """Detect if text contains Hindi keywords"""
    hindi_pattern = re.compile(r'[\u0900-\u097F]')
    if hindi_pattern.search(text):
        return 'hi'
    
    # Check for romanized Hindi
    text_lower = text.lower()
    for symptom_data in medical_knowledge.values():
        if 'keywords_hi' in symptom_data:
            for keyword in symptom_data['keywords_hi']:
                if keyword in text_lower:
                    return 'hi'
    return 'en'

def analyze_symptoms(message, lang='en'):
    """Analyze user message and return symptom analysis"""
    message_lower = message.lower()
    detected_symptoms = []
    
    for symptom_key, symptom_data in medical_knowledge.items():
        # Check English keywords
        if symptom_key.replace('_', ' ') in message_lower or symptom_key in message_lower:
            detected_symptoms.append((symptom_key, symptom_data))
        
        # Check Hindi keywords
        if 'keywords_hi' in symptom_data:
            for keyword in symptom_data['keywords_hi']:
                if keyword in message_lower:
                    detected_symptoms.append((symptom_key, symptom_data))
                    break
    
    if not detected_symptoms:
        if lang == 'hi':
            return {
                'found': False,
                'message': 'मुझे आपके लक्षण समझ नहीं आए। कृपया और विवरण दें जैसे कि बुखार, सिरदर्द, खांसी, आदि।'
            }
        else:
            return {
                'found': False,
                'message': 'I could not understand your symptoms. Please provide more details like fever, headache, cough, etc.'
            }
    
    # Get the first detected symptom (can be enhanced to handle multiple)
    symptom_key, symptom_data = detected_symptoms[0]
    data = symptom_data.get(lang, symptom_data['en'])
    
    return {
        'found': True,
        'symptom': symptom_key,
        'diseases': data['diseases'],
        'medicines': data['medicines'],
        'severity': data['severity'],
        'advice': data['advice']
    }

def generate_chatbot_response(message, lang='en'):
    """Generate AI chatbot response"""
    # Detect language
    detected_lang = detect_language(message)
    if detected_lang:
        lang = detected_lang
    
    # Analyze symptoms
    analysis = analyze_symptoms(message, lang)
    
    if not analysis['found']:
        return analysis['message'], lang
    
    # Build response
    if lang == 'hi':
        response = f"आपके लक्षण: {analysis['symptom'].replace('_', ' ')}\n\n"
        response += f"संभावित बीमारियां: {', '.join(analysis['diseases'])}\n\n"
        response += f"गंभीरता स्तर: {get_translation('severity_' + analysis['severity'], 'hi')}\n\n"
        response += f"सुझाई गई दवाइयां: {', '.join(analysis['medicines'])}\n\n"
        response += f"सलाह: {analysis['advice']}\n\n"
        response += "⚠️ महत्वपूर्ण: कृपया उचित निदान और उपचार के लिए डॉक्टर से परामर्श करें।"
    else:
        response = f"Your symptoms: {analysis['symptom'].replace('_', ' ')}\n\n"
        response += f"Possible conditions: {', '.join(analysis['diseases'])}\n\n"
        response += f"Severity Level: {analysis['severity'].upper()}\n\n"
        response += f"Suggested medicines: {', '.join(analysis['medicines'])}\n\n"
        response += f"Advice: {analysis['advice']}\n\n"
        response += "⚠️ Important: Please consult a doctor for proper diagnosis and treatment."
    
    return response, lang

# Routes
@app.route('/')
def index():
    lang = session.get('lang', 'en')
    return render_template('index.html', lang=lang, t=lambda k: get_translation(k, lang))

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['en', 'hi']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    lang = session.get('lang', 'en')
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        
        # Validation
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            age=int(age) if age else None,
            gender=gender
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', lang=lang, t=lambda k: get_translation(k, lang))

@app.route('/login', methods=['GET', 'POST'])
def login():
    lang = session.get('lang', 'en')
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html', lang=lang, t=lambda k: get_translation(k, lang))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/chatbot')
@login_required
def chatbot():
    lang = session.get('lang', 'en')
    return render_template('chatbot.html', lang=lang, t=lambda k: get_translation(k, lang))

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    data = request.get_json()
    message = data.get('message', '')
    lang = session.get('lang', 'en')
    
    # Get or create session for user
    user_id = current_user.id
    if user_id not in active_sessions:
        active_sessions[user_id] = conversation_manager.create_session(user_id)
    
    session_id = active_sessions[user_id]
    
    # Process message with NLP
    nlp_result = nlp_processor.preprocess(message)
    detected_lang = nlp_result['language']
    
    # Classify intent
    intent_result = intent_classifier.classify(message, detected_lang)
    intent = intent_result['intent']
    
    # Extract entities
    entities = nlp_processor.extract_entities(message)
    
    # Add user message to conversation
    conversation_manager.add_message(session_id, 'user', message, intent, entities)
    
    # Update context
    conversation_manager.update_context(session_id, {
        'current_intent': intent,
        'last_message': message
    })
    
    # Get conversation history for context
    conversation_history = conversation_manager.get_conversation_history(session_id)
    
    # Analyze sentiment for empathy
    sentiment = nlp_processor.sentiment_score(message)
    
    # Use GPT if available for ChatGPT-like experience
    if gpt_enabled and gpt_assistant:
        try:
            # Get detected symptoms for context
            analysis = symptom_analyzer.analyze_symptoms(message, detected_lang)
            
            # Get GPT response
            gpt_response = gpt_assistant.get_response(
                message, 
                current_user.id,
                detected_symptoms=analysis.get('detected_symptoms', []),
                language=detected_lang
            )
            
            if gpt_response['success']:
                response = gpt_response['response']
                
                # Add to conversation manager for context
                conversation_manager.add_message(session_id, 'assistant', response)
                
                # Save to chat history
                chat = ChatHistory(
                    user_id=current_user.id,
                    message=message,
                    response=response,
                    language=detected_lang
                )
                db.session.add(chat)
                db.session.commit()
                
                return jsonify({
                    'response': response,
                    'language': detected_lang,
                    'intent': intent,
                    'sentiment': sentiment,
                    'gpt_enabled': True,
                    'ml_predictions': None
                })
        except Exception as e:
            print(f"GPT error: {e}")
            # Fall back to rule-based response
    
    # Generate AI response based on intent using conversational engine (fallback)
    if intent == 'greeting':
        response = conversational_engine.generate_response(
            {'intent': 'greeting', 'sentiment': sentiment}, 
            detected_lang
        )
        
    elif intent == 'goodbye':
        response = conversational_engine.generate_response(
            {'intent': 'goodbye', 'sentiment': sentiment}, 
            detected_lang
        )
        
    elif intent == 'emergency':
        response = intent_classifier.get_intent_response('emergency', detected_lang)
        
    elif intent == 'appointment_booking':
        response = intent_classifier.get_intent_response('appointment_booking', detected_lang)
        
    elif intent == 'health_advice':
        # Get personalized recommendations with conversational tone
        user_profile = {
            'age': current_user.age,
            'gender': current_user.gender,
            'activity_level': 'moderate'
        }
        recommendations = recommendation_engine.get_personalized_recommendations(user_profile, detected_lang)
        
        # Build natural response
        context = {
            'intent': 'health_advice',
            'sentiment': sentiment,
            'recommendations': recommendations
        }
        response = conversational_engine.build_natural_response(
            context, message, conversation_history, detected_lang
        )
        
    elif intent == 'symptom_check' or intent == 'medicine_inquiry':
        # Use advanced symptom analyzer
        analysis = symptom_analyzer.analyze_symptoms(message, detected_lang)
        
        # Add detected symptoms to context
        for symptom in analysis['detected_symptoms']:
            conversation_manager.add_detected_symptom(session_id, symptom)
        
        # Build conversational context
        context = {
            'intent': 'symptom_check',
            'symptoms': analysis['detected_symptoms'],
            'sentiment': sentiment,
            'requires_doctor': analysis['requires_doctor']
        }
        
        # Generate natural conversational response
        response = conversational_engine.build_natural_response(
            context, message, conversation_history, detected_lang
        )
        
        # Add specific medical information if symptoms detected (but keep it conversational)
        if analysis['detected_symptoms']:
            medical_info = symptom_analyzer.generate_response(analysis, detected_lang)
            # Only add medical info if user seems ready for it (after some conversation)
            if len(conversation_history) >= 3:
                response += "\n\n" + medical_info
        
        # Set follow-up questions if needed
        if analysis['requires_doctor']:
            follow_ups = intent_classifier.extract_follow_up_questions('symptom_check', detected_lang)
            conversation_manager.set_follow_up_questions(session_id, follow_ups)
            
    else:
        # Check if there are pending follow-up questions
        next_question = conversation_manager.get_next_follow_up(session_id)
        if next_question:
            response = next_question
            conversation_manager.remove_follow_up(session_id)
        else:
            # Default conversational response
            analysis = symptom_analyzer.analyze_symptoms(message, detected_lang)
            context = {
                'intent': 'unknown',
                'symptoms': analysis['detected_symptoms'],
                'sentiment': sentiment
            }
            response = conversational_engine.build_natural_response(
                context, message, conversation_history, detected_lang
            )
            
            # Add medical info if symptoms found (only after some conversation)
            if analysis['detected_symptoms'] and len(conversation_history) >= 3:
                medical_info = symptom_analyzer.generate_response(analysis, detected_lang)
                response += "\n\n" + medical_info
    
    # Add assistant response to conversation
    conversation_manager.add_message(session_id, 'assistant', response)
    
    # Check if should escalate to human
    should_escalate = conversation_manager.should_escalate(session_id)
    
    # ML-based predictions if symptoms detected
    ml_predictions = None
    if analysis.get('detected_symptoms'):
        user_profile = {
            'age': current_user.age or 30,
            'gender': current_user.gender or 'unknown',
            'symptom_duration_days': 1
        }
        ml_predictions = ml_predictor.generate_health_report(
            current_user.id,
            analysis['detected_symptoms'],
            user_profile
        )
        
        # Add to user history for trend analysis
        ml_predictor.add_user_history(
            current_user.id,
            analysis['detected_symptoms'],
            ml_predictions['predicted_diseases'][0]['disease'] if ml_predictions['predicted_diseases'] else None
        )
    
    # Save to chat history
    chat = ChatHistory(
        user_id=current_user.id,
        message=message,
        response=response,
        language=detected_lang
    )
    db.session.add(chat)
    db.session.commit()
    
    return jsonify({
        'response': response,
        'language': detected_lang,
        'intent': intent,
        'sentiment': sentiment,
        'escalate': should_escalate,
        'session_summary': conversation_manager.get_conversation_summary(session_id),
        'ml_predictions': ml_predictions
    })

@app.route('/symptoms')
@login_required
def symptoms():
    lang = session.get('lang', 'en')
    return render_template('symptoms.html', lang=lang, t=lambda k: get_translation(k, lang), medical_knowledge=medical_knowledge)

@app.route('/medicines')
@login_required
def medicines():
    lang = session.get('lang', 'en')
    return render_template('medicines_new.html', lang=lang, t=lambda k: get_translation(k, lang))

@app.route('/api/medicines', methods=['GET'])
@login_required
def api_medicines():
    """Get medicine database"""
    medicines = get_medicine_database()
    return jsonify({'medicines': medicines})

@app.route('/appointments', methods=['GET', 'POST'])
@login_required
def appointments():
    lang = session.get('lang', 'en')
    
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        notes = request.form.get('notes')
        
        doctor = next((d for d in doctors_db if str(d['id']) == doctor_id), None)
        
        if doctor:
            from datetime import datetime as dt
            appointment = Appointment(
                user_id=current_user.id,
                doctor_id=doctor['id'],
                doctor_name=doctor['name'],
                specialty=doctor['specialty'],
                appointment_date=dt.strptime(appointment_date, '%Y-%m-%d').date(),
                appointment_time=dt.strptime(appointment_time, '%H:%M').time(),
                notes=notes
            )
            db.session.add(appointment)
            db.session.commit()
            
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('appointments'))
    
    user_appointments = Appointment.query.filter_by(user_id=current_user.id).order_by(Appointment.appointment_date.desc()).all()
    return render_template('appointments.html', lang=lang, t=lambda k: get_translation(k, lang), 
                          doctors=doctors_db, appointments=user_appointments)

@app.route('/records', methods=['GET', 'POST'])
@login_required
def records():
    lang = session.get('lang', 'en')
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected!', 'error')
            return redirect(url_for('records'))
        
        file = request.files['file']
        description = request.form.get('description', '')
        
        if file.filename == '':
            flash('No file selected!', 'error')
            return redirect(url_for('records'))
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            unique_filename = timestamp + filename
            
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            record = HealthRecord(
                user_id=current_user.id,
                filename=unique_filename,
                original_filename=filename,
                description=description
            )
            db.session.add(record)
            db.session.commit()
            
            flash('File uploaded successfully!', 'success')
        else:
            flash('Invalid file type!', 'error')
        
        return redirect(url_for('records'))
    
    user_records = HealthRecord.query.filter_by(user_id=current_user.id).order_by(HealthRecord.upload_date.desc()).all()
    return render_template('records.html', lang=lang, t=lambda k: get_translation(k, lang), records=user_records)

@app.route('/download/<int:record_id>')
@login_required
def download_record(record_id):
    record = HealthRecord.query.get_or_404(record_id)
    
    if record.user_id != current_user.id:
        flash('Access denied!', 'error')
        return redirect(url_for('records'))
    
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], record.filename, 
                              as_attachment=True, download_name=record.original_filename)

@app.route('/delete_record/<int:record_id>', methods=['POST'])
@login_required
def delete_record(record_id):
    record = HealthRecord.query.get_or_404(record_id)
    
    if record.user_id != current_user.id:
        flash('Access denied!', 'error')
        return redirect(url_for('records'))
    
    # Delete file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], record.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    db.session.delete(record)
    db.session.commit()
    
    flash('Record deleted successfully!', 'success')
    return redirect(url_for('records'))

@app.route('/emergency')
def emergency():
    lang = session.get('lang', 'en')
    helplines = emergency_helplines.get(lang, emergency_helplines['en'])
    return render_template('emergency.html', lang=lang, t=lambda k: get_translation(k, lang), helplines=helplines)

@app.route('/health_tips')
def health_tips_page():
    lang = session.get('lang', 'en')
    return render_template('health_tips.html', lang=lang, t=lambda k: get_translation(k, lang), tips=health_tips)

@app.route('/history')
@login_required
def chat_history():
    lang = session.get('lang', 'en')
    history = ChatHistory.query.filter_by(user_id=current_user.id).order_by(ChatHistory.timestamp.desc()).all()
    return render_template('history.html', lang=lang, t=lambda k: get_translation(k, lang), history=history)

@app.route('/api/check_symptoms', methods=['POST'])
def api_check_symptoms():
    data = request.get_json()
    symptoms_text = data.get('symptoms', '')
    lang = data.get('lang', session.get('lang', 'en'))
    
    # Use advanced symptom analyzer
    analysis = symptom_analyzer.analyze_symptoms(symptoms_text, lang)
    
    # Format response for frontend
    response = {
        'found': len(analysis['detected_symptoms']) > 0,
        'symptoms': analysis['detected_symptoms'],
        'diseases': [d['name'].get(lang, d['name']['en']) for d in analysis['possible_diseases'][:3]],
        'severity': analysis['severity_scores'].get(analysis['detected_symptoms'][0], 'low') if analysis['detected_symptoms'] else 'low',
        'medicines': [],
        'advice': '',
        'requires_doctor': analysis['requires_doctor']
    }
    
    # Get medicine names
    for med in analysis['medicines']:
        response['medicines'].extend(med['otc'])
    
    # Get advice
    if analysis['possible_diseases']:
        top_disease = analysis['possible_diseases'][0]
        response['advice'] = top_disease['description'].get(lang, top_disease['description']['en'])
    
    return jsonify(response)

@app.route('/api/health_assessment', methods=['POST'])
@login_required
def api_health_assessment():
    """Advanced health assessment endpoint"""
    data = request.get_json()
    lang = data.get('lang', session.get('lang', 'en'))
    
    # Get user profile
    user_profile = {
        'age': current_user.age or 30,
        'gender': current_user.gender or 'unknown',
        'weight': data.get('weight'),
        'height': data.get('height'),
        'symptom_duration_days': data.get('duration', 1)
    }
    
    # Get symptoms
    symptoms = data.get('symptoms', [])
    
    # Get vitals if provided
    vitals = data.get('vitals', {})
    
    # Generate comprehensive health report
    report = health_assessor.generate_health_report(user_profile, symptoms, vitals)
    
    return jsonify(report)

@app.route('/api/bmi_calculator', methods=['POST'])
def api_bmi_calculator():
    """BMI calculation endpoint"""
    data = request.get_json()
    weight = float(data.get('weight', 0))
    height = float(data.get('height', 0))
    
    if weight > 0 and height > 0:
        result = health_assessor.calculate_bmi(weight, height)
        return jsonify(result)
    
    return jsonify({'error': 'Invalid input'}), 400

@app.route('/api/recommendations', methods=['POST'])
@login_required
def api_recommendations():
    """Get personalized recommendations"""
    data = request.get_json()
    lang = data.get('lang', session.get('lang', 'en'))
    
    user_profile = {
        'age': current_user.age or 30,
        'gender': current_user.gender,
        'activity_level': data.get('activity_level', 'moderate'),
        'health_goal': data.get('goal', 'balanced'),
        'smoker': data.get('smoker', False),
        'stress_level': data.get('stress_level', 'low')
    }
    
    recommendations = recommendation_engine.get_personalized_recommendations(user_profile, lang)
    return jsonify(recommendations)

@app.route('/api/conversation_stats', methods=['GET'])
@login_required
def api_conversation_stats():
    """Get conversation statistics"""
    user_id = current_user.id
    
    if user_id in active_sessions:
        session_id = active_sessions[user_id]
        stats = conversation_manager.analyze_conversation_flow(session_id)
        return jsonify(stats)
    
    return jsonify({'error': 'No active session'}), 404

@app.route('/api/ml_health_check', methods=['POST'])
@login_required
def api_ml_health_check():
    """Get ML-based health analysis"""
    data = request.get_json()
    symptoms = data.get('symptoms', [])
    duration = data.get('duration', 1)
    severity = data.get('severity', 5)
    
    if not symptoms:
        return jsonify({'error': 'No symptoms provided'}), 400
    
    user_profile = {
        'age': current_user.age or 30,
        'gender': current_user.gender or 'unknown',
        'symptom_duration_days': duration
    }
    
    # Generate comprehensive health report
    report = ml_predictor.generate_health_report(
        current_user.id,
        symptoms,
        user_profile
    )
    
    return jsonify(report)

@app.route('/api/user_health_stats', methods=['GET'])
@login_required
def api_user_health_stats():
    """Get user's health statistics"""
    # Get total chats
    total_chats = ChatHistory.query.filter_by(user_id=current_user.id).count()
    
    # Get unique symptoms tracked
    user_chats = ChatHistory.query.filter_by(user_id=current_user.id).all()
    all_symptoms = set()
    for chat in user_chats:
        # Simple extraction - in production, store symptoms separately
        msg_lower = chat.message.lower()
        common_symptoms = ['fever', 'headache', 'cough', 'pain', 'nausea', 'fatigue', 
                          'dizziness', 'rash', 'vomiting', 'diarrhea']
        for symptom in common_symptoms:
            if symptom in msg_lower:
                all_symptoms.add(symptom)
    
    # Get ML insights count
    insights_count = len(ml_predictor.user_history_db.get(current_user.id, []))
    
    # Get latest ML predictions if available
    latest_predictions = None
    if current_user.id in ml_predictor.user_history_db and ml_predictor.user_history_db[current_user.id]:
        last_entry = ml_predictor.user_history_db[current_user.id][-1]
        if last_entry.get('symptoms'):
            user_profile = {
                'age': current_user.age or 30,
                'gender': current_user.gender or 'unknown',
                'symptom_duration_days': 1
            }
            latest_predictions = ml_predictor.generate_health_report(
                current_user.id,
                last_entry['symptoms'],
                user_profile
            )
    
    # Calculate health score based on various factors
    health_score = 85  # Base score
    if all_symptoms:
        health_score -= min(len(all_symptoms) * 5, 30)  # Reduce for symptoms
    if insights_count > 5:
        health_score -= 5  # Slight reduction for frequent issues
    health_score = max(health_score, 50)  # Minimum 50
    
    return jsonify({
        'total_chats': total_chats,
        'symptoms_tracked': len(all_symptoms),
        'ai_insights': insights_count,
        'health_score': health_score,
        'ml_predictions': latest_predictions
    })

@app.route('/ai_dashboard')
@login_required
def ai_dashboard():
    """AI Health Dashboard"""
    lang = session.get('lang', 'en')
    return render_template('ai_dashboard.html', lang=lang, t=lambda k: get_translation(k, lang))

@app.route('/image_analysis')
@login_required
def image_analysis():
    """Image Analysis Page"""
    lang = session.get('lang', 'en')
    return render_template('image_analysis.html', lang=lang, t=lambda k: get_translation(k, lang))

@app.route('/medications')
@login_required
def medications():
    """Medication Manager Page"""
    lang = session.get('lang', 'en')
    return render_template('medications.html', lang=lang, t=lambda k: get_translation(k, lang))

@app.route('/api/add_medication', methods=['POST'])
@login_required
def api_add_medication():
    """Add a new medication"""
    data = request.get_json()
    result = medication_manager.add_medication(current_user.id, data)
    return jsonify(result)

@app.route('/api/my_medications', methods=['GET'])
@login_required
def api_my_medications():
    """Get user's medications"""
    medications = medication_manager.get_medications(current_user.id)
    return jsonify({'medications': medications})

@app.route('/api/today_schedule', methods=['GET'])
@login_required
def api_today_schedule():
    """Get today's medication schedule"""
    schedule = medication_manager.get_todays_schedule(current_user.id)
    return jsonify({'schedule': schedule})

@app.route('/api/mark_dose_taken', methods=['POST'])
@login_required
def api_mark_dose_taken():
    """Mark a medication dose as taken"""
    data = request.get_json()
    result = medication_manager.mark_dose_taken(
        current_user.id,
        data['medication_id'],
        data['time']
    )
    return jsonify(result)

@app.route('/api/adherence_stats', methods=['GET'])
@login_required
def api_adherence_stats():
    """Get medication adherence statistics"""
    stats = medication_manager.get_adherence_stats(current_user.id)
    return jsonify(stats)

@app.route('/api/refill_reminders', methods=['GET'])
@login_required
def api_refill_reminders():
    """Get refill reminders"""
    reminders = medication_manager.get_refill_reminders(current_user.id)
    return jsonify({'reminders': reminders})

@app.route('/api/delete_medication', methods=['POST'])
@login_required
def api_delete_medication():
    """Delete a medication"""
    data = request.get_json()
    result = medication_manager.delete_medication(current_user.id, data['medication_id'])
    return jsonify(result)

@app.route('/api/analyze_image', methods=['POST'])
@login_required
def api_analyze_image():
    """Analyze uploaded health image"""
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    analysis_type = request.form.get('analysis_type', 'general')
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    # Save temporarily
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f'temp_{current_user.id}_{file.filename}')
    file.save(temp_path)
    
    try:
        # Analyze image
        result = image_analyzer.analyze_image(temp_path, analysis_type)
        
        # Clean up temp file
        os.remove(temp_path)
        
        return jsonify(result)
        
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/compare_images', methods=['POST'])
@login_required
def api_compare_images():
    """Compare two images for changes"""
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({'success': False, 'error': 'Both images required'}), 400
    
    file1 = request.files['image1']
    file2 = request.files['image2']
    
    # Save temporarily
    temp_path1 = os.path.join(app.config['UPLOAD_FOLDER'], f'temp1_{current_user.id}_{file1.filename}')
    temp_path2 = os.path.join(app.config['UPLOAD_FOLDER'], f'temp2_{current_user.id}_{file2.filename}')
    
    file1.save(temp_path1)
    file2.save(temp_path2)
    
    try:
        # Compare images
        result = image_analyzer.compare_images(temp_path1, temp_path2)
        
        # Clean up
        os.remove(temp_path1)
        os.remove(temp_path2)
        
        return jsonify(result)
        
    except Exception as e:
        if os.path.exists(temp_path1):
            os.remove(temp_path1)
        if os.path.exists(temp_path2):
            os.remove(temp_path2)
        return jsonify({'success': False, 'error': str(e)}), 500

# Cleanup old sessions periodically
@app.before_request
def cleanup_sessions():
    """Cleanup old sessions before each request"""
    conversation_manager.cleanup_old_sessions(max_age_hours=24)

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
