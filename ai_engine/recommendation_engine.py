"""
Recommendation Engine Module
Provides personalized health recommendations
"""

from typing import Dict, List, Optional
import random

class RecommendationEngine:
    """Generates personalized health recommendations"""
    
    def __init__(self):
        self.health_tips = self._load_health_tips()
        self.exercise_plans = self._load_exercise_plans()
        self.diet_plans = self._load_diet_plans()
    
    def _load_health_tips(self) -> Dict:
        """Load health tips database"""
        return {
            'general': {
                'en': [
                    'Drink at least 8 glasses of water daily',
                    'Get 7-8 hours of quality sleep each night',
                    'Take regular breaks from screen time',
                    'Practice deep breathing exercises',
                    'Maintain good posture while sitting',
                    'Wash hands frequently to prevent infections',
                    'Avoid smoking and limit alcohol consumption'
                ],
                'hi': [
                    'रोजाना कम से कम 8 गिलास पानी पिएं',
                    'प्रत्येक रात 7-8 घंटे की गुणवत्तापूर्ण नींद लें',
                    'स्क्रीन समय से नियमित ब्रेक लें',
                    'गहरी सांस लेने का अभ्यास करें',
                    'बैठते समय सही मुद्रा बनाए रखें',
                    'संक्रमण से बचने के लिए बार-बार हाथ धोएं',
                    'धूम्रपान से बचें और शराब का सेवन सीमित करें'
                ]
            },
            'immunity': {
                'en': [
                    'Eat vitamin C rich foods like citrus fruits',
                    'Include ginger and turmeric in your diet',
                    'Get adequate sunlight for vitamin D',
                    'Exercise regularly to boost immunity',
                    'Manage stress through meditation',
                    'Eat probiotic foods like yogurt'
                ],
                'hi': [
                    'संतरे जैसे विटामिन C युक्त खाद्य पदार्थ खाएं',
                    'अपने आहार में अदरक और हल्दी शामिल करें',
                    'विटामिन D के लिए पर्याप्त धूप लें',
                    'प्रतिरक्षा बढ़ाने के लिए नियमित व्यायाम करें',
                    'ध्यान के माध्यम से तनाव प्रबंधित करें',
                    'दही जैसे प्रोबायोटिक खाद्य पदार्थ खाएं'
                ]
            },
            'stress_management': {
                'en': [
                    'Practice mindfulness meditation daily',
                    'Take short walks during work breaks',
                    'Listen to calming music',
                    'Maintain a gratitude journal',
                    'Connect with friends and family',
                    'Limit caffeine intake in evening'
                ],
                'hi': [
                    'रोजाना माइंडफुलनेस ध्यान का अभ्यास करें',
                    'काम के ब्रेक के दौरान छोटी सैर पर जाएं',
                    'शांत करने वाला संगीत सुनें',
                    'कृतज्ञता जर्नल बनाए रखें',
                    'दोस्तों और परिवार से जुड़े रहें',
                    'शाम को कैफीन का सेवन सीमित करें'
                ]
            },
            'digestive_health': {
                'en': [
                    'Eat fiber-rich foods daily',
                    'Chew food thoroughly before swallowing',
                    'Avoid eating late at night',
                    'Include yogurt in your diet',
                    'Stay hydrated throughout the day',
                    'Limit spicy and oily foods'
                ],
                'hi': [
                    'रोजाना फाइबर युक्त खाद्य पदार्थ खाएं',
                    'निगलने से पहले खाने को अच्छी तरह चबाएं',
                    'रात को देर से खाने से बचें',
                    'अपने आहार में दही शामिल करें',
                    'पूरे दिन हाइड्रेटेड रहें',
                    'मसालेदार और तैलीय खाद्य पदार्थों को सीमित करें'
                ]
            }
        }
    
    def _load_exercise_plans(self) -> Dict:
        """Load exercise recommendations"""
        return {
            'beginner': {
                'en': {
                    'title': 'Beginner Exercise Plan',
                    'activities': [
                        '15 minutes brisk walking',
                        '5 minutes stretching',
                        '10 squats',
                        '5 push-ups (knee supported)',
                        '30 seconds plank'
                    ],
                    'frequency': '3-4 times per week'
                },
                'hi': {
                    'title': 'शुरुआती व्यायाम योजना',
                    'activities': [
                        '15 मिनट तेज चलना',
                        '5 मिनट स्ट्रेचिंग',
                        '10 स्क्वाट्स',
                        '5 पुश-अप्स (घुटने से सहारा)',
                        '30 सेकंड प्लैंक'
                    ],
                    'frequency': 'सप्ताह में 3-4 बार'
                }
            },
            'intermediate': {
                'en': {
                    'title': 'Intermediate Exercise Plan',
                    'activities': [
                        '30 minutes jogging or cycling',
                        '15 squats',
                        '10 push-ups',
                        '20 lunges',
                        '45 seconds plank',
                        '15 burpees'
                    ],
                    'frequency': '4-5 times per week'
                },
                'hi': {
                    'title': 'मध्यम व्यायाम योजना',
                    'activities': [
                        '30 मिनट जॉगिंग या साइकिलिंग',
                        '15 स्क्वाट्स',
                        '10 पुश-अप्स',
                        '20 लंजेस',
                        '45 सेकंड प्लैंक',
                        '15 बर्पीज'
                    ],
                    'frequency': 'सप्ताह में 4-5 बार'
                }
            },
            'advanced': {
                'en': {
                    'title': 'Advanced Exercise Plan',
                    'activities': [
                        '45 minutes running or HIIT',
                        '25 squats with weights',
                        '20 push-ups',
                        '30 lunges',
                        '60 seconds plank',
                        '25 burpees',
                        'Pull-ups (as many as possible)'
                    ],
                    'frequency': '5-6 times per week'
                },
                'hi': {
                    'title': 'उन्नत व्यायाम योजना',
                    'activities': [
                        '45 मिनट दौड़ना या HIIT',
                        'वजन के साथ 25 स्क्वाट्स',
                        '20 पुश-अप्स',
                        '30 लंजेस',
                        '60 सेकंड प्लैंक',
                        '25 बर्पीज',
                        'पुल-अप्स (जितना हो सके)'
                    ],
                    'frequency': 'सप्ताह में 5-6 बार'
                }
            }
        }
    
    def _load_diet_plans(self) -> Dict:
        """Load diet recommendations"""
        return {
            'weight_loss': {
                'en': {
                    'title': 'Weight Loss Diet',
                    'breakfast': 'Oatmeal with fruits + Green tea',
                    'lunch': 'Grilled chicken/fish + Salad + Brown rice',
                    'dinner': 'Vegetable soup + Whole grain bread',
                    'snacks': 'Nuts, fruits, or yogurt',
                    'tips': 'Eat small portions, avoid sugar and fried foods'
                },
                'hi': {
                    'title': 'वजन घटाने वाला आहार',
                    'breakfast': 'फलों के साथ ओटमील + ग्रीन टी',
                    'lunch': 'ग्रिल्ड चिकन/मछली + सलाद + ब्राउन राइस',
                    'dinner': 'सब्जी का सूप + whole grain ब्रेड',
                    'snacks': 'मेवे, फल, या दही',
                    'tips': 'छोटे हिस्से में खाएं, चीनी और तले हुए खाद्य पदार्थों से बचें'
                }
            },
            'muscle_gain': {
                'en': {
                    'title': 'Muscle Gain Diet',
                    'breakfast': 'Eggs + Whole grain toast + Banana',
                    'lunch': 'Chicken breast + Quinoa + Vegetables',
                    'dinner': 'Fish/Lean meat + Sweet potato + Salad',
                    'snacks': 'Protein shake, peanut butter sandwich',
                    'tips': 'High protein intake, eat every 3 hours'
                },
                'hi': {
                    'title': 'मांसपेशी बढ़ाने वाला आहार',
                    'breakfast': 'अंडे + whole grain टोस्ट + केला',
                    'lunch': 'चिकन ब्रेस्ट + क्विनोआ + सब्जियां',
                    'dinner': 'मछली/लीन मीट + शकरकंदी + सलाद',
                    'snacks': 'प्रोटीन शेक, मूंगफली का मक्खन सैंडविच',
                    'tips': 'अधिक प्रोटीन का सेवन, हर 3 घंटे में खाएं'
                }
            },
            'balanced': {
                'en': {
                    'title': 'Balanced Diet',
                    'breakfast': 'Whole grain cereal + Milk + Fruit',
                    'lunch': 'Mixed vegetables + Lentils + Rice/Roti',
                    'dinner': 'Light meal with vegetables and protein',
                    'snacks': 'Fruits, nuts, or healthy smoothies',
                    'tips': 'Include all food groups, stay hydrated'
                },
                'hi': {
                    'title': 'संतुलित आहार',
                    'breakfast': 'whole grain अनाज + दूध + फल',
                    'lunch': 'मिश्रित सब्जियां + दाल + चावल/रोटी',
                    'dinner': 'सब्जियों और प्रोटीन के साथ हल्का भोजन',
                    'snacks': 'फल, मेवे, या स्वस्थ स्मूदी',
                    'tips': 'सभी खाद्य समूह शामिल करें, हाइड्रेटेड रहें'
                }
            }
        }
    
    def get_daily_tip(self, category: str = 'general', lang: str = 'en') -> str:
        """Get a random health tip"""
        tips = self.health_tips.get(category, self.health_tips['general'])
        tip_list = tips.get(lang, tips.get('en', []))
        return random.choice(tip_list) if tip_list else "Stay healthy!"
    
    def get_exercise_plan(self, level: str = 'beginner', lang: str = 'en') -> Dict:
        """Get exercise plan based on fitness level"""
        plan = self.exercise_plans.get(level, self.exercise_plans['beginner'])
        return plan.get(lang, plan.get('en', {}))
    
    def get_diet_plan(self, goal: str = 'balanced', lang: str = 'en') -> Dict:
        """Get diet plan based on goal"""
        plan = self.diet_plans.get(goal, self.diet_plans['balanced'])
        return plan.get(lang, plan.get('en', {}))
    
    def get_symptom_based_recommendations(self, symptoms: List[str], 
                                          lang: str = 'en') -> List[str]:
        """Get recommendations based on symptoms"""
        recommendations = []
        
        # Rest recommendations
        if any(s in ['fever', 'body_pain', 'fatigue'] for s in symptoms):
            if lang == 'hi':
                recommendations.append('पर्याप्त आराम करें और 7-8 घंटे सोएं')
            else:
                recommendations.append('Get plenty of rest and sleep 7-8 hours')
        
        # Hydration recommendations
        if any(s in ['fever', 'diarrhea', 'vomiting'] for s in symptoms):
            if lang == 'hi':
                recommendations.append('भरपूर तरल पदार्थ पिएं, खासकर ORS')
            else:
                recommendations.append('Stay well hydrated, especially with ORS')
        
        # Diet recommendations
        if any(s in ['stomach_pain', 'vomiting', 'diarrhea'] for s in symptoms):
            if lang == 'hi':
                recommendations.append('हल्का, सुपाच्य भोजन खाएं, मसालेदार खाने से बचें')
            else:
                recommendations.append('Eat light, bland food and avoid spicy foods')
        
        # Breathing recommendations
        if any(s in ['cough', 'breathing_difficulty'] for s in symptoms):
            if lang == 'hi':
                recommendations.append('भाप लें और गर्म तरल पदार्थ पिएं')
            else:
                recommendations.append('Take steam inhalation and drink warm fluids')
        
        return recommendations
    
    def get_personalized_recommendations(self, user_profile: Dict, 
                                          lang: str = 'en') -> Dict:
        """Get fully personalized recommendations"""
        recommendations = {
            'daily_tip': self.get_daily_tip('general', lang),
            'exercise': None,
            'diet': None,
            'lifestyle': []
        }
        
        # Exercise recommendation based on age and activity level
        age = user_profile.get('age', 30)
        activity_level = user_profile.get('activity_level', 'sedentary')
        
        if age < 40:
            if activity_level == 'active':
                recommendations['exercise'] = self.get_exercise_plan('advanced', lang)
            else:
                recommendations['exercise'] = self.get_exercise_plan('intermediate', lang)
        else:
            recommendations['exercise'] = self.get_exercise_plan('beginner', lang)
        
        # Diet recommendation based on goal
        goal = user_profile.get('health_goal', 'balanced')
        recommendations['diet'] = self.get_diet_plan(goal, lang)
        
        # Lifestyle recommendations
        if user_profile.get('smoker'):
            if lang == 'hi':
                recommendations['lifestyle'].append('धूम्रपान छोड़ने के लिए सहायता लें')
            else:
                recommendations['lifestyle'].append('Consider seeking help to quit smoking')
        
        if user_profile.get('stress_level', 'low') == 'high':
            if lang == 'hi':
                recommendations['lifestyle'].append('तनाव प्रबंधन के लिए ध्यान या योग का अभ्यास करें')
            else:
                recommendations['lifestyle'].append('Practice meditation or yoga for stress management')
        
        return recommendations
    
    def generate_health_report_summary(self, health_data: Dict, lang: str = 'en') -> str:
        """Generate a summary of health recommendations"""
        if lang == 'hi':
            summary = "**आपकी स्वास्थ्य सिफारिशें:**\n\n"
            summary += f"💡 **आज का सुझाव:** {self.get_daily_tip('general', 'hi')}\n\n"
            summary += "🥗 **आहार:** संतुलित आहार खाएं जिसमें सभी पोषक तत्व हों\n"
            summary += "🏃 **व्यायाम:** नियमित रूप से कम से कम 30 मिनट व्यायाम करें\n"
            summary += "💧 **हाइड्रेशन:** दिन भर पर्याप्त पानी पिएं\n"
            summary += "😴 **नींद:** रोजाना 7-8 घंटे की नींद लें\n"
        else:
            summary = "**Your Health Recommendations:**\n\n"
            summary += f"💡 **Daily Tip:** {self.get_daily_tip('general', 'en')}\n\n"
            summary += "🥗 **Diet:** Eat a balanced diet with all nutrients\n"
            summary += "🏃 **Exercise:** Exercise regularly for at least 30 minutes\n"
            summary += "💧 **Hydration:** Drink plenty of water throughout the day\n"
            summary += "😴 **Sleep:** Get 7-8 hours of sleep daily\n"
        
        return summary