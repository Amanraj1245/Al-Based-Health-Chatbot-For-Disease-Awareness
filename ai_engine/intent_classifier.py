"""
Intent Classification Module
Classifies user messages into different intents
"""

from typing import Dict, List, Tuple
import re

class IntentClassifier:
    """Classifies user intents for the healthcare chatbot"""
    
    def __init__(self):
        self.intents = {
            'greeting': {
                'en': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 
                       'howdy', 'greetings', 'what\'s up', 'sup'],
                'hi': ['नमस्ते', 'हैलो', 'हाय', 'सुप्रभात', 'शुभ संध्या', 'नमस्कार', 'राम राम']
            },
            'symptom_check': {
                'en': ['fever', 'headache', 'cough', 'cold', 'pain', 'ache', 'sick', 'not feeling',
                       'symptom', 'problem', 'issue', 'hurts', 'hurting', 'suffering', 'feeling',
                       'temperature', 'nausea', 'vomiting', 'dizzy', 'tired', 'weak', 'breathing'],
                'hi': ['बुखार', 'सिरदर्द', 'खांसी', 'सर्दी', 'दर्द', 'बीमार', 'तबीयत', 'समस्या',
                       'दिक्कत', 'दिक्कत', 'उल्टी', 'चक्कर', 'थकान', 'कमजोरी', 'सांस']
            },
            'medicine_inquiry': {
                'en': ['medicine', 'medication', 'drug', 'pill', 'tablet', 'syrup', 'dose', 'dosage',
                       'prescription', 'treatment', 'cure', 'remedy', 'what should i take'],
                'hi': ['दवाई', 'दवा', 'गोली', 'सिरप', 'खुराक', 'इलाज', 'उपचार', 'क्या लूं']
            },
            'appointment_booking': {
                'en': ['appointment', 'book', 'schedule', 'doctor', 'visit', 'consultation', 
                       'checkup', 'clinic', 'hospital', 'see a doctor'],
                'hi': ['अपॉइंटमेंट', 'बुक', 'डॉक्टर', 'मुलाकात', 'जांच', 'दिखाना', 'दवाखाना']
            },
            'emergency': {
                'en': ['emergency', 'urgent', 'critical', 'serious', 'severe', 'ambulance', 
                       'hospital', 'help', 'dying', 'unconscious', 'bleeding', 'attack'],
                'hi': ['आपातकाल', 'एमर्जेंसी', 'गंभीर', 'एम्बुलेंस', 'बेहोश', 'खून', 'हमला']
            },
            'health_advice': {
                'en': ['advice', 'tip', 'suggestion', 'recommendation', 'what should i do',
                       'how to', 'prevention', 'diet', 'exercise', 'healthy', 'lifestyle'],
                'hi': ['सलाह', 'सुझाव', 'क्या करूं', 'कैसे', 'रोकथाम', 'आहार', 'व्यायाम', 'स्वस्थ']
            },
            'goodbye': {
                'en': ['bye', 'goodbye', 'see you', 'take care', 'thanks', 'thank you', 'ok bye'],
                'hi': ['अलविदा', 'नमस्ते', 'धन्यवाद', 'शुक्रिया', 'ठीक है', 'बाय']
            },
            'general_question': {
                'en': ['what', 'how', 'why', 'when', 'where', 'who', 'which', 'can you', 'do you'],
                'hi': ['क्या', 'कैसे', 'क्यों', 'कब', 'कहां', 'कौन', 'कौनसा', 'क्या आप']
            }
        }
        
        # Confidence thresholds
        self.confidence_threshold = 0.3
    
    def classify(self, text: str, lang: str = 'en') -> Dict:
        """Classify the intent of a user message"""
        text_lower = text.lower()
        scores = {}
        
        for intent, keywords in self.intents.items():
            # Get keywords for the detected language, fallback to English
            intent_keywords = keywords.get(lang, keywords.get('en', []))
            
            # Calculate score based on keyword matches
            score = 0
            matched_keywords = []
            
            for keyword in intent_keywords:
                if keyword in text_lower:
                    score += 1
                    matched_keywords.append(keyword)
            
            # Normalize score
            if intent_keywords:
                scores[intent] = {
                    'score': score / len(intent_keywords),
                    'matches': matched_keywords
                }
        
        # Find the best matching intent
        if scores:
            best_intent = max(scores, key=lambda x: scores[x]['score'])
            best_score = scores[best_intent]['score']
            
            # Check if confidence is above threshold
            if best_score >= self.confidence_threshold:
                return {
                    'intent': best_intent,
                    'confidence': best_score,
                    'matches': scores[best_intent]['matches'],
                    'all_scores': scores
                }
        
        # Default to general question if no clear intent
        return {
            'intent': 'unknown',
            'confidence': 0,
            'matches': [],
            'all_scores': scores
        }
    
    def get_intent_response(self, intent: str, lang: str = 'en') -> str:
        """Get a response template for a specific intent"""
        responses = {
            'greeting': {
                'en': "Hello! I'm your AI health assistant. How can I help you today?",
                'hi': "नमस्ते! मैं आपका AI स्वास्थ्य सहायक हूं। मैं आपकी कैसे मदद कर सकता हूं?"
            },
            'symptom_check': {
                'en': "I'll help you analyze your symptoms. Please describe what you're feeling in detail.",
                'hi': "मैं आपके लक्षणों का विश्लेषण करने में मदद करूंगा। कृपया विस्तार से बताएं कि आप कैसा महसूस कर रहे हैं।"
            },
            'medicine_inquiry': {
                'en': "I can provide information about common medicines. What symptoms are you experiencing?",
                'hi': "मैं सामान्य दवाइयों के बारे में जानकारी दे सकता हूं। आप क्या लक्षण अनुभव कर रहे हैं?"
            },
            'appointment_booking': {
                'en': "I can help you book an appointment with a doctor. Would you like to see the available doctors?",
                'hi': "मैं आपको डॉक्टर के साथ अपॉइंटमेंट बुक करने में मदद कर सकता हूं। क्या आप उपलब्ध डॉक्टरों को देखना चाहेंगे?"
            },
            'emergency': {
                'en': "⚠️ This sounds serious! Please call emergency services immediately: 112 or 108 for ambulance. If you're not in immediate danger, tell me more about your symptoms.",
                'hi': "⚠️ यह गंभीर लगता है! कृपया तुरंत आपातकालीन सेवाओं को कॉल करें: एम्बुलेंस के लिए 112 या 108। यदि आप तत्काल खतरे में नहीं हैं, तो मुझे अपने लक्षणों के बारे में और बताएं।"
            },
            'health_advice': {
                'en': "I'd be happy to provide health advice. What specific area are you interested in - diet, exercise, or general wellness?",
                'hi': "मुझे स्वास्थ्य सलाह देने में खुशी होगी। आप किस विशिष्ट क्षेत्र में रुचि रखते हैं - आहार, व्यायाम, या सामान्य स्वास्थ्य?"
            },
            'goodbye': {
                'en': "Take care! If you have any health concerns in the future, feel free to ask. Stay healthy!",
                'hi': 'अपना ख्याल रखें! यदि भविष्य में आपको कोई स्वास्थ्य संबंधी चिंता है, तो पूछने में संकोच न करें। स्वस्थ रहें!'
            },
            'general_question': {
                'en': "That's a good question. Let me help you with that.",
                'hi': "यह एक अच्छा सवाल है। मुझे आपकी मदद करने दें।"
            },
            'unknown': {
                'en': "I'm not sure I understood that correctly. Could you please rephrase or tell me about any symptoms you're experiencing?",
                'hi': "मुझे यकीन नहीं है कि मैंने इसे सही तरह से समझा। कृपया इसे दोहराएं या मुझे बताएं कि आप क्या लक्षण अनुभव कर रहे हैं?"
            }
        }
        
        return responses.get(intent, responses['unknown']).get(lang, responses['unknown']['en'])
    
    def extract_follow_up_questions(self, intent: str, lang: str = 'en') -> List[str]:
        """Get follow-up questions based on intent"""
        follow_ups = {
            'symptom_check': {
                'en': [
                    "When did these symptoms start?",
                    "How severe is the pain/discomfort on a scale of 1-10?",
                    "Are you taking any medications currently?",
                    "Do you have any allergies?"
                ],
                'hi': [
                    "ये लक्षण कब शुरू हुए?",
                    "1-10 के पैमाने पर दर्द/परेशानी कितनी गंभीर है?",
                    "क्या आप वर्तमान में कोई दवाइयां ले रहे हैं?",
                    "क्या आपको कोई एलर्जी है?"
                ]
            },
            'medicine_inquiry': {
                'en': [
                    "What is your age?",
                    "Do you have any chronic conditions?",
                    "Are you pregnant or breastfeeding?"
                ],
                'hi': [
                    "आपकी उम्र क्या है?",
                    "क्या आपको कोई पुरानी बीमारी है?",
                    "क्या आप गर्भवती हैं या स्तनपान करा रही हैं?"
                ]
            }
        }
        
        return follow_ups.get(intent, {}).get(lang, [])