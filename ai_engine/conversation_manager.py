"""
Conversation Manager Module
Manages conversation context, memory, and flow
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import deque
import json

class ConversationManager:
    """Manages conversation state and context for the AI chatbot"""
    
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.sessions = {}
        self.context_memory = {}
    
    def create_session(self, user_id: int) -> str:
        """Create a new conversation session"""
        session_id = f"{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.sessions[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
            'last_active': datetime.now(),
            'history': deque(maxlen=self.max_history),
            'context': {
                'current_intent': None,
                'detected_symptoms': [],
                'user_info': {},
                'follow_up_needed': False,
                'follow_up_questions': [],
                'conversation_stage': 'greeting'  # greeting, information_gathering, diagnosis, recommendation
            }
        }
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data"""
        return self.sessions.get(session_id)
    
    def add_message(self, session_id: str, role: str, content: str, 
                    intent: str = None, entities: List = None):
        """Add a message to conversation history"""
        if session_id not in self.sessions:
            return
        
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now(),
            'intent': intent,
            'entities': entities or []
        }
        
        self.sessions[session_id]['history'].append(message)
        self.sessions[session_id]['last_active'] = datetime.now()
    
    def get_conversation_history(self, session_id: str, last_n: int = 5) -> List[Dict]:
        """Get last N messages from conversation"""
        if session_id not in self.sessions:
            return []
        
        history = list(self.sessions[session_id]['history'])
        return history[-last_n:] if len(history) > last_n else history
    
    def update_context(self, session_id: str, updates: Dict):
        """Update conversation context"""
        if session_id not in self.sessions:
            return
        
        self.sessions[session_id]['context'].update(updates)
    
    def get_context(self, session_id: str) -> Dict:
        """Get current conversation context"""
        if session_id not in self.sessions:
            return {}
        return self.sessions[session_id]['context']
    
    def add_detected_symptom(self, session_id: str, symptom: str):
        """Add a detected symptom to context"""
        if session_id not in self.sessions:
            return
        
        symptoms = self.sessions[session_id]['context']['detected_symptoms']
        if symptom not in symptoms:
            symptoms.append(symptom)
    
    def set_follow_up_questions(self, session_id: str, questions: List[str]):
        """Set follow-up questions for the conversation"""
        if session_id not in self.sessions:
            return
        
        self.sessions[session_id]['context']['follow_up_questions'] = questions
        self.sessions[session_id]['context']['follow_up_needed'] = len(questions) > 0
    
    def get_next_follow_up(self, session_id: str) -> Optional[str]:
        """Get next follow-up question"""
        if session_id not in self.sessions:
            return None
        
        questions = self.sessions[session_id]['context']['follow_up_questions']
        if questions:
            return questions[0]
        return None
    
    def remove_follow_up(self, session_id: str):
        """Remove answered follow-up question"""
        if session_id not in self.sessions:
            return
        
        questions = self.sessions[session_id]['context']['follow_up_questions']
        if questions:
            questions.pop(0)
        
        if not questions:
            self.sessions[session_id]['context']['follow_up_needed'] = False
    
    def analyze_conversation_flow(self, session_id: str) -> Dict:
        """Analyze conversation flow and patterns"""
        if session_id not in self.sessions:
            return {}
        
        history = list(self.sessions[session_id]['history'])
        
        # Count messages by role
        user_messages = [m for m in history if m['role'] == 'user']
        assistant_messages = [m for m in history if m['role'] == 'assistant']
        
        # Analyze intents
        intents = {}
        for msg in user_messages:
            if msg.get('intent'):
                intents[msg['intent']] = intents.get(msg['intent'], 0) + 1
        
        # Calculate conversation duration
        if len(history) >= 2:
            duration = history[-1]['timestamp'] - history[0]['timestamp']
        else:
            duration = timedelta(0)
        
        return {
            'total_messages': len(history),
            'user_messages': len(user_messages),
            'assistant_messages': len(assistant_messages),
            'intent_distribution': intents,
            'duration_seconds': duration.total_seconds(),
            'average_response_time': self._calculate_avg_response_time(history)
        }
    
    def _calculate_avg_response_time(self, history: List[Dict]) -> float:
        """Calculate average response time"""
        if len(history) < 2:
            return 0.0
        
        response_times = []
        for i in range(1, len(history)):
            if history[i]['role'] == 'assistant' and history[i-1]['role'] == 'user':
                time_diff = history[i]['timestamp'] - history[i-1]['timestamp']
                response_times.append(time_diff.total_seconds())
        
        return sum(response_times) / len(response_times) if response_times else 0.0
    
    def get_conversation_summary(self, session_id: str) -> str:
        """Generate a summary of the conversation"""
        if session_id not in self.sessions:
            return "No conversation found."
        
        context = self.sessions[session_id]['context']
        symptoms = context.get('detected_symptoms', [])
        current_intent = context.get('current_intent')
        
        summary_parts = []
        
        if symptoms:
            summary_parts.append(f"Symptoms discussed: {', '.join(symptoms)}")
        
        if current_intent:
            summary_parts.append(f"Current topic: {current_intent}")
        
        return " | ".join(summary_parts) if summary_parts else "General conversation"
    
    def should_escalate(self, session_id: str) -> bool:
        """Determine if conversation should be escalated to human"""
        if session_id not in self.sessions:
            return False
        
        context = self.sessions[session_id]['context']
        
        # Escalate if multiple high severity symptoms
        symptoms = context.get('detected_symptoms', [])
        if len(symptoms) >= 5:
            return True
        
        # Escalate if conversation is too long
        history = self.sessions[session_id]['history']
        if len(history) > 20:
            return True
        
        # Escalate if user is frustrated (repeated questions)
        user_messages = [m for m in history if m['role'] == 'user']
        if len(user_messages) >= 3:
            # Check for repetition
            recent = [m['content'].lower() for m in user_messages[-3:]]
            if len(set(recent)) < len(recent):
                return True
        
        return False
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Remove old inactive sessions"""
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        to_remove = []
        
        for session_id, session in self.sessions.items():
            if session['last_active'] < cutoff:
                to_remove.append(session_id)
        
        for session_id in to_remove:
            del self.sessions[session_id]
        
        return len(to_remove)
    
    def export_conversation(self, session_id: str) -> Dict:
        """Export conversation data for storage"""
        if session_id not in self.sessions:
            return {}
        
        session = self.sessions[session_id]
        return {
            'session_id': session_id,
            'user_id': session['user_id'],
            'created_at': session['created_at'].isoformat(),
            'last_active': session['last_active'].isoformat(),
            'context': session['context'],
            'history': [
                {
                    'role': msg['role'],
                    'content': msg['content'],
                    'timestamp': msg['timestamp'].isoformat(),
                    'intent': msg.get('intent')
                }
                for msg in session['history']
            ]
        }
    
    def get_user_memory(self, user_id: int) -> Dict:
        """Get persistent memory for a user"""
        return self.context_memory.get(user_id, {
            'previous_symptoms': [],
            'common_concerns': [],
            'preferred_language': 'en',
            'total_conversations': 0
        })
    
    def update_user_memory(self, user_id: int, data: Dict):
        """Update persistent user memory"""
        if user_id not in self.context_memory:
            self.context_memory[user_id] = self.get_user_memory(user_id)
        
        self.context_memory[user_id].update(data)
        self.context_memory[user_id]['total_conversations'] += 1