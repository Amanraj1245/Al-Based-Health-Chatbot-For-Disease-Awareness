"""
Natural Language Processing Module
Handles text preprocessing, tokenization, and language detection
"""

import re
import string
from typing import List, Dict, Tuple
from collections import Counter

class NLPProcessor:
    """Advanced NLP processor for medical text analysis"""
    
    def __init__(self):
        self.hindi_pattern = re.compile(r'[\u0900-\u097F]')
        self.word_pattern = re.compile(r'\b\w+\b')
        
        # Medical stopwords in English and Hindi
        self.stopwords = {
            'en': {'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
                   'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
                   'must', 'shall', 'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
                   'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during',
                   'before', 'after', 'above', 'below', 'between', 'under', 'and', 'but', 'or',
                   'yet', 'so', 'if', 'because', 'although', 'though', 'while', 'where', 'when',
                   'that', 'which', 'who', 'whom', 'whose', 'what', 'this', 'these', 'those',
                   'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
                   'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
                   'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
                   'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
                   'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being'},
            'hi': {'का', 'की', 'के', 'में', 'से', 'को', 'ने', 'पर', 'है', 'हैं', 'था', 'थी',
                   'थे', 'और', 'या', 'लेकिन', 'क्योंकि', 'जब', 'तब', 'कि', 'जो', 'सब',
                   'सभी', 'यह', 'वह', 'ये', 'वो', 'मैं', 'मुझे', 'मेरा', 'मेरी', 'मेरे',
                   'तुम', 'तुझे', 'तुम्हारा', 'आप', 'आपका', 'हम', 'हमें', 'हमारा', 'वो',
                   'उसे', 'उसका', 'उसकी', 'उसके', 'वे', 'उन्हें', 'उनका', 'उनकी', 'उनके'}
        }
        
        # Stemming rules
        self.suffixes = {
            'en': ['ing', 'ly', 'ed', 'ies', 'ied', 'ies', 'ied', 's', 'es'],
            'hi': ['कर', 'ाएंगे', 'ाएगा', 'ाओगे', 'ाओ', 'आएं', 'ाए', 'ाऊंगा', 'ाऊंगी']
        }
    
    def detect_language(self, text: str) -> str:
        """Detect if text is English or Hindi"""
        if self.hindi_pattern.search(text):
            return 'hi'
        return 'en'
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        return self.word_pattern.findall(text.lower())
    
    def remove_stopwords(self, tokens: List[str], lang: str = 'en') -> List[str]:
        """Remove stopwords from token list"""
        stop_words = self.stopwords.get(lang, self.stopwords['en'])
        return [token for token in tokens if token not in stop_words]
    
    def stem(self, word: str, lang: str = 'en') -> str:
        """Simple stemming algorithm"""
        suffix_list = self.suffixes.get(lang, [])
        for suffix in suffix_list:
            if word.endswith(suffix):
                return word[:-len(suffix)]
        return word
    
    def preprocess(self, text: str) -> Dict:
        """Full preprocessing pipeline"""
        lang = self.detect_language(text)
        tokens = self.tokenize(text)
        tokens_clean = self.remove_stopwords(tokens, lang)
        stems = [self.stem(token, lang) for token in tokens_clean]
        
        return {
            'original': text,
            'language': lang,
            'tokens': tokens,
            'tokens_clean': tokens_clean,
            'stems': stems,
            'word_count': len(tokens),
            'unique_words': len(set(tokens))
        }
    
    def extract_entities(self, text: str) -> List[Dict]:
        """Extract medical entities from text"""
        entities = []
        
        # Number extraction (age, temperature, etc.)
        numbers = re.findall(r'\b(\d+)\s*(years?|months?|days?|degree|°C|°F|mg|ml|%)\b', text, re.IGNORECASE)
        for num, unit in numbers:
            entities.append({
                'type': 'measurement',
                'value': num,
                'unit': unit,
                'text': f"{num} {unit}"
            })
        
        # Time patterns
        time_patterns = re.findall(r'\b(\d+)\s*(hours?|hrs?|minutes?|mins?|days?|weeks?|months?)\b', text, re.IGNORECASE)
        for num, unit in time_patterns:
            entities.append({
                'type': 'duration',
                'value': num,
                'unit': unit,
                'text': f"{num} {unit}"
            })
        
        return entities
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts"""
        tokens1 = set(self.tokenize(text1.lower()))
        tokens2 = set(self.tokenize(text2.lower()))
        
        if not tokens1 or not tokens2:
            return 0.0
        
        intersection = tokens1.intersection(tokens2)
        return len(intersection) / (len(tokens1) * len(tokens2)) ** 0.5
    
    def extract_keywords(self, text: str, top_n: int = 5) -> List[Tuple[str, int]]:
        """Extract top keywords from text"""
        processed = self.preprocess(text)
        word_freq = Counter(processed['tokens_clean'])
        return word_freq.most_common(top_n)
    
    def sentiment_score(self, text: str) -> float:
        """Simple sentiment analysis (-1 to 1)"""
        positive_words = {'good', 'better', 'great', 'excellent', 'happy', 'relieved', 'fine', 
                         'comfortable', 'relaxed', 'peaceful', 'accha', 'बढ़िया', 'अच्छा'}
        negative_words = {'bad', 'worse', 'terrible', 'pain', 'hurt', 'sad', 'worried', 'anxious',
                         'uncomfortable', 'severe', 'critical', 'bura', 'खराब', 'दर्द', 'चिंता'}
        
        tokens = set(self.tokenize(text.lower()))
        
        pos_count = len(tokens.intersection(positive_words))
        neg_count = len(tokens.intersection(negative_words))
        
        total = pos_count + neg_count
        if total == 0:
            return 0.0
        
        return (pos_count - neg_count) / total
    
    def normalize_text(self, text: str) -> str:
        """Normalize text for better matching"""
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Remove punctuation except for medical symbols
        text = re.sub(r'[^\w\s\.\-\°\%]', ' ', text)
        return text.strip()