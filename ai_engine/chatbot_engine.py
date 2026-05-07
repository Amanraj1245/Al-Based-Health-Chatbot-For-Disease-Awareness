"""
Conversational Chatbot Engine
Generates natural, human-like responses with empathy and context
"""

import random
from typing import Dict, List, Optional
from datetime import datetime

class ConversationalEngine:
    """Advanced conversational AI for natural health conversations"""
    
    def __init__(self):
        self.conversation_state = {}
        self.response_templates = self._load_response_templates()
        self.empathy_phrases = self._load_empathy_phrases()
        self.small_talk = self._load_small_talk()
        self.user_context = {}  # Store context about user
        self.conversation_memory = []  # Remember what was discussed
        
    def _load_response_templates(self) -> Dict:
        """Load natural conversation templates"""
        return {
            'greeting': {
                'en': [
                    "Hey there! 👋 I'm your health assistant. How are you feeling today?",
                    "Hello! Great to see you. How can I help with your health today?",
                    "Hi! I'm here to help. What's on your mind regarding your health?",
                    "Welcome! I'm your personal health companion. How are you doing?"
                ],
                'hi': [
                    "नमस्ते! 👋 मैं आपका स्वास्थ्य सहायक हूं। आज आप कैसा महसूस कर रहे हैं?",
                    "हैलो! आपसे मिलकर अच्छा लगा। मैं आपकी सेहत में कैसे मदद कर सकता हूं?",
                    "हाय! मैं यहां मदद के लिए हूं। आपके मन में सेहत को लेकर क्या चल रहा है?",
                    "स्वागत है! मैं आपका व्यक्तिगत स्वास्थ्य साथी हूं। आप कैसे हैं?"
                ]
            },
            'acknowledge_symptom': {
                'en': [
                    "I understand you're dealing with {symptom}. That sounds uncomfortable.",
                    "I'm sorry to hear you're experiencing {symptom}. Let me help you with that.",
                    "Dealing with {symptom} can be tough. I'm here to help you figure this out.",
                    "I hear you - {symptom} is definitely something we should look into."
                ],
                'hi': [
                    "मैं समझता हूं कि आप {symptom} से जूझ रहे हैं। यह असहज लगता है।",
                    "मुझे खेद है कि आपको {symptom} हो रहा है। मैं आपकी मदद करता हूं।",
                    "{symptom} से निपटना मुश्किल हो सकता है। मैं आपकी मदद के लिए यहां हूं।",
                    "मैं सुन रहा हूं - {symptom} निश्चित रूप से कुछ ऐसा है जिसे हमें देखना चाहिए।"
                ]
            },
            'ask_followup': {
                'en': [
                    "Can you tell me more about when this started?",
                    "I'd like to understand better - how long have you been feeling this way?",
                    "To help you better, could you share when you first noticed this?",
                    "When did you start experiencing these symptoms?"
                ],
                'hi': [
                    "क्या आप मुझे बता सकते हैं कि यह कब शुरू हुआ?",
                    "मैं बेहतर ढंग से समझना चाहता हूं - आप कब से ऐसा महसूस कर रहे हैं?",
                    "आपकी बेहतर मदद करने के लिए, क्या आप बता सकते हैं कि आपने पहली बार कब देखा?",
                    "आपने ये लक्षण कब से अनुभव करना शुरू किया?"
                ]
            },
            'provide_comfort': {
                'en': [
                    "Don't worry, we'll figure this out together. Many people experience this.",
                    "I know it can be concerning, but you're taking the right step by asking.",
                    "Take a deep breath. We're going to work through this together.",
                    "It's good that you're paying attention to your body. Let's see what we can do."
                ],
                'hi': [
                    "चिंता न करें, हम इसे मिलकर हल करेंगे। कई लोग इसका अनुभव करते हैं।",
                    "मुझे पता है कि यह चिंताजनक हो सकता है, लेकिन आप पूछकर सही कदम उठा रहे हैं।",
                    "गहरी सांस लें। हम इसे मिलकर पार करेंगे।",
                    "यह अच्छा है कि आप अपने शरीर पर ध्यान दे रहे हैं। देखते हैं क्या कर सकते हैं।"
                ]
            },
            'suggest_action': {
                'en': [
                    "Based on what you've told me, here's what I suggest...",
                    "Here's what might help you feel better...",
                    "Let me share some recommendations that could help...",
                    "Here's my advice based on your symptoms..."
                ],
                'hi': [
                    "आपने जो मुझे बताया है, उसके आधार पर, मैं यह सुझाव देता हूं...",
                    "यहां वह है जो आपको बेहतर महसूस करने में मदद कर सकता है...",
                    "मुझे कुछ सुझाव साझा करने दें जो मदद कर सकते हैं...",
                    "आपके लक्षणों के आधार पर यहां मेरी सलाह है..."
                ]
            },
            'closing': {
                'en': [
                    "I hope this helps! Remember, I'm always here if you need more assistance.",
                    "Take care of yourself! Feel free to come back if you have more questions.",
                    "Wishing you a speedy recovery! Don't hesitate to reach out again.",
                    "Stay healthy! I'm here anytime you need health advice."
                ],
                'hi': [
                    "मुझे उम्मीद है कि यह मदद करेगा! याद रखें, यदि आपको और सहायता चाहिए तो मैं हमेशा यहां हूं।",
                    "अपना ख्याल रखें! यदि आपके पास और प्रश्न हैं तो वापस आने में संकोच न करें।",
                    "आपके जल्द ठीक होने की कामना करता हूं! फिर से संपर्क करने में संकोच न करें।",
                    "स्वस्थ रहें! जब भी आपको स्वास्थ्य सलाह की आवश्यकता हो, मैं यहां हूं।"
                ]
            }
        }
    
    def _load_empathy_phrases(self) -> Dict:
        """Load empathy and understanding phrases"""
        return {
            'en': [
                "I understand how you feel.",
                "That must be difficult for you.",
                "I can imagine that's frustrating.",
                "You have every right to be concerned.",
                "It's completely understandable to feel this way.",
                "I'm here to support you through this."
            ],
            'hi': [
                "मैं समझता हूं कि आप कैसा महसूस कर रहे हैं।",
                "यह आपके लिए मुश्किल होगा।",
                "मैं कल्पना कर सकता हूं कि यह निराशाजनक है।",
                "आपको चिंतित होने का पूरा अधिकार है।",
                "ऐसा महसूस करना पूरी तरह से समझ में आता है।",
                "मैं इसमें आपका साथ देने के लिए यहां हूं।"
            ]
        }
    
    def _load_small_talk(self) -> Dict:
        """Load casual conversation starters"""
        return {
            'en': [
                "How's your day going so far?",
                "Have you been able to rest well lately?",
                "Is there anything else on your mind?",
                "How are you coping with everything?",
                "Have you noticed anything that makes it better or worse?"
            ],
            'hi': [
                "आपका दिन अब तक कैसा जा रहा है?",
                "क्या आप हाल ही में अच्छी तरह से आराम कर पा रहे हैं?",
                "क्या आपके मन में और कुछ है?",
                "आप सब कुछ कैसे संभाल रहे हैं?",
                "क्या आपने कुछ देखा है जो इसे बेहतर या बदतर बनाता है?"
            ]
        }
    
    def generate_response(self, context: Dict, lang: str = 'en') -> str:
        """Generate a natural, conversational response"""
        response_parts = []
        
        # Add empathy if user expressed discomfort
        if context.get('sentiment', 0) < 0:
            empathy = random.choice(self.empathy_phrases.get(lang, self.empathy_phrases['en']))
            response_parts.append(empathy)
        
        # Main response based on intent
        intent = context.get('intent', 'unknown')
        symptoms = context.get('symptoms', [])
        
        if intent == 'greeting':
            response_parts.append(self._get_template('greeting', lang))
            
        elif intent == 'symptom_check' and symptoms:
            # Acknowledge the symptom
            symptom = symptoms[0] if symptoms else 'this'
            acknowledge = self._get_template('acknowledge_symptom', lang).format(symptom=symptom)
            response_parts.append(acknowledge)
            
            # Add comfort
            response_parts.append(self._get_template('provide_comfort', lang))
            
            # Ask follow-up
            response_parts.append(self._get_template('ask_followup', lang))
            
        elif intent == 'goodbye':
            response_parts.append(self._get_template('closing', lang))
            
        else:
            # General conversational response
            if symptoms:
                symptom = symptoms[0]
                response_parts.append(
                    self._get_template('acknowledge_symptom', lang).format(symptom=symptom)
                )
            response_parts.append(self._get_template('ask_followup', lang))
        
        return ' '.join(response_parts)
    
    def _get_template(self, template_type: str, lang: str) -> str:
        """Get a random template for the given type"""
        templates = self.response_templates.get(template_type, {})
        template_list = templates.get(lang, templates.get('en', ['']))
        return random.choice(template_list) if template_list else ''
    
    def build_natural_response(self, analysis: Dict, user_message: str, 
                               conversation_history: List[Dict], lang: str = 'en') -> str:
        """Build a complete natural response like a caring doctor"""
        
        # Update context
        self._update_context(user_message, analysis)
        
        # Check conversation stage
        stage = self._determine_conversation_stage(conversation_history)
        
        response_parts = []
        
        # 1. EMOTIONAL CONNECTION - Show empathy first
        empathy = self._generate_empathy_response(analysis, lang)
        if empathy:
            response_parts.append(empathy)
        
        # 2. ACKNOWLEDGMENT - Show I understand their specific situation
        acknowledgment = self._generate_acknowledgment(analysis, user_message, lang)
        if acknowledgment:
            response_parts.append(acknowledgment)
        
        # 3. PROFESSIONAL INSIGHT - Share what I notice (like a doctor would)
        if analysis.get('symptoms'):
            insight = self._generate_doctor_insight(analysis, lang)
            response_parts.append(insight)
        
        # 4. ENGAGING QUESTIONS - Ask follow-up like a real conversation
        question = self._generate_conversational_question(analysis, stage, lang)
        if question:
            response_parts.append(question)
        
        # 5. HELPFUL SUGGESTIONS - But only when appropriate
        if stage in ['information_gathered', 'ready_for_advice'] and analysis.get('symptoms'):
            suggestions = self._generate_helpful_suggestions(analysis, lang)
            response_parts.append(suggestions)
        
        # 6. WARM CLOSING - End like a caring human
        closing = self._generate_warm_closing(stage, lang)
        if closing:
            response_parts.append(closing)
        
        return '\n\n'.join(filter(None, response_parts))
    
    def _determine_conversation_stage(self, history: List[Dict]) -> str:
        """Determine where we are in the conversation"""
        if not history:
            return 'initial'
        
        message_count = len([m for m in history if m.get('role') == 'user'])
        
        if message_count == 0:
            return 'initial'
        elif message_count == 1:
            return 'gathering_info'
        elif message_count < 4:
            return 'information_gathered'
        else:
            return 'ready_for_advice'
    
    def _generate_opening(self, analysis: Dict, lang: str) -> str:
        """Generate conversation opening"""
        templates = {
            'en': [
                "Thanks for reaching out. I want to help you feel better.",
                "I'm glad you came to me. Let's work through this together.",
                "I'm here to listen and help. Tell me more about what's going on."
            ],
            'hi': [
                "संपर्क करने के लिए धन्यवाद। मैं चाहता हूं कि आप बेहतर महसूस करें।",
                "मुझे खुशी है कि आप मेरे पास आए। आइए इसे मिलकर पार करें।",
                "मैं सुनने और मदद करने के लिए यहां हूं। मुझे बताएं क्या हो रहा है।"
            ]
        }
        return random.choice(templates.get(lang, templates['en']))
    
    def _generate_symptom_discussion(self, analysis: Dict, lang: str) -> str:
        """Generate discussion about symptoms"""
        symptoms = analysis.get('symptoms', [])
        
        if not symptoms:
            return ''
        
        if lang == 'hi':
            if len(symptoms) == 1:
                return f"आपने बताया कि आपको {symptoms[0]} है। यह कब से हो रहा है?"
            else:
                symptom_str = ', '.join(symptoms[:-1]) + f" और {symptoms[-1]}"
                return f"मैं देखता हूं कि आप {symptom_str} का अनुभव कर रहे हैं। ये सब एक साथ कब शुरू हुए?"
        else:
            if len(symptoms) == 1:
                return f"You mentioned you're experiencing {symptoms[0]}. When did this start?"
            else:
                symptom_str = ', '.join(symptoms[:-1]) + f" and {symptoms[-1]}"
                return f"I see you're dealing with {symptom_str}. When did these all start?"
    
    def _generate_suggestions(self, analysis: Dict, lang: str) -> str:
        """Generate helpful suggestions"""
        templates = {
            'en': [
                "While I'm not a doctor, here are some things that might help:",
                "Based on what you've shared, here are my thoughts:",
                "Here are some suggestions that could provide relief:"
            ],
            'hi': [
                "जबकि मैं डॉक्टर नहीं हूं, यहां कुछ चीजें हैं जो मदद कर सकती हैं:",
                "आपने जो साझा किया है उसके आधार पर, यहां मेरे विचार हैं:",
                "यहां कुछ सुझाव हैं जो राहत प्रदान कर सकते हैं:"
            ]
        }
        return random.choice(templates.get(lang, templates['en']))
    
    def _generate_next_steps(self, analysis: Dict, stage: str, lang: str) -> str:
        """Generate next steps or follow-up questions"""
        
        if stage == 'initial':
            templates = {
                'en': [
                    "Can you tell me more about how you're feeling?",
                    "I'd love to understand better - what else are you experiencing?",
                    "Help me help you - what other symptoms should I know about?"
                ],
                'hi': [
                    "क्या आप मुझे बता सकते हैं कि आप कैसा महसूस कर रहे हैं?",
                    "मैं बेहतर ढंग से समझना चाहूंगा - आप और क्या अनुभव कर रहे हैं?",
                    "मुझे आपकी मदद करने में मदद करें - मुझे किन अन्य लक्षणों के बारे में पता होना चाहिए?"
                ]
            }
        elif stage == 'gathering_info':
            templates = {
                'en': [
                    "Is there anything that makes it feel better or worse?",
                    "Have you tried anything to relieve the symptoms?",
                    "Are you taking any medications right now?"
                ],
                'hi': [
                    "क्या ऐसा कुछ है जो इसे बेहतर या बदतर महसूस कराता है?",
                    "क्या आपने लक्षणों से राहत के लिए कुछ करने की कोशिश की है?",
                    "क्या आप अभी कोई दवाइयां ले रहे हैं?"
                ]
            }
        else:
            templates = {
                'en': [
                    "Remember, if things get worse, please see a doctor. I'm here to help anytime!",
                    "I hope you feel better soon. Don't hesitate to ask if you need more help!",
                    "Take care! If you have more questions, I'm just a message away."
                ],
                'hi': [
                    "याद रखें, अगर स्थिति बिगड़ती है तो कृपया डॉक्टर से मिलें। मैं कभी भी मदद के लिए यहां हूं!",
                    "मुझे उम्मीद है कि आप जल्द ही बेहतर महसूस करेंगे। यदि आपको और मदद चाहिए तो पूछने में संकोच न करें!",
                    "अपना ख्याल रखें! यदि आपके पास और प्रश्न हैं, तो मैं केवल एक संदेश दूर हूं।"
                ]
            }
        
        return random.choice(templates.get(lang, templates['en']))
    
    def add_personality(self, response: str, lang: str = 'en') -> str:
        """Add personality touches to responses"""
        # Add occasional emoji or friendly touches
        friendly_endings = {
            'en': [' 😊', ' 👍', ' 💪', ' 🌟'],
            'hi': [' 😊', ' 👍', ' 💪', ' 🙏']
        }
        
        # 30% chance to add a friendly ending
        if random.random() < 0.3:
            endings = friendly_endings.get(lang, friendly_endings['en'])
            response += random.choice(endings)
        
        return response
    
    def _update_context(self, user_message: str, analysis: Dict):
        """Update conversation context"""
        # Store symptoms mentioned
        if analysis.get('symptoms'):
            if 'symptoms' not in self.user_context:
                self.user_context['symptoms'] = []
            for symptom in analysis['symptoms']:
                if symptom not in self.user_context['symptoms']:
                    self.user_context['symptoms'].append(symptom)
        
        # Store conversation topics
        self.conversation_memory.append({
            'message': user_message,
            'symptoms': analysis.get('symptoms', []),
            'timestamp': datetime.now()
        })
        
        # Keep only last 10 exchanges
        if len(self.conversation_memory) > 10:
            self.conversation_memory = self.conversation_memory[-10:]
    
    def _generate_empathy_response(self, analysis: Dict, lang: str) -> str:
        """Generate genuine empathetic response like a caring doctor"""
        sentiment = analysis.get('sentiment', 0)
        symptoms = analysis.get('symptoms', [])
        
        # High empathy for negative sentiment or serious symptoms
        serious_symptoms = ['chest_pain', 'shortness_of_breath', 'severe_pain', 'bleeding']
        has_serious = any(s in serious_symptoms for s in symptoms)
        
        if has_serious:
            if lang == 'hi':
                return "मुझे सुनकर खेद हो रहा है कि आप यह अनुभव कर रहे हैं। मैं आपकी मदद के लिए यहां हूं।"
            return "I'm really sorry to hear you're going through this. I want to help you get through it."
        
        if sentiment < -0.3:
            empathy_phrases = {
                'en': [
                    "I can hear that you're not feeling well, and I want you to know I care.",
                    "It sounds like you're having a rough time. I'm here to listen and help.",
                    "I understand this is frustrating. Let's work through it together.",
                    "Your health concerns are valid, and I'm here to support you."
                ],
                'hi': [
                    "मैं सुन सकता हूं कि आप ठीक नहीं महसूस कर रहे हैं, और मैं चाहता हूं कि आप जानें कि मुझे परवाह है।",
                    "ऐसा लगता है कि आप कठिन समय से गुजर रहे हैं। मैं सुनने और मदद करने के लिए यहां हूं।",
                    "मुझे पता है कि यह निराशाजनक है। आइए इसे मिलकर पार करें।",
                    "आपकी स्वास्थ्य चिंताएं वैध हैं, और मैं आपका समर्थन करने के लिए यहां हूं।"
                ]
            }
            return random.choice(empathy_phrases.get(lang, empathy_phrases['en']))
        
        # Mild empathy for general symptoms
        if symptoms:
            mild_empathy = {
                'en': [
                    "Thanks for sharing that with me.",
                    "I appreciate you telling me about this.",
                    "I'm glad you reached out about this."
                ],
                'hi': [
                    "मुझसे यह साझा करने के लिए धन्यवाद।",
                    "मैं इसके बारे में आपके बताने की सराहना करता हूं।",
                    "मुझे खुशी है कि आपने इस बारे में मुझसे संपर्क किया।"
                ]
            }
            return random.choice(mild_empathy.get(lang, mild_empathy['en']))
        
        return ""
    
    def _generate_acknowledgment(self, analysis: Dict, user_message: str, lang: str) -> str:
        """Acknowledge what the user said specifically"""
        symptoms = analysis.get('symptoms', [])
        
        if not symptoms:
            # General acknowledgment
            general_ack = {
                'en': [
                    "I hear you.",
                    "I understand.",
                    "Got it, thanks for letting me know."
                ],
                'hi': [
                    "मैं सुन रहा हूं।",
                    "मैं समझता हूं।",
                    "समझ गया, मुझे बताने के लिए धन्यवाद।"
                ]
            }
            return random.choice(general_ack.get(lang, general_ack['en']))
        
        # Specific acknowledgment with symptoms
        if lang == 'hi':
            if len(symptoms) == 1:
                acks = [
                    f"तो आप {symptoms[0]} से परेशान हैं।",
                    f"आपने बताया कि आपको {symptoms[0]} है।",
                    f"मैं समझता हूं - {symptoms[0]} काफी असहज हो सकता है।"
                ]
            else:
                symptom_str = ' और '.join(symptoms)
                acks = [
                    f"तो आप {symptom_str} जैसी कई समस्याओं का सामना कर रहे हैं।",
                    f"आपने {symptom_str} का उल्लेख किया - यह बहुत हो सकता है।"
                ]
        else:
            if len(symptoms) == 1:
                acks = [
                    f"So you're dealing with {symptoms[0]}.",
                    f"You mentioned having {symptoms[0]}.",
                    f"I understand - {symptoms[0]} can be quite uncomfortable."
                ]
            else:
                symptom_str = ', '.join(symptoms[:-1]) + f" and {symptoms[-1]}"
                acks = [
                    f"So you're dealing with several things - {symptom_str}.",
                    f"You mentioned {symptom_str} - that's a lot to handle.",
                    f"I see you're experiencing {symptom_str} together."
                ]
        
        return random.choice(acks)
    
    def _generate_doctor_insight(self, analysis: Dict, lang: str) -> str:
        """Generate insight like a doctor would share"""
        symptoms = analysis.get('symptoms', [])
        
        if not symptoms:
            return ""
        
        # Check if we've discussed these symptoms before
        previous_symptoms = self.user_context.get('symptoms', [])
        new_symptoms = [s for s in symptoms if s not in previous_symptoms[:-len(symptoms)]]
        
        if lang == 'hi':
            if new_symptoms:
                insights = [
                    "यह जानना महत्वपूर्ण है। कुछ लक्षण एक साथ हो सकते हैं जो एक पैटर्न दिखाते हैं।",
                    "मैं जो देख रहा हूं उसके आधार पर, ये लक्षण एक दूसरे से जुड़े हो सकते हैं।",
                    "यह अच्छी जानकारी है। इन लक्षणों को एक साथ समझना मदद कर सकता है।"
                ]
            else:
                insights = [
                    "इन लक्षणों को ध्यान में रखते हुए, मैं कुछ संभावनाओं पर विचार कर रहा हूं।",
                    "जो आप बता रहे हैं उसके आधार पर, मुझे कुछ विचार हैं।",
                    "यह स्थिति समझने में मदद करती है।"
                ]
        else:
            if new_symptoms:
                insights = [
                    "That's important to know. Sometimes symptoms occur together that can indicate a pattern.",
                    "Based on what I'm seeing, these symptoms could be related to each other.",
                    "This is helpful information. Understanding these symptoms together can point us in the right direction."
                ]
            else:
                insights = [
                    "Given these symptoms, I'm considering a few possibilities.",
                    "Based on what you're describing, I have some thoughts on what might be going on.",
                    "This helps me understand your situation better."
                ]
        
        return random.choice(insights)
    
    def _generate_conversational_question(self, analysis: Dict, stage: str, lang: str) -> str:
        """Generate natural follow-up questions like a real conversation"""
        symptoms = analysis.get('symptoms', [])
        
        if stage == 'initial':
            if lang == 'hi':
                questions = [
                    "क्या आप मुझे बता सकते हैं कि यह कब से शुरू हुआ?",
                    "यह पहले कभी हुआ है, या यह पहली बार है?",
                    "क्या आप इसे 1 से 10 के पैमाने पर कितना गंभीर मानेंगे?"
                ]
            else:
                questions = [
                    "Can you tell me when this started?",
                    "Has this happened to you before, or is this the first time?",
                    "On a scale of 1 to 10, how would you rate how you're feeling?",
                    "What made you decide to reach out about this today?"
                ]
        
        elif stage == 'gathering_info':
            if lang == 'hi':
                questions = [
                    "क्या कुछ ऐसा है जो इसे बेहतर या बदतर बनाता है?",
                    "क्या आपने इसे ठीक करने के लिए कुछ करने की कोशिश की है?",
                    "क्या आप कोई दवाइयां ले रहे हैं?",
                    "क्या आपके परिवार में किसी को इसी तरह की समस्या है?"
                ]
            else:
                questions = [
                    "Is there anything that seems to make it better or worse?",
                    "Have you tried anything to help with this so far?",
                    "Are you currently taking any medications?",
                    "Does anyone in your family have similar issues?"
                ]
        
        else:  # information_gathered or ready_for_advice
            if lang == 'hi':
                questions = [
                    "क्या आपको लगता है कि मैंने कुछ मिस कर दिया है जो मुझे जानना चाहिए?",
                    "इसके अलावा, क्या आपके मन में और कुछ है?",
                    "क्या आपको मेरी बताई गई जानकारी से मदद मिली?"
                ]
            else:
                questions = [
                    "Is there anything else you think I should know?",
                    "Besides what we've discussed, is there anything else on your mind?",
                    "Does what I've shared make sense to you?"
                ]
        
        return random.choice(questions)
    
    def _generate_helpful_suggestions(self, analysis: Dict, lang: str) -> str:
        """Generate helpful suggestions without being too clinical"""
        symptoms = analysis.get('symptoms', [])
        
        if not symptoms:
            return ""
        
        if lang == 'hi':
            intros = [
                "जब तक आप डॉक्टर से नहीं मिलते, यहां कुछ चीजें हैं जो मदद कर सकती हैं:",
                "मैं कुछ सुझाव देना चाहूंगा जो आपको राहत दे सकते हैं:",
                "यहां कुछ चीजें हैं जो आपको बेहतर महसूस करने में मदद कर सकती हैं:"
            ]
            
            suggestions = [
                "• बहुत सारा तरल पदार्थ पिएं और आराम करें",
                "• अपने लक्षणों पर नजर रखें और देखें कि वे कैसे बदलते हैं",
                "• यदि लक्षण बढ़ते हैं या बेहतर नहीं होते हैं, तो डॉक्टर से मिलें"
            ]
        else:
            intros = [
                "While you should see a doctor for a proper diagnosis, here are some things that might help in the meantime:",
                "I'd like to suggest a few things that could provide some relief:",
                "Here are some steps you can take that might help you feel better:"
            ]
            
            suggestions = [
                "• Make sure you're staying hydrated and getting plenty of rest",
                "• Keep track of your symptoms and notice any changes",
                "• If symptoms worsen or don't improve, please see a healthcare professional"
            ]
        
        return random.choice(intros) + "\n" + '\n'.join(suggestions)
    
    def _generate_warm_closing(self, stage: str, lang: str) -> str:
        """Generate warm, human-like closing"""
        if stage == 'initial':
            if lang == 'hi':
                return "मैं यहां हूं और सुन रहा हूं। आगे बताएं।"
            return "I'm here and I'm listening. Tell me more."
        
        elif stage == 'gathering_info':
            closings = {
                'en': [
                    "You're doing great by paying attention to your health. Let's keep going.",
                    "I appreciate you sharing this with me. It helps me understand better.",
                    "We're making progress. Thanks for being patient with the questions."
                ],
                'hi': [
                    "आप अपने स्वास्थ्य पर ध्यान देकर बहुत अच्छा कर रहे हैं। आगे बढ़ते रहें।",
                    "मैं इसे मुझसे साझा करने के लिए आपकी सराहना करता हूं। यह मुझे बेहतर ढंग से समझने में मदद करता है।",
                    "हम प्रगति कर रहे हैं। सवालों के लिए धैर्यवान रहने के लिए धन्यवाद।"
                ]
            }
        
        else:  # ready_for_advice
            closings = {
                'en': [
                    "Remember, I'm always here if you need to talk more. Take care! 💙",
                    "I hope you start feeling better soon. Don't hesitate to reach out again!",
                    "Your health is important. Please take care of yourself, and come back anytime you need support.",
                    "Wishing you a speedy recovery. I'm just a message away if you need me!"
                ],
                'hi': [
                    "याद रखें, यदि आपको और बात करने की आवश्यकता है तो मैं हमेशा यहां हूं। अपना ख्याल रखें! 💙",
                    "मुझे उम्मीद है कि आप जल्द ही बेहतर महसूस करेंगे। फिर से संपर्क करने में संकोच न करें!",
                    "आपका स्वास्थ्य महत्वपूर्ण है। कृपया अपना ख्याल रखें, और जब भी आपको सहायता की आवश्यकता हो वापस आएं।",
                    "आपके जल्द ठीक होने की कामना करता हूं। यदि आपको मेरी आवश्यकता हो तो मैं केवल एक संदेश दूर हूं!"
                ]
            }
        
        return random.choice(closings.get(lang, closings['en']))