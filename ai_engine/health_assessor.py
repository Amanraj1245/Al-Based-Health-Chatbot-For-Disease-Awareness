"""
Health Risk Assessment Module
Assesses health risks based on symptoms and user profile
"""

from typing import Dict, List, Optional
from datetime import datetime

class HealthAssessor:
    """Assesses health risks and provides recommendations"""
    
    def __init__(self):
        self.risk_factors = self._load_risk_factors()
        self.vital_signs_ranges = self._load_vital_signs_ranges()
    
    def _load_risk_factors(self) -> Dict:
        """Load health risk factors"""
        return {
            'age': {
                'child': (0, 12),
                'teen': (13, 19),
                'adult': (20, 59),
                'senior': (60, 150)
            },
            'bmi': {
                'underweight': (0, 18.5),
                'normal': (18.5, 24.9),
                'overweight': (25, 29.9),
                'obese': (30, 100)
            },
            'blood_pressure': {
                'normal': (90, 120),
                'elevated': (120, 129),
                'high_stage1': (130, 139),
                'high_stage2': (140, 180)
            }
        }
    
    def _load_vital_signs_ranges(self) -> Dict:
        """Load normal ranges for vital signs"""
        return {
            'temperature': {
                'normal': (36.1, 37.2),
                'fever': (37.3, 38.0),
                'high_fever': (38.1, 41.0)
            },
            'heart_rate': {
                'normal': (60, 100),
                'bradycardia': (0, 59),
                'tachycardia': (101, 200)
            },
            'respiratory_rate': {
                'normal': (12, 20),
                'bradypnea': (0, 11),
                'tachypnea': (21, 60)
            },
            'oxygen_saturation': {
                'normal': (95, 100),
                'mild_hypoxemia': (90, 94),
                'severe_hypoxemia': (0, 89)
            }
        }
    
    def calculate_bmi(self, weight_kg: float, height_cm: float) -> Dict:
        """Calculate BMI and return category"""
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        if bmi < 18.5:
            category = 'underweight'
            risk = 'medium'
        elif bmi < 25:
            category = 'normal'
            risk = 'low'
        elif bmi < 30:
            category = 'overweight'
            risk = 'medium'
        else:
            category = 'obese'
            risk = 'high'
        
        return {
            'bmi': round(bmi, 1),
            'category': category,
            'risk_level': risk,
            'recommendations': self._get_bmi_recommendations(category)
        }
    
    def _get_bmi_recommendations(self, category: str) -> List[str]:
        """Get recommendations based on BMI category"""
        recommendations = {
            'underweight': [
                'Increase calorie intake with nutritious foods',
                'Eat more protein-rich foods',
                'Consider strength training exercises',
                'Consult a nutritionist'
            ],
            'normal': [
                'Maintain your current lifestyle',
                'Continue balanced diet',
                'Regular exercise 30 minutes daily',
                'Annual health checkups'
            ],
            'overweight': [
                'Reduce calorie intake gradually',
                'Increase physical activity',
                'Choose whole grains over refined carbs',
                'Monitor portion sizes'
            ],
            'obese': [
                'Consult a healthcare provider',
                'Create a weight loss plan',
                'Consider joining a support group',
                'Monitor for related health conditions'
            ]
        }
        return recommendations.get(category, [])
    
    def assess_symptom_severity(self, symptoms: List[str], duration_days: int,
                                 age: int = None) -> Dict:
        """Assess overall severity of symptoms"""
        severity_score = 0
        risk_factors = []
        
        # Critical symptoms (high weight)
        critical_symptoms = ['chest_pain', 'breathing_difficulty', 'severe_bleeding', 
                            'unconsciousness', 'severe_headache', 'paralysis']
        
        # Moderate symptoms
        moderate_symptoms = ['fever', 'persistent_cough', 'vomiting', 'diarrhea',
                            'severe_pain']
        
        for symptom in symptoms:
            if symptom in critical_symptoms:
                severity_score += 10
                risk_factors.append(f"Critical symptom: {symptom}")
            elif symptom in moderate_symptoms:
                severity_score += 5
                risk_factors.append(f"Moderate symptom: {symptom}")
            else:
                severity_score += 2
        
        # Factor in duration
        if duration_days > 7:
            severity_score += 3
            risk_factors.append("Symptoms persisting > 7 days")
        elif duration_days > 3:
            severity_score += 1
        
        # Factor in age
        if age:
            if age < 5 or age > 65:
                severity_score += 3
                risk_factors.append("High-risk age group")
        
        # Determine overall severity
        if severity_score >= 15:
            overall_severity = 'high'
            action = 'immediate_medical_attention'
        elif severity_score >= 8:
            overall_severity = 'medium'
            action = 'schedule_appointment'
        else:
            overall_severity = 'low'
            action = 'self_care_monitor'
        
        return {
            'severity_score': severity_score,
            'overall_severity': overall_severity,
            'recommended_action': action,
            'risk_factors': risk_factors,
            'monitoring_required': overall_severity != 'low'
        }
    
    def check_vital_signs(self, vitals: Dict) -> Dict:
        """Check vital signs against normal ranges"""
        abnormalities = []
        
        # Check temperature
        if 'temperature' in vitals:
            temp = vitals['temperature']
            if temp > 38.0:
                abnormalities.append({
                    'parameter': 'temperature',
                    'value': temp,
                    'status': 'high_fever',
                    'severity': 'high'
                })
            elif temp > 37.2:
                abnormalities.append({
                    'parameter': 'temperature',
                    'value': temp,
                    'status': 'fever',
                    'severity': 'medium'
                })
        
        # Check heart rate
        if 'heart_rate' in vitals:
            hr = vitals['heart_rate']
            if hr > 100:
                abnormalities.append({
                    'parameter': 'heart_rate',
                    'value': hr,
                    'status': 'tachycardia',
                    'severity': 'medium'
                })
            elif hr < 60:
                abnormalities.append({
                    'parameter': 'heart_rate',
                    'value': hr,
                    'status': 'bradycardia',
                    'severity': 'medium'
                })
        
        # Check oxygen saturation
        if 'oxygen_saturation' in vitals:
            spo2 = vitals['oxygen_saturation']
            if spo2 < 90:
                abnormalities.append({
                    'parameter': 'oxygen_saturation',
                    'value': spo2,
                    'status': 'severe_hypoxemia',
                    'severity': 'high'
                })
            elif spo2 < 95:
                abnormalities.append({
                    'parameter': 'oxygen_saturation',
                    'value': spo2,
                    'status': 'mild_hypoxemia',
                    'severity': 'medium'
                })
        
        return {
            'abnormalities_found': len(abnormalities) > 0,
            'abnormalities': abnormalities,
            'requires_attention': any(a['severity'] == 'high' for a in abnormalities)
        }
    
    def generate_health_report(self, user_data: Dict, symptoms: List[str],
                                vitals: Dict = None) -> Dict:
        """Generate a comprehensive health report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'user_profile': user_data,
            'symptoms': symptoms,
            'assessments': {}
        }
        
        # BMI assessment if data available
        if 'weight' in user_data and 'height' in user_data:
            report['assessments']['bmi'] = self.calculate_bmi(
                user_data['weight'], user_data['height']
            )
        
        # Symptom severity assessment
        duration = user_data.get('symptom_duration_days', 1)
        age = user_data.get('age')
        report['assessments']['symptoms'] = self.assess_symptom_severity(
            symptoms, duration, age
        )
        
        # Vital signs check
        if vitals:
            report['assessments']['vitals'] = self.check_vital_signs(vitals)
        
        # Overall risk assessment
        report['overall_risk'] = self._calculate_overall_risk(report['assessments'])
        
        # Recommendations
        report['recommendations'] = self._generate_recommendations(report)
        
        return report
    
    def _calculate_overall_risk(self, assessments: Dict) -> str:
        """Calculate overall risk level"""
        risk_scores = []
        
        if 'symptoms' in assessments:
            severity = assessments['symptoms']['overall_severity']
            risk_scores.append({'high': 3, 'medium': 2, 'low': 1}.get(severity, 0))
        
        if 'vitals' in assessments:
            if assessments['vitals']['requires_attention']:
                risk_scores.append(3)
            elif assessments['vitals']['abnormalities_found']:
                risk_scores.append(2)
        
        if 'bmi' in assessments:
            risk_level = assessments['bmi']['risk_level']
            risk_scores.append({'high': 3, 'medium': 2, 'low': 1}.get(risk_level, 0))
        
        if not risk_scores:
            return 'unknown'
        
        avg_risk = sum(risk_scores) / len(risk_scores)
        
        if avg_risk >= 2.5:
            return 'high'
        elif avg_risk >= 1.5:
            return 'medium'
        else:
            return 'low'
    
    def _generate_recommendations(self, report: Dict) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Based on overall risk
        risk = report.get('overall_risk', 'unknown')
        
        if risk == 'high':
            recommendations.extend([
                'Seek immediate medical attention',
                'Do not delay consulting a doctor',
                'Monitor symptoms closely',
                'Keep emergency numbers handy'
            ])
        elif risk == 'medium':
            recommendations.extend([
                'Schedule a doctor appointment within 24-48 hours',
                'Monitor your symptoms',
                'Rest and stay hydrated',
                'Avoid self-medication'
            ])
        else:
            recommendations.extend([
                'Continue monitoring your health',
                'Maintain a healthy lifestyle',
                'Consult doctor if symptoms worsen',
                'Stay hydrated and get adequate rest'
            ])
        
        # Add specific recommendations based on assessments
        if 'bmi' in report['assessments']:
            bmi_recs = report['assessments']['bmi'].get('recommendations', [])
            recommendations.extend(bmi_recs[:2])  # Add top 2 BMI recommendations
        
        return recommendations
    
    def predict_health_trends(self, user_history: List[Dict]) -> Dict:
        """Predict health trends based on user history"""
        if not user_history or len(user_history) < 3:
            return {'trend': 'insufficient_data'}
        
        # Analyze symptom frequency
        symptom_frequency = {}
        for entry in user_history:
            for symptom in entry.get('symptoms', []):
                symptom_frequency[symptom] = symptom_frequency.get(symptom, 0) + 1
        
        # Identify recurring issues
        recurring = {k: v for k, v in symptom_frequency.items() if v >= 3}
        
        # Determine trend
        if len(recurring) > 0:
            trend = 'recurring_issues'
            recommendation = 'Consider comprehensive health checkup'
        elif len(symptom_frequency) > 5:
            trend = 'varied_symptoms'
            recommendation = 'Monitor overall health closely'
        else:
            trend = 'stable'
            recommendation = 'Maintain current health practices'
        
        return {
            'trend': trend,
            'symptom_frequency': symptom_frequency,
            'recurring_issues': list(recurring.keys()),
            'recommendation': recommendation
        }