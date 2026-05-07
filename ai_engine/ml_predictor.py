"""
Machine Learning Predictor Module
Advanced ML-based symptom and disease prediction without external APIs
"""

import json
import math
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import random

class MLPredictor:
    """Machine Learning-based health prediction system"""
    
    def __init__(self):
        self.symptom_weights = self._initialize_symptom_weights()
        self.disease_patterns = self._load_disease_patterns()
        self.user_history_db = defaultdict(list)
        self.confidence_threshold = 0.6
        
    def _initialize_symptom_weights(self) -> Dict:
        """Initialize weighted symptom-disease relationships"""
        return {
            'fever': {
                'viral_infection': 0.8, 'flu': 0.9, 'malaria': 0.7, 
                'typhoid': 0.75, 'covid19': 0.85, 'dengue': 0.8,
                'pneumonia': 0.6, 'uti': 0.5
            },
            'headache': {
                'migraine': 0.9, 'tension_headache': 0.8, 'sinusitis': 0.7,
                'flu': 0.6, 'viral_infection': 0.5, 'high_bp': 0.65,
                'eye_strain': 0.55, 'dehydration': 0.5
            },
            'cough': {
                'common_cold': 0.8, 'bronchitis': 0.85, 'pneumonia': 0.75,
                'flu': 0.7, 'allergies': 0.6, 'asthma': 0.65,
                'covid19': 0.8, 'tb': 0.4
            },
            'chest_pain': {
                'heart_attack': 0.9, 'angina': 0.85, 'gerd': 0.6,
                'anxiety': 0.5, 'pneumonia': 0.55, 'costochondritis': 0.7,
                'muscle_strain': 0.5
            },
            'shortness_of_breath': {
                'asthma': 0.9, 'copd': 0.85, 'pneumonia': 0.75,
                'heart_failure': 0.8, 'anxiety': 0.6, 'anemia': 0.5,
                'covid19': 0.7
            },
            'fatigue': {
                'anemia': 0.8, 'thyroid': 0.75, 'diabetes': 0.7,
                'depression': 0.65, 'sleep_apnea': 0.7, 'viral_infection': 0.6,
                'chronic_fatigue': 0.85
            },
            'nausea': {
                'gastroenteritis': 0.85, 'food_poisoning': 0.8, 'migraine': 0.7,
                'pregnancy': 0.75, 'motion_sickness': 0.8, 'appendicitis': 0.6,
                'kidney_stones': 0.55
            },
            'diarrhea': {
                'gastroenteritis': 0.9, 'food_poisoning': 0.85, 'ibs': 0.7,
                'lactose_intolerance': 0.75, 'viral_infection': 0.6,
                'bacterial_infection': 0.8
            },
            'rash': {
                'allergic_reaction': 0.85, 'viral_exanthem': 0.7, 'eczema': 0.75,
                'chickenpox': 0.8, 'measles': 0.75, 'dengue': 0.7,
                'drug_reaction': 0.8
            },
            'joint_pain': {
                'arthritis': 0.9, 'gout': 0.8, 'viral_infection': 0.6,
                'lupus': 0.7, 'lyme_disease': 0.65, 'fibromyalgia': 0.75
            }
        }
    
    def _load_disease_patterns(self) -> Dict:
        """Load disease symptom patterns for pattern matching"""
        return {
            'viral_infection': {
                'symptoms': ['fever', 'fatigue', 'body_ache', 'headache'],
                'duration': '3-7 days',
                'severity': 'mild_to_moderate'
            },
            'flu': {
                'symptoms': ['fever', 'cough', 'sore_throat', 'body_ache', 'fatigue'],
                'duration': '5-10 days',
                'severity': 'moderate'
            },
            'covid19': {
                'symptoms': ['fever', 'cough', 'shortness_of_breath', 'fatigue', 'loss_of_taste'],
                'duration': '7-14 days',
                'severity': 'moderate_to_severe'
            },
            'migraine': {
                'symptoms': ['headache', 'nausea', 'sensitivity_to_light', 'visual_aura'],
                'duration': '4-72 hours',
                'severity': 'moderate_to_severe'
            },
            'gastroenteritis': {
                'symptoms': ['nausea', 'vomiting', 'diarrhea', 'stomach_cramps', 'fever'],
                'duration': '1-3 days',
                'severity': 'mild_to_moderate'
            },
            'pneumonia': {
                'symptoms': ['cough', 'fever', 'shortness_of_breath', 'chest_pain', 'fatigue'],
                'duration': '2-3 weeks',
                'severity': 'severe'
            },
            'heart_attack': {
                'symptoms': ['chest_pain', 'shortness_of_breath', 'nausea', 'sweating', 'arm_pain'],
                'duration': 'emergency',
                'severity': 'critical'
            },
            'diabetes': {
                'symptoms': ['frequent_urination', 'excessive_thirst', 'fatigue', 'blurred_vision', 'slow_healing'],
                'duration': 'chronic',
                'severity': 'variable'
            },
            'anemia': {
                'symptoms': ['fatigue', 'weakness', 'pale_skin', 'shortness_of_breath', 'dizziness'],
                'duration': 'chronic',
                'severity': 'mild_to_moderate'
            },
            'thyroid': {
                'symptoms': ['fatigue', 'weight_changes', 'temperature_sensitivity', 'mood_changes'],
                'duration': 'chronic',
                'severity': 'mild_to_moderate'
            }
        }
    
    def predict_disease(self, symptoms: List[str], user_profile: Dict = None) -> List[Dict]:
        """Predict diseases based on symptoms using ML approach"""
        if not symptoms:
            return []
        
        # Calculate disease scores
        disease_scores = defaultdict(float)
        
        for symptom in symptoms:
            if symptom in self.symptom_weights:
                for disease, weight in self.symptom_weights[symptom].items():
                    disease_scores[disease] += weight
        
        # Normalize by number of symptoms
        for disease in disease_scores:
            disease_scores[disease] /= len(symptoms)
        
        # Add pattern matching bonus
        for disease, pattern in self.disease_patterns.items():
            pattern_symptoms = set(pattern['symptoms'])
            user_symptoms = set(symptoms)
            match_ratio = len(pattern_symptoms & user_symptoms) / len(pattern_symptoms)
            disease_scores[disease] += match_ratio * 0.3
        
        # Sort by score
        sorted_diseases = sorted(disease_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Format results
        results = []
        for disease, score in sorted_diseases[:5]:  # Top 5
            if score > 0.3:  # Minimum threshold
                pattern = self.disease_patterns.get(disease, {})
                results.append({
                    'disease': disease,
                    'confidence': round(min(score, 0.99), 2),
                    'severity': pattern.get('severity', 'unknown'),
                    'duration': pattern.get('duration', 'unknown'),
                    'matching_symptoms': len(set(pattern.get('symptoms', [])) & set(symptoms)),
                    'total_symptoms': len(pattern.get('symptoms', []))
                })
        
        return results
    
    def calculate_risk_score(self, symptoms: List[str], age: int = 30, 
                            gender: str = 'unknown', duration_days: int = 1) -> Dict:
        """Calculate comprehensive health risk score"""
        base_score = 0
        risk_factors = []
        
        # Symptom severity weights
        critical_symptoms = ['chest_pain', 'shortness_of_breath', 'severe_bleeding', 
                            'loss_of_consciousness', 'paralysis']
        high_risk = ['high_fever', 'severe_headache', 'persistent_vomiting', 
                    'blood_in_stool', 'severe_dehydration']
        
        for symptom in symptoms:
            if symptom in critical_symptoms:
                base_score += 25
                risk_factors.append(f"Critical symptom: {symptom}")
            elif symptom in high_risk:
                base_score += 15
                risk_factors.append(f"High risk symptom: {symptom}")
            else:
                base_score += 5
        
        # Age factor
        if age < 5 or age > 65:
            base_score += 10
            risk_factors.append("High-risk age group")
        
        # Duration factor
        if duration_days > 7:
            base_score += 10
            risk_factors.append("Symptoms persisting > 7 days")
        elif duration_days > 3:
            base_score += 5
        
        # Gender-specific risks
        if gender == 'female' and any(s in symptoms for s in ['abdominal_pain', 'irregular_periods']):
            base_score += 3
        
        # Cap at 100
        final_score = min(base_score, 100)
        
        # Determine risk level
        if final_score >= 70:
            risk_level = 'critical'
            action = 'immediate_medical_attention'
        elif final_score >= 50:
            risk_level = 'high'
            action = 'urgent_doctor_visit'
        elif final_score >= 30:
            risk_level = 'moderate'
            action = 'schedule_appointment'
        elif final_score >= 15:
            risk_level = 'low'
            action = 'self_care_monitor'
        else:
            risk_level = 'minimal'
            action = 'maintain_healthy_lifestyle'
        
        return {
            'risk_score': final_score,
            'risk_level': risk_level,
            'recommended_action': action,
            'risk_factors': risk_factors,
            'monitoring_required': final_score >= 30
        }
    
    def predict_health_trends(self, user_id: int, days_history: int = 30) -> Dict:
        """Predict future health trends based on historical data"""
        history = self.user_history_db.get(user_id, [])
        
        if len(history) < 3:
            return {'status': 'insufficient_data'}
        
        # Analyze symptom frequency
        symptom_frequency = defaultdict(int)
        for entry in history:
            for symptom in entry.get('symptoms', []):
                symptom_frequency[symptom] += 1
        
        # Identify recurring patterns
        recurring_symptoms = {k: v for k, v in symptom_frequency.items() if v >= 3}
        
        # Predict trends
        predictions = []
        
        if 'headache' in recurring_symptoms:
            predictions.append({
                'condition': 'chronic_headache',
                'probability': 0.7,
                'recommendation': 'Consider neurological evaluation'
            })
        
        if 'fatigue' in recurring_symptoms and 'fever' in recurring_symptoms:
            predictions.append({
                'condition': 'chronic_infection_or_autoimmune',
                'probability': 0.6,
                'recommendation': 'Comprehensive blood work recommended'
            })
        
        if len(symptom_frequency) > 5:
            predictions.append({
                'condition': 'general_health_decline',
                'probability': 0.5,
                'recommendation': 'Lifestyle modification and health checkup'
            })
        
        return {
            'status': 'analysis_complete',
            'symptom_frequency': dict(symptom_frequency),
            'recurring_symptoms': list(recurring_symptoms.keys()),
            'predictions': predictions,
            'health_trajectory': 'stable' if len(predictions) < 2 else 'concerning'
        }
    
    def get_personalized_precautions(self, disease: str, user_profile: Dict) -> List[str]:
        """Get personalized precautions based on disease and user profile"""
        base_precautions = {
            'viral_infection': [
                'Rest adequately and stay hydrated',
                'Monitor temperature every 6 hours',
                'Avoid contact with others to prevent spread',
                'Eat light, nutritious meals'
            ],
            'flu': [
                'Stay home and rest for at least 5 days',
                'Drink warm fluids frequently',
                'Use mask to prevent transmission',
                'Monitor for complications'
            ],
            'covid19': [
                'Self-isolate immediately',
                'Monitor oxygen levels if possible',
                'Stay hydrated and rest',
                'Seek medical help if breathing difficulty occurs'
            ],
            'diabetes': [
                'Monitor blood sugar regularly',
                'Follow diabetic diet strictly',
                'Exercise 30 minutes daily',
                'Regular eye and foot checkups'
            ],
            'hypertension': [
                'Monitor blood pressure daily',
                'Reduce salt intake',
                'Take medications on time',
                'Practice stress management'
            ]
        }
        
        precautions = base_precautions.get(disease, ['Consult a doctor for personalized advice'])
        
        # Add age-specific precautions
        age = user_profile.get('age', 30)
        if age > 60:
            precautions.append('Extra caution advised due to age - monitor symptoms closely')
        
        return precautions
    
    def add_user_history(self, user_id: int, symptoms: List[str], diagnosis: str = None):
        """Add user health history for trend analysis"""
        self.user_history_db[user_id].append({
            'timestamp': datetime.now().isoformat(),
            'symptoms': symptoms,
            'diagnosis': diagnosis
        })
        
        # Keep only last 50 entries
        if len(self.user_history_db[user_id]) > 50:
            self.user_history_db[user_id] = self.user_history_db[user_id][-50:]
    
    def generate_health_report(self, user_id: int, current_symptoms: List[str], 
                              user_profile: Dict) -> Dict:
        """Generate comprehensive ML-based health report"""
        
        # Disease prediction
        disease_predictions = self.predict_disease(current_symptoms, user_profile)
        
        # Risk assessment
        risk_assessment = self.calculate_risk_score(
            current_symptoms,
            user_profile.get('age', 30),
            user_profile.get('gender', 'unknown'),
            user_profile.get('symptom_duration_days', 1)
        )
        
        # Trend analysis
        trend_analysis = self.predict_health_trends(user_id)
        
        # Get precautions for top predicted disease
        precautions = []
        if disease_predictions:
            top_disease = disease_predictions[0]['disease']
            precautions = self.get_personalized_precautions(top_disease, user_profile)
        
        return {
            'predicted_diseases': disease_predictions,
            'risk_assessment': risk_assessment,
            'trend_analysis': trend_analysis,
            'precautions': precautions,
            'recommendations': self._generate_recommendations(risk_assessment, trend_analysis),
            'generated_at': datetime.now().isoformat()
        }
    
    def _generate_recommendations(self, risk: Dict, trends: Dict) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        if risk['risk_level'] == 'critical':
            recommendations.extend([
                'Seek emergency medical care immediately',
                'Do not drive yourself - call ambulance or have someone take you',
                'Keep emergency contacts ready'
            ])
        elif risk['risk_level'] == 'high':
            recommendations.extend([
                'Visit a doctor within 24 hours',
                'Monitor symptoms closely',
                'Have someone check on you regularly'
            ])
        elif risk['risk_level'] == 'moderate':
            recommendations.extend([
                'Schedule a doctor appointment this week',
                'Rest and avoid strenuous activities',
                'Keep a symptom diary'
            ])
        
        if trends.get('health_trajectory') == 'concerning':
            recommendations.append('Consider comprehensive health screening')
        
        return recommendations


# Import datetime at module level
from datetime import datetime