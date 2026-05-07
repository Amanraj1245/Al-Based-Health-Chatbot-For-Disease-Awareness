"""
Advanced Symptom Analysis Module
Uses machine learning-like approach for symptom-disease matching
"""

from typing import Dict, List, Tuple, Optional
import json
import os

class SymptomAnalyzer:
    """Advanced symptom analyzer with comprehensive medical knowledge"""
    
    def __init__(self):
        self.symptoms_db = self._load_symptoms_database()
        self.disease_db = self._load_disease_database()
        self.medicine_db = self._load_medicine_database()
    
    def _load_symptoms_database(self) -> Dict:
        """Load comprehensive symptom database"""
        return {
            'fever': {
                'keywords': {
                    'en': ['fever', 'temperature', 'hot', 'burning', 'febrile', 'pyrexia'],
                    'hi': ['bukhar', 'bukhaar', 'ताप', 'बुखार', 'गर्मी', 'ज्वर']
                },
                'severity_indicators': {
                    'low': ['mild', 'slight', 'low grade', '99', '100'],
                    'medium': ['moderate', '101', '102', 'high'],
                    'high': ['severe', 'very high', '103', '104', '105', 'dangerous']
                }
            },
            'headache': {
                'keywords': {
                    'en': ['headache', 'head pain', 'migraine', 'sinus', 'tension headache'],
                    'hi': ['sir dard', 'sar dard', 'सिरदर्द', 'सरदर्द', 'माइग्रेन', 'आधासीसी']
                },
                'severity_indicators': {
                    'low': ['mild', 'slight', 'dull', 'tolerable'],
                    'medium': ['moderate', 'throbbing', 'persistent'],
                    'high': ['severe', 'excruciating', 'unbearable', 'worst']
                }
            },
            'cough': {
                'keywords': {
                    'en': ['cough', 'coughing', 'dry cough', 'wet cough', 'chest congestion'],
                    'hi': ['khansi', 'kaansi', 'खांसी', 'कांसी', 'सूखी खांसी']
                },
                'severity_indicators': {
                    'low': ['occasional', 'mild', 'few times'],
                    'medium': ['frequent', 'persistent', 'disturbing sleep'],
                    'high': ['continuous', 'with blood', 'severe', 'can\'t breathe']
                }
            },
            'cold': {
                'keywords': {
                    'en': ['cold', 'runny nose', 'stuffy nose', 'nasal congestion', 'sneezing'],
                    'hi': ['sardi', 'zukam', 'सर्दी', 'जुकाम', 'नाक बहना', 'छींक']
                },
                'severity_indicators': {
                    'low': ['mild', 'slight', 'occasional'],
                    'medium': ['moderate', 'frequent sneezing', 'blocked nose'],
                    'high': ['severe', 'completely blocked', 'with fever']
                }
            },
            'stomach_pain': {
                'keywords': {
                    'en': ['stomach pain', 'abdominal pain', 'belly ache', 'tummy pain', 'gastric'],
                    'hi': ['pet dard', 'pet me dard', 'पेट दर्द', 'पेट में दर्द', 'गैस', 'गैस्ट्रिक']
                },
                'severity_indicators': {
                    'low': ['mild', 'discomfort', 'bloating'],
                    'medium': ['moderate pain', 'cramping', 'persistent'],
                    'high': ['severe', 'sharp pain', 'appendix', 'can\'t move']
                }
            },
            'vomiting': {
                'keywords': {
                    'en': ['vomiting', 'nausea', 'throwing up', 'sick', 'queasy'],
                    'hi': ['ulti', 'vomiting', 'उल्टी', 'मतली', 'जी मिचलाना']
                },
                'severity_indicators': {
                    'low': ['nausea', 'feeling sick', 'once'],
                    'medium': ['vomited 2-3 times', 'can\'t eat'],
                    'high': ['continuous', 'with blood', 'dehydrated']
                }
            },
            'diarrhea': {
                'keywords': {
                    'en': ['diarrhea', 'loose motion', 'loose stools', 'frequent stools'],
                    'hi': ['dast', 'दस्त', 'पतला दस्त', 'पेट खराब']
                },
                'severity_indicators': {
                    'low': ['1-2 times', 'mild'],
                    'medium': ['3-4 times', 'watery'],
                    'high': ['more than 5 times', 'with blood', 'severe dehydration']
                }
            },
            'body_pain': {
                'keywords': {
                    'en': ['body pain', 'body ache', 'muscle pain', 'joint pain', 'weakness'],
                    'hi': ['badan dard', 'sharir dard', 'बदन दर्द', 'शरीर दर्द', 'जोड़ों का दर्द']
                },
                'severity_indicators': {
                    'low': ['mild', 'tired', 'fatigue'],
                    'medium': ['moderate', 'difficulty moving', 'aching'],
                    'high': ['severe', 'can\'t walk', 'excruciating']
                }
            },
            'sore_throat': {
                'keywords': {
                    'en': ['sore throat', 'throat pain', 'painful swallowing', 'hoarseness'],
                    'hi': ['galay me dard', 'गले में दर्द', 'गला खराब', 'आवाज बैठना']
                },
                'severity_indicators': {
                    'low': ['scratchy', 'mild irritation'],
                    'medium': ['painful', 'difficulty swallowing'],
                    'high': ['severe pain', 'can\'t swallow', 'with high fever']
                }
            },
            'breathing': {
                'keywords': {
                    'en': ['breathing difficulty', 'shortness of breath', 'chest tightness', 'wheezing'],
                    'hi': ['saans lene me dikkat', 'सांस लेने में दिक्कत', 'सांस फूलना', 'घरघराहट']
                },
                'severity_indicators': {
                    'low': ['slight difficulty', 'after exertion'],
                    'medium': ['moderate', 'at rest', 'tightness'],
                    'high': ['severe', 'can\'t breathe', 'blue lips']
                }
            }
        }
    
    def _load_disease_database(self) -> Dict:
        """Load disease-symptom mapping"""
        return {
            'viral_fever': {
                'name': {'en': 'Viral Fever', 'hi': 'वायरल बुखार'},
                'symptoms': ['fever', 'body_pain', 'headache', 'weakness'],
                'severity': 'medium',
                'description': {
                    'en': 'Common viral infection causing fever and body aches',
                    'hi': 'बुखार और शरीर दर्द causing सामान्य वायरल संक्रमण'
                }
            },
            'common_cold': {
                'name': {'en': 'Common Cold', 'hi': 'सामान्य सर्दी'},
                'symptoms': ['cold', 'sore_throat', 'cough', 'mild_fever'],
                'severity': 'low',
                'description': {
                    'en': 'Mild viral infection of upper respiratory tract',
                    'hi': 'ऊपरी श्वसन पथ का हल्का वायरल संक्रमण'
                }
            },
            'influenza': {
                'name': {'en': 'Influenza (Flu)', 'hi': 'इन्फ्लूएंजा (फ्लू)'},
                'symptoms': ['fever', 'body_pain', 'headache', 'cough', 'weakness'],
                'severity': 'medium',
                'description': {
                    'en': 'Viral infection more severe than common cold',
                    'hi': 'सामान्य सर्दी से अधिक गंभीर वायरल संक्रमण'
                }
            },
            'gastroenteritis': {
                'name': {'en': 'Gastroenteritis', 'hi': 'गैस्ट्रोएंटराइटिस'},
                'symptoms': ['stomach_pain', 'vomiting', 'diarrhea', 'fever'],
                'severity': 'medium',
                'description': {
                    'en': 'Stomach and intestinal infection',
                    'hi': 'पेट और आंतों का संक्रमण'
                }
            },
            'migraine': {
                'name': {'en': 'Migraine', 'hi': 'माइग्रेन'},
                'symptoms': ['headache', 'nausea', 'sensitivity_to_light'],
                'severity': 'medium',
                'description': {
                    'en': 'Severe headache often with nausea and light sensitivity',
                    'hi': 'गंभीर सिरदर्द, अक्सर मतली और रोशनी के प्रति संवेदनशीलता के साथ'
                }
            },
            'bronchitis': {
                'name': {'en': 'Bronchitis', 'hi': 'ब्रोंकाइटिस'},
                'symptoms': ['cough', 'chest_congestion', 'mild_fever', 'breathing'],
                'severity': 'medium',
                'description': {
                    'en': 'Inflammation of bronchial tubes',
                    'hi': 'श्वासनली की सूजन'
                }
            },
            'pneumonia': {
                'name': {'en': 'Pneumonia', 'hi': 'निमोनिया'},
                'symptoms': ['fever', 'cough', 'breathing', 'chest_pain', 'fatigue'],
                'severity': 'high',
                'description': {
                    'en': 'Serious lung infection requiring medical attention',
                    'hi': 'गंभीर फेफड़ों का संक्रमण, चिकित्सा ध्यान की आवश्यकता'
                }
            },
            'food_poisoning': {
                'name': {'en': 'Food Poisoning', 'hi': 'फूड पॉइजनिंग'},
                'symptoms': ['vomiting', 'diarrhea', 'stomach_pain', 'fever'],
                'severity': 'medium',
                'description': {
                    'en': 'Illness caused by contaminated food',
                    'hi': 'दूषित भोजन से होने वाली बीमारी'
                }
            },
            'covid19': {
                'name': {'en': 'COVID-19', 'hi': 'कोविड-19'},
                'symptoms': ['fever', 'cough', 'breathing', 'loss_of_taste', 'fatigue'],
                'severity': 'high',
                'description': {
                    'en': 'Viral respiratory infection caused by SARS-CoV-2',
                    'hi': 'SARS-CoV-2 द्वारा caused वायरल श्वसन संक्रमण'
                }
            },
            'dengue': {
                'name': {'en': 'Dengue Fever', 'hi': 'डेंगू बुखार'},
                'symptoms': ['high_fever', 'body_pain', 'headache', 'rash', 'bleeding'],
                'severity': 'high',
                'description': {
                    'en': 'Mosquito-borne viral infection',
                    'hi': 'मच्छर से फैलने वाला वायरल संक्रमण'
                }
            },
            'malaria': {
                'name': {'en': 'Malaria', 'hi': 'मलेरिया'},
                'symptoms': ['fever', 'chills', 'sweating', 'headache', 'body_pain'],
                'severity': 'high',
                'description': {
                    'en': 'Mosquito-borne parasitic disease',
                    'hi': 'मच्छर से फैलने वाला परजीवी रोग'
                }
            },
            'typhoid': {
                'name': {'en': 'Typhoid Fever', 'hi': 'टाइफाइड बुखार'},
                'symptoms': ['prolonged_fever', 'stomach_pain', 'headache', 'weakness', 'loss_of_appetite'],
                'severity': 'high',
                'description': {
                    'en': 'Bacterial infection caused by Salmonella typhi',
                    'hi': 'साल्मोनेला टाइफी द्वारा caused जीवाणु संक्रमण'
                }
            }
        }
    
    def _load_medicine_database(self) -> Dict:
        """Load medicine recommendations"""
        return {
            'fever': {
                'otc': ['Paracetamol', 'Ibuprofen'],
                'dosage': {'en': '500mg-1g every 4-6 hours', 'hi': '500mg-1g हर 4-6 घंटे'},
                'warning': {'en': 'Do not exceed 4g per day', 'hi': 'प्रतिदिन 4g से अधिक न लें'}
            },
            'headache': {
                'otc': ['Paracetamol', 'Aspirin', 'Ibuprofen'],
                'dosage': {'en': 'As needed, max 3-4 times daily', 'hi': 'आवश्यकतानुसार, अधिकतम 3-4 बार प्रतिदिन'},
                'warning': {'en': 'Avoid if you have stomach ulcers', 'hi': 'यदि पेट में अल्सर है तो बचें'}
            },
            'cough': {
                'otc': ['Cough Syrup', 'Honey', 'Warm Water Gargle'],
                'dosage': {'en': 'As per syrup instructions', 'hi': 'सिरप निर्देशों के अनुसार'},
                'warning': {'en': 'Consult doctor if persists > 1 week', 'hi': '1 सप्ताह से अधिक रहने पर डॉक्टर से परामर्श करें'}
            },
            'cold': {
                'otc': ['Cetirizine', 'Paracetamol', 'Vitamin C'],
                'dosage': {'en': 'Once daily or as needed', 'hi': 'दिन में एक बार या आवश्यकतानुसार'},
                'warning': {'en': 'May cause drowsiness', 'hi': 'नींद आ सकती है'}
            },
            'stomach_pain': {
                'otc': ['Antacid', 'Meftal Spas'],
                'dosage': {'en': 'After meals as needed', 'hi': 'खाने के बाद आवश्यकतानुसार'},
                'warning': {'en': 'Avoid spicy food', 'hi': 'मसालेदार खाने से बचें'}
            },
            'vomiting': {
                'otc': ['ORS', 'Domperidone'],
                'dosage': {'en': 'ORS after every loose motion', 'hi': 'हर पतले दस्त के बाद ORS'},
                'warning': {'en': 'Stay hydrated', 'hi': 'हाइड्रेटेड रहें'}
            },
            'diarrhea': {
                'otc': ['ORS', 'Loperamide'],
                'dosage': {'en': 'ORS frequently, Loperamide as directed', 'hi': 'बार-बार ORS, निर्देशानुसार लोपेरामाइड'},
                'warning': {'en': 'Seek help if blood in stool', 'hi': 'मल में खून होने पर सहायता लें'}
            },
            'body_pain': {
                'otc': ['Paracetamol', 'Ibuprofen', 'Hot Compress'],
                'dosage': {'en': 'Every 6-8 hours as needed', 'hi': 'आवश्यकतानुसार हर 6-8 घंटे'},
                'warning': {'en': 'Rest adequately', 'hi': 'पर्याप्त आराम करें'}
            }
        }
    
    def analyze_symptoms(self, text: str, lang: str = 'en') -> Dict:
        """Analyze symptoms from user text"""
        text_lower = text.lower()
        detected_symptoms = []
        severity_scores = {}
        
        # Detect symptoms
        for symptom_id, symptom_data in self.symptoms_db.items():
            keywords = symptom_data['keywords'].get(lang, symptom_data['keywords']['en'])
            
            for keyword in keywords:
                if keyword in text_lower:
                    detected_symptoms.append(symptom_id)
                    
                    # Assess severity
                    severity = self._assess_severity(text_lower, symptom_data['severity_indicators'])
                    severity_scores[symptom_id] = severity
                    break
        
        # Match diseases
        possible_diseases = self._match_diseases(detected_symptoms)
        
        # Get medicine recommendations
        medicines = self._get_medicines(detected_symptoms, lang)
        
        return {
            'detected_symptoms': list(set(detected_symptoms)),
            'severity_scores': severity_scores,
            'possible_diseases': possible_diseases,
            'medicines': medicines,
            'requires_doctor': self._requires_doctor(detected_symptoms, severity_scores)
        }
    
    def _assess_severity(self, text: str, indicators: Dict) -> str:
        """Assess symptom severity from text"""
        for severity, keywords in indicators.items():
            for keyword in keywords:
                if keyword in text:
                    return severity
        return 'low'  # Default
    
    def _match_diseases(self, symptoms: List[str]) -> List[Dict]:
        """Match symptoms to possible diseases"""
        matches = []
        
        for disease_id, disease_data in self.disease_db.items():
            disease_symptoms = disease_data['symptoms']
            matching = set(symptoms).intersection(set(disease_symptoms))
            
            if matching:
                match_score = len(matching) / len(disease_symptoms)
                matches.append({
                    'id': disease_id,
                    'name': disease_data['name'],
                    'severity': disease_data['severity'],
                    'description': disease_data['description'],
                    'match_score': match_score,
                    'matching_symptoms': list(matching)
                })
        
        # Sort by match score
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        return matches[:5]  # Top 5 matches
    
    def _get_medicines(self, symptoms: List[str], lang: str) -> List[Dict]:
        """Get medicine recommendations for symptoms"""
        medicines = []
        
        for symptom in symptoms:
            if symptom in self.medicine_db:
                med_data = self.medicine_db[symptom]
                medicines.append({
                    'symptom': symptom,
                    'otc': med_data['otc'],
                    'dosage': med_data['dosage'].get(lang, med_data['dosage']['en']),
                    'warning': med_data['warning'].get(lang, med_data['warning']['en'])
                })
        
        return medicines
    
    def _requires_doctor(self, symptoms: List[str], severities: Dict) -> bool:
        """Determine if doctor consultation is required"""
        high_severity_symptoms = ['breathing', 'chest_pain', 'severe_headache', 'bleeding']
        
        # Check for high severity
        for symptom, severity in severities.items():
            if severity == 'high':
                return True
        
        # Check for critical symptoms
        for symptom in symptoms:
            if symptom in high_severity_symptoms:
                return True
        
        # Check for multiple symptoms
        if len(symptoms) >= 4:
            return True
        
        return False
    
    def generate_response(self, analysis: Dict, lang: str = 'en') -> str:
        """Generate AI response based on analysis"""
        if not analysis['detected_symptoms']:
            if lang == 'hi':
                return "मुझे आपके लक्षण समझ नहीं आए। कृपया और विवरण दें जैसे कि बुखार, सिरदर्द, खांसी आदि।"
            return "I couldn't understand your symptoms. Please provide more details like fever, headache, cough, etc."
        
        response_parts = []
        
        # Detected symptoms
        if lang == 'hi':
            response_parts.append(f"**पहचाने गए लक्षण:** {', '.join(analysis['detected_symptoms'])}")
        else:
            response_parts.append(f"**Detected Symptoms:** {', '.join(analysis['detected_symptoms'])}")
        
        # Possible diseases
        if analysis['possible_diseases']:
            if lang == 'hi':
                response_parts.append("\n**संभावित बीमारियां:**")
            else:
                response_parts.append("\n**Possible Conditions:**")
            
            for disease in analysis['possible_diseases'][:3]:
                name = disease['name'].get(lang, disease['name']['en'])
                desc = disease['description'].get(lang, disease['description']['en'])
                response_parts.append(f"• {name} ({disease['severity']}) - {desc}")
        
        # Medicine recommendations
        if analysis['medicines']:
            if lang == 'hi':
                response_parts.append("\n**सुझाई गई दवाइयां (OTC):**")
            else:
                response_parts.append("\n**Suggested Medicines (OTC):**")
            
            for med in analysis['medicines']:
                response_parts.append(f"• {', '.join(med['otc'])}")
                response_parts.append(f"  Dosage: {med['dosage']}")
                response_parts.append(f"  ⚠️ {med['warning']}")
        
        # Doctor consultation warning
        if analysis['requires_doctor']:
            if lang == 'hi':
                response_parts.append("\n🚨 **महत्वपूर्ण:** आपकी स्थिति गंभीर लगती है। कृपया तुरंत डॉक्टर से परामर्श करें।")
            else:
                response_parts.append("\n🚨 **Important:** Your condition appears serious. Please consult a doctor immediately.")
        else:
            if lang == 'hi':
                response_parts.append("\n⚠️ **ध्यान दें:** उचित निदान और उपचार के लिए कृपया डॉक्टर से परामर्श करें।")
            else:
                response_parts.append("\n⚠️ **Note:** Please consult a doctor for proper diagnosis and treatment.")
        
        return '\n'.join(response_parts)