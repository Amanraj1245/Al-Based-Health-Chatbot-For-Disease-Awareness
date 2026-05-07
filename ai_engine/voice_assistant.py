"""
Voice Assistant Module
Text-to-Speech and Speech-to-Text capabilities for the healthcare chatbot
Works without external APIs using browser-based Web Speech API
"""

import re
from typing import Dict, List, Optional

class VoiceAssistant:
    """Voice processing for healthcare chatbot"""
    
    def __init__(self):
        self.voice_enabled = True
        self.supported_languages = {
            'en': 'en-US',
            'hi': 'hi-IN',
            'es': 'es-ES',
            'fr': 'fr-FR',
            'de': 'de-DE',
            'zh': 'zh-CN',
            'ar': 'ar-SA'
        }
        self.voice_preferences = {}
        
    def process_voice_input(self, audio_text: str, language: str = 'en') -> Dict:
        """Process voice input and extract health information"""
        if not audio_text:
            return {
                'success': False,
                'message': 'No audio input received',
                'extracted_symptoms': [],
                'confidence': 0
            }
        
        # Clean and normalize text
        cleaned_text = self._clean_text(audio_text)
        
        # Extract symptoms from voice input
        extracted_symptoms = self._extract_symptoms_from_voice(cleaned_text, language)
        
        # Calculate confidence based on clarity
        confidence = self._calculate_voice_confidence(cleaned_text)
        
        # Detect urgency in voice
        urgency_level = self._detect_urgency(cleaned_text, language)
        
        return {
            'success': True,
            'original_text': audio_text,
            'cleaned_text': cleaned_text,
            'extracted_symptoms': extracted_symptoms,
            'confidence': confidence,
            'urgency_level': urgency_level,
            'language_detected': language
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize voice input text"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove filler words
        filler_words = ['um', 'uh', 'like', 'you know', 'so', 'actually', 'basically']
        for word in filler_words:
            text = text.replace(f' {word} ', ' ')
        
        # Fix common voice recognition errors
        corrections = {
            'head ache': 'headache',
            'tummy ache': 'stomachache',
            'belly ache': 'stomachache',
            'tummy pain': 'stomach pain',
            'chest pain': 'chest pain',
            'back ache': 'backache',
            'tooth ache': 'toothache',
            'ear ache': 'earache'
        }
        
        for wrong, correct in corrections.items():
            text = text.replace(wrong, correct)
        
        return text.strip()
    
    def _extract_symptoms_from_voice(self, text: str, language: str) -> List[str]:
        """Extract symptoms from voice input"""
        symptoms_map = {
            'en': {
                'fever': ['fever', 'high temperature', 'hot', 'burning up', 'chills'],
                'headache': ['headache', 'head pain', 'migraine', 'head hurts', 'head is pounding'],
                'cough': ['cough', 'coughing', 'dry cough', 'wet cough', 'hacking'],
                'sore_throat': ['sore throat', 'throat pain', 'scratchy throat', 'hurts to swallow'],
                'runny_nose': ['runny nose', 'stuffy nose', 'congested', 'nasal congestion'],
                'stomach_pain': ['stomach pain', 'stomachache', 'belly pain', 'abdominal pain', 'tummy hurts'],
                'nausea': ['nausea', 'nauseous', 'feel like vomiting', 'queasy', 'sick to stomach'],
                'vomiting': ['vomiting', 'throwing up', 'puking', 'vomited'],
                'diarrhea': ['diarrhea', 'loose stools', 'watery stools', 'running stomach'],
                'constipation': ['constipation', 'can\'t poop', 'hard stools', 'not going to bathroom'],
                'chest_pain': ['chest pain', 'chest hurts', 'pressure in chest', 'tight chest'],
                'shortness_of_breath': ['shortness of breath', 'can\'t breathe', 'breathless', 'gasping', 'wheezing'],
                'fatigue': ['fatigue', 'tired', 'exhausted', 'no energy', 'weak', 'lethargic'],
                'dizziness': ['dizziness', 'dizzy', 'lightheaded', 'room is spinning', 'vertigo'],
                'rash': ['rash', 'skin rash', 'red spots', 'itchy skin', 'hives'],
                'joint_pain': ['joint pain', 'arthritis', 'joints hurt', 'aching joints'],
                'muscle_pain': ['muscle pain', 'muscle ache', 'body ache', 'sore muscles'],
                'back_pain': ['back pain', 'backache', 'lower back pain', 'upper back pain'],
                'insomnia': ['insomnia', 'can\'t sleep', 'trouble sleeping', 'sleepless'],
                'anxiety': ['anxiety', 'anxious', 'worried', 'nervous', 'panic'],
                'depression': ['depression', 'depressed', 'sad', 'hopeless', 'no interest'],
                'weight_loss': ['weight loss', 'losing weight', 'getting thinner', 'not eating'],
                'weight_gain': ['weight gain', 'gaining weight', 'getting heavier', 'overeating'],
                'blurred_vision': ['blurred vision', 'can\'t see clearly', 'fuzzy vision'],
                'ear_pain': ['ear pain', 'earache', 'ear hurts', 'ear infection'],
                'tooth_pain': ['tooth pain', 'toothache', 'tooth hurts', 'dental pain']
            },
            'hi': {
                'fever': ['bukhar', 'taap', 'garmi', 'jwar'],
                'headache': ['sar dard', 'sir dard', 'matha dard'],
                'cough': ['khansi', 'kaas', 'kaasi'],
                'sore_throat': ['gale mein dard', 'gala kharab', 'gale ki kharaash'],
                'stomach_pain': ['pet dard', 'udar shool', 'pet mein dard'],
                'nausea': ['matli', 'ulti aana', 'jee machalna'],
                'vomiting': ['ulti', 'vaman', 'vomit'],
                'diarrhea': ['dast', 'paichish', 'loose motion'],
                'chest_pain': ['seene mein dard', 'chhaati dard', 'urah sthal mein peeda'],
                'shortness_of_breath': ['saans phoolna', 'saans lene mein takleef', 'dam phoolna'],
                'fatigue': ['thakaan', 'kamzori', 'aalas', 'takleef']
            }
        }
        
        detected_symptoms = []
        lang_symptoms = symptoms_map.get(language, symptoms_map['en'])
        
        for symptom, keywords in lang_symptoms.items():
            for keyword in keywords:
                if keyword in text:
                    if symptom not in detected_symptoms:
                        detected_symptoms.append(symptom)
                    break
        
        return detected_symptoms
    
    def _calculate_voice_confidence(self, text: str) -> float:
        """Calculate confidence score for voice input"""
        confidence = 0.7  # Base confidence
        
        # Increase confidence for longer, coherent text
        words = text.split()
        if len(words) >= 5:
            confidence += 0.1
        if len(words) >= 10:
            confidence += 0.1
        
        # Decrease confidence for very short input
        if len(words) < 3:
            confidence -= 0.2
        
        # Check for medical terms (indicates clearer speech)
        medical_terms = ['pain', 'symptom', 'doctor', 'medicine', 'treatment', 
                        'fever', 'headache', 'cough', 'nausea']
        found_terms = sum(1 for term in medical_terms if term in text)
        confidence += found_terms * 0.02
        
        return min(confidence, 1.0)
    
    def _detect_urgency(self, text: str, language: str) -> str:
        """Detect urgency level in voice input"""
        urgent_keywords = {
            'en': ['emergency', 'severe', 'extreme', 'unbearable', 'can\'t breathe', 
                   'chest pain', 'heart', 'unconscious', 'bleeding', '911', 'ambulance'],
            'hi': ['aatyaavashyak', ' gambhir', 'teevr', 'ghatnaaspad', 'dawa']
        }
        
        high_keywords = {
            'en': ['very bad', 'worsening', 'getting worse', 'intense', 'sharp pain',
                   'can\'t move', 'can\'t eat', 'can\'t sleep'],
            'hi': ['bahut bura', 'badhta jaa raha', 'teekha dard']
        }
        
        lang_urgent = urgent_keywords.get(language, urgent_keywords['en'])
        lang_high = high_keywords.get(language, high_keywords['en'])
        
        text_lower = text.lower()
        
        for keyword in lang_urgent:
            if keyword in text_lower:
                return 'critical'
        
        for keyword in lang_high:
            if keyword in text_lower:
                return 'high'
        
        return 'normal'
    
    def generate_voice_response(self, text: str, language: str = 'en', 
                                emotion: str = 'neutral') -> Dict:
        """Generate voice-friendly response text"""
        # Clean text for voice output
        voice_text = self._prepare_for_voice(text)
        
        # Add empathy markers based on emotion
        if emotion == 'concerned':
            voice_text = self._add_voice_empathy(voice_text, language)
        
        # Split into manageable chunks
        chunks = self._split_into_chunks(voice_text)
        
        return {
            'voice_text': voice_text,
            'chunks': chunks,
            'language': self.supported_languages.get(language, 'en-US'),
            'emotion': emotion,
            'estimated_duration': len(voice_text.split()) * 0.5  # Approximate seconds
        }
    
    def _prepare_for_voice(self, text: str) -> str:
        """Prepare text for voice output"""
        # Remove markdown and formatting
        text = re.sub(r'\*\*|__|\*|_', '', text)  # Remove bold/italic
        text = re.sub(r'`[^`]*`', '', text)  # Remove code
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # Remove links
        
        # Convert numbers to words for better TTS
        text = self._numbers_to_words(text)
        
        # Add pauses for better comprehension
        text = text.replace('. ', '. <break time="500ms"/> ')
        text = text.replace('? ', '? <break time="500ms"/> ')
        text = text.replace('! ', '! <break time="500ms"/> ')
        
        return text.strip()
    
    def _numbers_to_words(self, text: str) -> str:
        """Convert numbers to words for better speech"""
        # Simple conversion for common numbers
        number_words = {
            '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
            '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine',
            '10': 'ten', '911': 'nine one one'
        }
        
        for num, word in number_words.items():
            text = text.replace(f' {num} ', f' {word} ')
            text = text.replace(f' {num}.', f' {word}.')
        
        return text
    
    def _add_voice_empathy(self, text: str, language: str) -> str:
        """Add empathetic voice markers"""
        empathy_prefixes = {
            'en': [
                "I understand this is difficult. ",
                "I'm here to help you. ",
                "I hear your concern. "
            ],
            'hi': [
                "Main samajhta hoon ki yeh mushkil hai. ",
                "Main aapki madad ke liye yahan hoon. ",
                "Main aapki chinta samajhta hoon. "
            ]
        }
        
        prefixes = empathy_prefixes.get(language, empathy_prefixes['en'])
        import random
        return random.choice(prefixes) + text
    
    def _split_into_chunks(self, text: str, max_words: int = 30) -> List[str]:
        """Split long text into voice-friendly chunks"""
        sentences = text.split('. ')
        chunks = []
        current_chunk = []
        current_word_count = 0
        
        for sentence in sentences:
            words = sentence.split()
            if current_word_count + len(words) > max_words and current_chunk:
                chunks.append('. '.join(current_chunk) + '.')
                current_chunk = [sentence]
                current_word_count = len(words)
            else:
                current_chunk.append(sentence)
                current_word_count += len(words)
        
        if current_chunk:
            chunks.append('. '.join(current_chunk) + '.')
        
        return chunks
    
    def get_voice_commands(self, language: str = 'en') -> Dict[str, str]:
        """Get available voice commands"""
        commands = {
            'en': {
                'help': 'Say "help" for assistance',
                'emergency': 'Say "emergency" for immediate help',
                'symptoms': 'Say "my symptoms are" followed by your symptoms',
                'repeat': 'Say "repeat" to hear the last message again',
                'stop': 'Say "stop" to end voice mode',
                'book_appointment': 'Say "book appointment" to schedule a visit',
                'medicine_info': 'Say "medicine information" for drug details'
            },
            'hi': {
                'help': '"madad" boliye sahaayata ke liye',
                'emergency': 'turuant sahaayata ke liye "aapatkaaleen" boliye',
                'symptoms': 'apne lakshan bataane ke liye "mere lakshan hain" boliye'
            }
        }
        
        return commands.get(language, commands['en'])
    
    def enable_voice_mode(self, user_id: int, preferences: Dict = None) -> Dict:
        """Enable voice mode for a user"""
        self.voice_preferences[user_id] = {
            'enabled': True,
            'language': preferences.get('language', 'en') if preferences else 'en',
            'speed': preferences.get('speed', 'normal') if preferences else 'normal',
            'auto_read': preferences.get('auto_read', True) if preferences else True
        }
        
        return {
            'enabled': True,
            'message': 'Voice mode enabled. You can now speak to the chatbot.',
            'commands': self.get_voice_commands(self.voice_preferences[user_id]['language'])
        }
    
    def disable_voice_mode(self, user_id: int) -> Dict:
        """Disable voice mode for a user"""
        if user_id in self.voice_preferences:
            self.voice_preferences[user_id]['enabled'] = False
        
        return {
            'enabled': False,
            'message': 'Voice mode disabled.'
        }


# Initialize voice assistant
voice_assistant = VoiceAssistant()