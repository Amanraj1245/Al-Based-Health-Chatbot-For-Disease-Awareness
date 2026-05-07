"""
Medication Manager Module
Manages medication schedules, reminders, and tracking
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict
import json

class MedicationManager:
    """Manage medication schedules and reminders"""
    
    def __init__(self):
        self.medications_db = defaultdict(list)  # user_id -> list of medications
        self.reminder_history = defaultdict(list)  # user_id -> reminder history
        self.drug_interactions = self._load_drug_interactions()
        self.medication_database = self._load_medication_database()
    
    def _load_drug_interactions(self) -> Dict:
        """Load known drug interactions"""
        return {
            ('warfarin', 'aspirin'): 'high',
            ('warfarin', 'ibuprofen'): 'high',
            ('metformin', 'contrast_dye'): 'medium',
            ('lisinopril', 'potassium'): 'medium',
            ('simvastatin', 'grapefruit'): 'medium',
            ('fluoxetine', 'tramadol'): 'high',
            ('amoxicillin', 'probenecid'): 'low',
            ('insulin', 'beta_blockers'): 'medium'
        }
    
    def _load_medication_database(self) -> Dict:
        """Load medication information database"""
        return {
            'paracetamol': {
                'category': 'pain_relief',
                'max_daily_dose': '4000mg',
                'frequency': 'every 4-6 hours',
                'with_food': False,
                'side_effects': ['nausea', 'stomach_upset'],
                'interactions': ['warfarin', 'alcohol']
            },
            'ibuprofen': {
                'category': 'nsaid',
                'max_daily_dose': '1200mg',
                'frequency': 'every 6-8 hours',
                'with_food': True,
                'side_effects': ['stomach_pain', 'heartburn', 'dizziness'],
                'interactions': ['aspirin', 'warfarin', 'lisinopril']
            },
            'amoxicillin': {
                'category': 'antibiotic',
                'max_daily_dose': 'as_prescribed',
                'frequency': 'every 8 hours',
                'with_food': False,
                'side_effects': ['diarrhea', 'rash', 'nausea'],
                'interactions': ['probenecid', 'allopurinol']
            },
            'metformin': {
                'category': 'diabetes',
                'max_daily_dose': '2000mg',
                'frequency': 'twice daily with meals',
                'with_food': True,
                'side_effects': ['stomach_upset', 'diarrhea', 'metallic_taste'],
                'interactions': ['contrast_dye', 'alcohol']
            },
            'atorvastatin': {
                'category': 'cholesterol',
                'max_daily_dose': '80mg',
                'frequency': 'once daily',
                'with_food': False,
                'side_effects': ['muscle_pain', 'liver_issues'],
                'interactions': ['grapefruit', 'erythromycin']
            },
            'lisinopril': {
                'category': 'blood_pressure',
                'max_daily_dose': '40mg',
                'frequency': 'once daily',
                'with_food': False,
                'side_effects': ['dry_cough', 'dizziness', 'high_potassium'],
                'interactions': ['potassium_supplements', 'nsaids']
            },
            'omeprazole': {
                'category': 'acid_reflux',
                'max_daily_dose': '40mg',
                'frequency': 'once daily before breakfast',
                'with_food': False,
                'side_effects': ['headache', 'diarrhea', 'vitamin_b12_deficiency'],
                'interactions': ['clopidogrel', 'antifungals']
            },
            'levothyroxine': {
                'category': 'thyroid',
                'max_daily_dose': 'as_prescribed',
                'frequency': 'once daily on empty stomach',
                'with_food': False,
                'side_effects': ['weight_loss', 'tremors', 'insomnia'],
                'interactions': ['calcium', 'iron', 'antacids']
            }
        }
    
    def add_medication(self, user_id: int, medication_data: Dict) -> Dict:
        """Add a new medication for a user"""
        medication = {
            'id': len(self.medications_db[user_id]) + 1,
            'name': medication_data['name'].lower(),
            'dosage': medication_data['dosage'],
            'frequency': medication_data['frequency'],
            'times': medication_data.get('times', ['08:00']),
            'start_date': medication_data.get('start_date', datetime.now().strftime('%Y-%m-%d')),
            'end_date': medication_data.get('end_date'),
            'with_food': medication_data.get('with_food', False),
            'notes': medication_data.get('notes', ''),
            'created_at': datetime.now().isoformat(),
            'active': True
        }
        
        # Check for interactions with existing medications
        interactions = self._check_interactions(user_id, medication['name'])
        
        self.medications_db[user_id].append(medication)
        
        return {
            'success': True,
            'medication': medication,
            'interactions': interactions,
            'message': 'Medication added successfully' if not interactions else 'Warning: Drug interactions detected'
        }
    
    def _check_interactions(self, user_id: int, new_medication: str) -> List[Dict]:
        """Check for drug interactions"""
        interactions = []
        new_med_lower = new_medication.lower()
        
        for med in self.medications_db[user_id]:
            if not med['active']:
                continue
                
            med_lower = med['name'].lower()
            
            # Check direct interactions
            interaction_key = tuple(sorted([new_med_lower, med_lower]))
            if interaction_key in self.drug_interactions:
                severity = self.drug_interactions[interaction_key]
                interactions.append({
                    'medication1': new_medication,
                    'medication2': med['name'],
                    'severity': severity,
                    'recommendation': 'Consult doctor immediately' if severity == 'high' else 'Monitor for side effects'
                })
            
            # Check database interactions
            med_info = self.medication_database.get(med_lower, {})
            if new_med_lower in med_info.get('interactions', []):
                interactions.append({
                    'medication1': new_medication,
                    'medication2': med['name'],
                    'severity': 'medium',
                    'recommendation': 'Potential interaction - consult pharmacist'
                })
        
        return interactions
    
    def get_medications(self, user_id: int, active_only: bool = True) -> List[Dict]:
        """Get all medications for a user"""
        medications = self.medications_db.get(user_id, [])
        if active_only:
            medications = [m for m in medications if m['active']]
        return medications
    
    def get_todays_schedule(self, user_id: int) -> List[Dict]:
        """Get today's medication schedule"""
        medications = self.get_medications(user_id)
        schedule = []
        today = datetime.now().strftime('%Y-%m-%d')
        
        for med in medications:
            for time_str in med['times']:
                schedule.append({
                    'medication_id': med['id'],
                    'name': med['name'],
                    'dosage': med['dosage'],
                    'time': time_str,
                    'with_food': med['with_food'],
                    'taken': self._is_dose_taken(user_id, med['id'], today, time_str),
                    'overdue': self._is_overdue(time_str)
                })
        
        # Sort by time
        schedule.sort(key=lambda x: x['time'])
        return schedule
    
    def _is_dose_taken(self, user_id: int, med_id: int, date: str, time: str) -> bool:
        """Check if a specific dose has been taken"""
        history = self.reminder_history.get(user_id, [])
        for entry in history:
            if (entry.get('medication_id') == med_id and 
                entry.get('date') == date and 
                entry.get('time') == time and
                entry.get('taken', False)):
                return True
        return False
    
    def _is_overdue(self, time_str: str) -> bool:
        """Check if a medication time is overdue"""
        now = datetime.now()
        scheduled_time = datetime.strptime(time_str, '%H:%M').replace(
            year=now.year, month=now.month, day=now.day
        )
        return now > scheduled_time + timedelta(minutes=30)
    
    def mark_dose_taken(self, user_id: int, medication_id: int, time_str: str) -> Dict:
        """Mark a medication dose as taken"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        entry = {
            'medication_id': medication_id,
            'date': today,
            'time': time_str,
            'taken': True,
            'taken_at': datetime.now().isoformat()
        }
        
        self.reminder_history[user_id].append(entry)
        
        return {
            'success': True,
            'message': 'Dose marked as taken',
            'streak': self._calculate_streak(user_id, medication_id)
        }
    
    def _calculate_streak(self, user_id: int, medication_id: int) -> int:
        """Calculate consecutive days medication was taken"""
        history = self.reminder_history.get(user_id, [])
        med_history = [h for h in history if h['medication_id'] == medication_id and h.get('taken')]
        
        if not med_history:
            return 0
        
        # Sort by date
        dates = sorted(set([h['date'] for h in med_history]), reverse=True)
        
        streak = 0
        today = datetime.now().date()
        
        for i, date_str in enumerate(dates):
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            expected_date = today - timedelta(days=i)
            
            if date == expected_date:
                streak += 1
            else:
                break
        
        return streak
    
    def get_adherence_stats(self, user_id: int, days: int = 30) -> Dict:
        """Get medication adherence statistics"""
        history = self.reminder_history.get(user_id, [])
        medications = self.get_medications(user_id)
        
        if not medications:
            return {'status': 'no_medications'}
        
        # Calculate expected doses
        total_expected = 0
        for med in medications:
            total_expected += len(med['times']) * days
        
        # Calculate taken doses
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        taken_doses = len([h for h in history if h['date'] >= cutoff_date and h.get('taken')])
        
        adherence_rate = (taken_doses / total_expected * 100) if total_expected > 0 else 0
        
        return {
            'period_days': days,
            'expected_doses': total_expected,
            'taken_doses': taken_doses,
            'missed_doses': total_expected - taken_doses,
            'adherence_rate': round(adherence_rate, 1),
            'status': 'excellent' if adherence_rate >= 90 else 'good' if adherence_rate >= 80 else 'needs_improvement'
        }
    
    def get_medication_info(self, medication_name: str) -> Optional[Dict]:
        """Get information about a medication"""
        return self.medication_database.get(medication_name.lower())
    
    def get_reminders(self, user_id: int) -> List[Dict]:
        """Get pending reminders for a user"""
        schedule = self.get_todays_schedule(user_id)
        now = datetime.now()
        reminders = []
        
        for item in schedule:
            if item['taken']:
                continue
                
            scheduled_time = datetime.strptime(item['time'], '%H:%M').replace(
                year=now.year, month=now.month, day=now.day
            )
            
            time_diff = (scheduled_time - now).total_seconds() / 60  # minutes
            
            if -30 <= time_diff <= 30:  # Within 30 minutes
                reminders.append({
                    'medication_id': item['medication_id'],
                    'name': item['name'],
                    'dosage': item['dosage'],
                    'time': item['time'],
                    'with_food': item['with_food'],
                    'urgency': 'now' if abs(time_diff) < 5 else 'soon'
                })
        
        return reminders
    
    def delete_medication(self, user_id: int, medication_id: int) -> Dict:
        """Delete (deactivate) a medication"""
        medications = self.medications_db.get(user_id, [])
        
        for med in medications:
            if med['id'] == medication_id:
                med['active'] = False
                return {'success': True, 'message': 'Medication removed'}
        
        return {'success': False, 'error': 'Medication not found'}
    
    def get_refill_reminders(self, user_id: int) -> List[Dict]:
        """Get medications that may need refilling"""
        # This is a simplified version - in production, track pill counts
        reminders = []
        medications = self.get_medications(user_id)
        
        for med in medications:
            # Check if medication has been active for a while
            start_date = datetime.strptime(med['start_date'], '%Y-%m-%d')
            days_active = (datetime.now() - start_date).days
            
            # Assume 30-day supply
            if days_active >= 25 and days_active % 30 >= 25:
                reminders.append({
                    'medication_id': med['id'],
                    'name': med['name'],
                    'message': f'Refill {med["name"]} soon - running low'
                })
        
        return reminders


# Initialize medication manager
medication_manager = MedicationManager()