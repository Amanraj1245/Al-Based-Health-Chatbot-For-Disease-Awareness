"""
Image Analysis Module
Analyzes health-related images (skin conditions, eye redness, etc.)
Works without external APIs using rule-based analysis
"""

import os
from typing import Dict, List, Tuple, Optional
from PIL import Image
import colorsys

class ImageAnalyzer:
    """Analyze health-related images"""
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        
        # Skin condition color patterns
        self.skin_conditions = {
            'redness': {
                'color_ranges': [(0, 50, 50), (20, 100, 100)],  # HSV ranges
                'conditions': ['irritation', 'rash', 'sunburn', 'allergic_reaction'],
                'severity_indicators': ['intensity', 'spread']
            },
            'yellowing': {
                'color_ranges': [(40, 50, 50), (70, 100, 100)],
                'conditions': ['jaundice', 'bruise_healing', 'infection'],
                'severity_indicators': ['intensity']
            },
            'dark_spots': {
                'color_ranges': [(0, 0, 0), (360, 50, 50)],
                'conditions': ['moles', 'melanoma_risk', 'age_spots', 'acne_scars'],
                'severity_indicators': ['irregularity', 'size_variation']
            },
            'blue_purple': {
                'color_ranges': [(200, 30, 30), (280, 100, 100)],
                'conditions': ['bruising', 'poor_circulation', 'cyanosis'],
                'severity_indicators': ['spread', 'intensity']
            },
            'white_patches': {
                'color_ranges': [(0, 0, 80), (360, 20, 100)],
                'conditions': ['vitiligo', 'fungal_infection', 'scars', 'pityriasis'],
                'severity_indicators': ['spread', 'contrast']
            }
        }
        
        # Eye condition indicators
        self.eye_conditions = {
            'redness': {
                'color_ranges': [(0, 50, 40), (20, 100, 100)],
                'conditions': ['conjunctivitis', 'eye_strain', 'dry_eyes', 'allergy'],
                'recommendations': ['eye_drops', 'rest', 'avoid_allergens']
            },
            'yellow_sclera': {
                'color_ranges': [(50, 30, 50), (70, 100, 100)],
                'conditions': ['jaundice', 'liver_issues'],
                'recommendations': ['see_doctor_immediately', 'liver_function_test']
            }
        }
        
        # Nail condition indicators
        self.nail_conditions = {
            'white_spots': ['zinc_deficiency', 'minor_trauma', 'fungal_infection'],
            'yellow_nails': ['fungal_infection', 'psoriasis', 'thyroid_issues'],
            'ridges': ['nutritional_deficiency', 'aging', 'eczema'],
            'clubbing': ['lung_disease', 'heart_disease', 'liver_disease'],
            'pale_nails': ['anemia', 'malnutrition', 'liver_disease']
        }
    
    def analyze_image(self, image_path: str, analysis_type: str = 'general') -> Dict:
        """Analyze a health-related image"""
        
        # Validate image
        validation = self._validate_image(image_path)
        if not validation['valid']:
            return {
                'success': False,
                'error': validation['error'],
                'recommendations': ['Please upload a valid image file']
            }
        
        try:
            # Load and process image
            img = Image.open(image_path)
            img_rgb = img.convert('RGB')
            
            # Get image statistics
            color_stats = self._analyze_colors(img_rgb)
            
            # Perform specific analysis based on type
            if analysis_type == 'skin':
                analysis = self._analyze_skin(img_rgb, color_stats)
            elif analysis_type == 'eye':
                analysis = self._analyze_eye(img_rgb, color_stats)
            elif analysis_type == 'nail':
                analysis = self._analyze_nail(img_rgb, color_stats)
            else:
                analysis = self._general_analysis(img_rgb, color_stats)
            
            return {
                'success': True,
                'analysis_type': analysis_type,
                'image_info': {
                    'size': img.size,
                    'mode': img.mode,
                    'format': img.format
                },
                'color_analysis': color_stats,
                'findings': analysis['findings'],
                'possible_conditions': analysis['conditions'],
                'confidence_score': analysis['confidence'],
                'recommendations': analysis['recommendations'],
                'urgency_level': analysis['urgency']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error analyzing image: {str(e)}',
                'recommendations': ['Please try with a different image']
            }
    
    def _validate_image(self, image_path: str) -> Dict:
        """Validate image file"""
        if not os.path.exists(image_path):
            return {'valid': False, 'error': 'File not found'}
        
        # Check file extension
        ext = os.path.splitext(image_path)[1].lower()
        if ext not in self.supported_formats:
            return {'valid': False, 'error': f'Unsupported format. Use: {", ".join(self.supported_formats)}'}
        
        # Check file size
        file_size = os.path.getsize(image_path)
        if file_size > self.max_file_size:
            return {'valid': False, 'error': f'File too large. Max size: {self.max_file_size // (1024*1024)}MB'}
        
        return {'valid': True}
    
    def _analyze_colors(self, img: Image.Image) -> Dict:
        """Analyze color distribution in image"""
        pixels = list(img.getdata())
        total_pixels = len(pixels)
        
        # Calculate average colors
        r_total = g_total = b_total = 0
        h_values = []
        s_values = []
        v_values = []
        
        for r, g, b in pixels:
            r_total += r
            g_total += g
            b_total += b
            
            # Convert to HSV
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            h_values.append(h * 360)
            s_values.append(s * 100)
            v_values.append(v * 100)
        
        avg_r = r_total // total_pixels
        avg_g = g_total // total_pixels
        avg_b = b_total // total_pixels
        
        return {
            'average_rgb': (avg_r, avg_g, avg_b),
            'average_hsv': (
                sum(h_values) / len(h_values),
                sum(s_values) / len(s_values),
                sum(v_values) / len(v_values)
            ),
            'dominant_hue': self._get_dominant_hue(h_values),
            'brightness': sum(v_values) / len(v_values),
            'saturation': sum(s_values) / len(s_values)
        }
    
    def _get_dominant_hue(self, h_values: List[float]) -> str:
        """Determine dominant hue from H values"""
        avg_h = sum(h_values) / len(h_values)
        
        if 0 <= avg_h < 30 or avg_h >= 330:
            return 'red'
        elif 30 <= avg_h < 60:
            return 'orange_yellow'
        elif 60 <= avg_h < 90:
            return 'yellow_green'
        elif 90 <= avg_h < 150:
            return 'green'
        elif 150 <= avg_h < 210:
            return 'cyan'
        elif 210 <= avg_h < 270:
            return 'blue'
        elif 270 <= avg_h < 330:
            return 'purple_magenta'
        
        return 'unknown'
    
    def _analyze_skin(self, img: Image.Image, color_stats: Dict) -> Dict:
        """Analyze skin conditions"""
        findings = []
        conditions = []
        confidence = 0.5
        urgency = 'low'
        
        avg_h, avg_s, avg_v = color_stats['average_hsv']
        dominant_hue = color_stats['dominant_hue']
        
        # Check for redness
        if dominant_hue == 'red' and avg_s > 30:
            findings.append('Significant redness detected in skin')
            conditions.extend(['irritation', 'rash', 'possible_allergic_reaction'])
            confidence = 0.75
            if avg_s > 60:
                urgency = 'moderate'
        
        # Check for yellowing
        elif dominant_hue == 'orange_yellow' and avg_s > 20:
            findings.append('Yellowish discoloration detected')
            conditions.extend(['jaundice_suspected', 'bruise_healing'])
            confidence = 0.6
            urgency = 'high'  # Jaundice needs medical attention
        
        # Check for dark spots
        elif color_stats['brightness'] < 40:
            findings.append('Dark areas detected - possible moles or hyperpigmentation')
            conditions.extend(['moles', 'age_spots', 'monitor_for_changes'])
            confidence = 0.55
        
        # Check for pale/white areas
        elif avg_v > 80 and avg_s < 20:
            findings.append('Pale or white patches detected')
            conditions.extend(['vitiligo', 'scars', 'fungal_infection'])
            confidence = 0.6
        
        # Check for blue/purple (bruising or circulation issues)
        elif dominant_hue in ['blue', 'purple_magenta']:
            findings.append('Blue/purple discoloration detected')
            conditions.extend(['bruising', 'poor_circulation', 'cyanosis'])
            confidence = 0.7
            urgency = 'moderate'
        
        if not findings:
            findings.append('No significant abnormalities detected')
            conditions.append('normal_skin_appearance')
            confidence = 0.8
        
        recommendations = self._get_skin_recommendations(conditions, urgency)
        
        return {
            'findings': findings,
            'conditions': list(set(conditions)),
            'confidence': confidence,
            'urgency': urgency,
            'recommendations': recommendations
        }
    
    def _analyze_eye(self, img: Image.Image, color_stats: Dict) -> Dict:
        """Analyze eye conditions"""
        findings = []
        conditions = []
        confidence = 0.5
        urgency = 'low'
        
        avg_h, avg_s, avg_v = color_stats['average_hsv']
        dominant_hue = color_stats['dominant_hue']
        
        # Check for redness
        if dominant_hue == 'red' and avg_s > 25:
            findings.append('Eye redness detected')
            conditions.extend(['conjunctivitis', 'eye_strain', 'dry_eyes', 'allergy'])
            confidence = 0.75
            urgency = 'moderate'
        
        # Check for yellow sclera
        elif dominant_hue == 'orange_yellow' and avg_s > 15:
            findings.append('Yellowing of sclera detected - possible jaundice')
            conditions.extend(['jaundice', 'liver_issues'])
            confidence = 0.65
            urgency = 'high'
        
        # Check for pale appearance
        elif avg_v > 85:
            findings.append('Eyes appear pale')
            conditions.extend(['anemia_possible', 'fatigue'])
            confidence = 0.5
        
        if not findings:
            findings.append('Eyes appear normal')
            conditions.append('healthy_eyes')
            confidence = 0.85
        
        recommendations = self._get_eye_recommendations(conditions, urgency)
        
        return {
            'findings': findings,
            'conditions': list(set(conditions)),
            'confidence': confidence,
            'urgency': urgency,
            'recommendations': recommendations
        }
    
    def _analyze_nail(self, img: Image.Image, color_stats: Dict) -> Dict:
        """Analyze nail conditions"""
        findings = []
        conditions = []
        confidence = 0.5
        urgency = 'low'
        
        avg_h, avg_s, avg_v = color_stats['average_hsv']
        dominant_hue = color_stats['dominant_hue']
        
        # Check for yellow nails
        if dominant_hue == 'orange_yellow':
            findings.append('Yellow discoloration of nails')
            conditions.extend(['fungal_infection', 'psoriasis'])
            confidence = 0.7
            urgency = 'moderate'
        
        # Check for pale nails
        elif avg_v > 85 and avg_s < 15:
            findings.append('Nails appear pale')
            conditions.extend(['anemia', 'malnutrition'])
            confidence = 0.6
        
        # Check for blue/purple nails
        elif dominant_hue in ['blue', 'purple_magenta']:
            findings.append('Blue/purple nail discoloration')
            conditions.extend(['poor_circulation', 'cyanosis', 'heart_issues'])
            confidence = 0.7
            urgency = 'high'
        
        if not findings:
            findings.append('Nails appear healthy')
            conditions.append('healthy_nails')
            confidence = 0.8
        
        recommendations = self._get_nail_recommendations(conditions, urgency)
        
        return {
            'findings': findings,
            'conditions': list(set(conditions)),
            'confidence': confidence,
            'urgency': urgency,
            'recommendations': recommendations
        }
    
    def _general_analysis(self, img: Image.Image, color_stats: Dict) -> Dict:
        """General health image analysis"""
        findings = []
        conditions = []
        confidence = 0.4
        urgency = 'low'
        
        # Basic color-based analysis
        dominant_hue = color_stats['dominant_hue']
        brightness = color_stats['brightness']
        
        findings.append(f'Dominant color tone: {dominant_hue}')
        findings.append(f'Image brightness: {"normal" if 30 < brightness < 80 else "unusual"}')
        
        conditions.append('general_health_assessment')
        
        recommendations = [
            'For more accurate analysis, specify the body part (skin, eye, nail)',
            'Ensure good lighting when taking health photos',
            'Consult a healthcare professional for proper diagnosis'
        ]
        
        return {
            'findings': findings,
            'conditions': conditions,
            'confidence': confidence,
            'urgency': urgency,
            'recommendations': recommendations
        }
    
    def _get_skin_recommendations(self, conditions: List[str], urgency: str) -> List[str]:
        """Get recommendations for skin conditions"""
        recommendations = []
        
        if urgency == 'high':
            recommendations.append('Seek immediate medical attention')
        elif urgency == 'moderate':
            recommendations.append('Schedule an appointment with a dermatologist within 24-48 hours')
        
        if 'jaundice_suspected' in conditions:
            recommendations.extend([
                'See a doctor immediately - yellowing may indicate liver issues',
                'Get liver function tests done'
            ])
        
        if any(c in conditions for c in ['irritation', 'rash', 'allergic_reaction']):
            recommendations.extend([
                'Avoid potential irritants or allergens',
                'Apply soothing lotion or calamine',
                'Take antihistamines if allergic reaction suspected'
            ])
        
        if 'moles' in conditions or 'monitor_for_changes' in conditions:
            recommendations.extend([
                'Monitor for changes in size, shape, or color',
                'Use the ABCDE rule: Asymmetry, Border, Color, Diameter, Evolving',
                'See a dermatologist if any changes occur'
            ])
        
        if not recommendations:
            recommendations.append('Maintain good skin hygiene')
            recommendations.append('Use sunscreen for protection')
        
        return recommendations
    
    def _get_eye_recommendations(self, conditions: List[str], urgency: str) -> List[str]:
        """Get recommendations for eye conditions"""
        recommendations = []
        
        if urgency == 'high':
            recommendations.append('Seek immediate medical attention')
        
        if 'conjunctivitis' in conditions:
            recommendations.extend([
                'Use prescribed antibiotic or antihistamine eye drops',
                'Avoid touching or rubbing eyes',
                'Wash hands frequently',
                'Avoid sharing towels or cosmetics'
            ])
        
        if 'eye_strain' in conditions or 'dry_eyes' in conditions:
            recommendations.extend([
                'Follow the 20-20-20 rule: Every 20 minutes, look at something 20 feet away for 20 seconds',
                'Use artificial tears for dry eyes',
                'Adjust screen brightness and position',
                'Ensure proper lighting while reading or working'
            ])
        
        if 'allergy' in conditions:
            recommendations.extend([
                'Avoid known allergens',
                'Use antihistamine eye drops',
                'Apply cold compress to reduce swelling'
            ])
        
        if not recommendations:
            recommendations.append('Continue regular eye care')
            recommendations.append('Schedule routine eye checkup')
        
        return recommendations
    
    def _get_nail_recommendations(self, conditions: List[str], urgency: str) -> List[str]:
        """Get recommendations for nail conditions"""
        recommendations = []
        
        if urgency == 'high':
            recommendations.append('Seek immediate medical attention')
        
        if 'fungal_infection' in conditions:
            recommendations.extend([
                'Keep nails clean and dry',
                'Use antifungal medication as prescribed',
                'Avoid sharing nail clippers',
                'Wear breathable footwear'
            ])
        
        if 'anemia' in conditions or 'malnutrition' in conditions:
            recommendations.extend([
                'Get blood tests to check iron and vitamin levels',
                'Eat iron-rich foods (leafy greens, red meat, beans)',
                'Consider iron supplements after consulting doctor'
            ])
        
        if not recommendations:
            recommendations.append('Maintain good nail hygiene')
            recommendations.append('Keep nails trimmed and clean')
        
        return recommendations
    
    def compare_images(self, image_path1: str, image_path2: str) -> Dict:
        """Compare two images to track changes over time"""
        analysis1 = self.analyze_image(image_path1)
        analysis2 = self.analyze_image(image_path2)
        
        if not analysis1['success'] or not analysis2['success']:
            return {
                'success': False,
                'error': 'Could not analyze one or both images'
            }
        
        # Compare color statistics
        color1 = analysis1['color_analysis']
        color2 = analysis2['color_analysis']
        
        rgb_diff = (
            abs(color1['average_rgb'][0] - color2['average_rgb'][0]),
            abs(color1['average_rgb'][1] - color2['average_rgb'][1]),
            abs(color1['average_rgb'][2] - color2['average_rgb'][2])
        )
        
        total_diff = sum(rgb_diff) / 3
        significant_change = total_diff > 30
        
        return {
            'success': True,
            'color_change': {
                'red_diff': rgb_diff[0],
                'green_diff': rgb_diff[1],
                'blue_diff': rgb_diff[2],
                'average_diff': total_diff
            },
            'significant_change': significant_change,
            'conditions_changed': analysis1['possible_conditions'] != analysis2['possible_conditions'],
            'recommendation': 'See a doctor if changes are concerning' if significant_change else 'Continue monitoring'
        }


# Initialize image analyzer
image_analyzer = ImageAnalyzer()