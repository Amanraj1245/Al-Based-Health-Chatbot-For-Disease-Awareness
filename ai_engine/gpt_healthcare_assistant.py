"""
GPT-Powered Healthcare Assistant
Integrates OpenAI GPT-4 for ChatGPT-like conversational experience
with healthcare specialization
"""

import os
from typing import Dict, List, Optional
from openai import OpenAI
import json

class GPTHealthcareAssistant:
    """ChatGPT-like healthcare assistant using GPT-4"""
    
    def __init__(self, api_key: Optional[str] = None):
        # Use provided API key or get from environment
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"  # Using GPT-4 Mini for cost-effectiveness
        
        # Medical knowledge base for context
        self.medical_context = self._load_medical_context()
        
        # Conversation history storage
        self.conversations = {}
    
    def _load_medical_context(self) -> str:
        """Load comprehensive medical context for GPT"""
        return """You are Dr. AI, a knowledgeable, empathetic, and professional healthcare assistant. 

YOUR ROLE:
- Provide helpful health information and guidance
- Engage in natural, conversational dialogue like ChatGPT
- Show genuine empathy and concern for users
- Ask relevant follow-up questions to understand better
- Provide evidence-based health information

IMPORTANT GUIDELINES:
1. ALWAYS include a disclaimer that you're an AI, not a real doctor
2. For serious symptoms (chest pain, difficulty breathing, severe bleeding, etc.), URGE immediate medical attention
3. Be conversational and warm - not clinical or robotic
4. Ask one or two questions at a time - don't overwhelm
5. Validate the user's feelings and concerns
6. Provide practical, actionable advice when appropriate
7. Use clear, simple language - avoid excessive medical jargon
8. Be supportive and encouraging

SYMPTOM ANALYSIS APPROACH:
- Acknowledge their symptoms with empathy
- Ask clarifying questions (duration, severity, triggers)
- Consider possible causes without diagnosing
- Suggest when to see a doctor
- Offer self-care tips for minor issues

EMERGENCY RECOGNITION:
If user mentions: chest pain, can't breathe, severe bleeding, unconsciousness, severe allergic reaction, suicidal thoughts
→ IMMEDIATELY advise calling emergency services (911) or going to ER

CONVERSATION STYLE:
- Warm and caring like a trusted family doctor
- Use phrases like "I understand," "That sounds difficult," "I'm here to help"
- Share information gradually, not all at once
- Check in: "Does that make sense?" or "Do you have any questions about that?"
- End with encouragement and next steps"""
    
    def get_response(self, user_message: str, user_id: int, 
                     detected_symptoms: List[str] = None,
                     language: str = 'en') -> Dict:
        """Get GPT-powered response for healthcare query"""
        
        # Initialize conversation history for new users
        if user_id not in self.conversations:
            self.conversations[user_id] = [
                {"role": "system", "content": self.medical_context}
            ]
        
        # Add symptom context if detected
        symptom_context = ""
        if detected_symptoms:
            symptom_context = f"\n[Detected symptoms: {', '.join(detected_symptoms)}]"
        
        # Add language preference
        lang_instruction = ""
        if language == 'hi':
            lang_instruction = "\nRespond in Hindi language."
        
        # Prepare user message with context
        enhanced_message = user_message + symptom_context + lang_instruction
        
        # Add user message to history
        self.conversations[user_id].append({
            "role": "user", 
            "content": enhanced_message
        })
        
        # Keep only last 20 messages to manage context window
        if len(self.conversations[user_id]) > 21:  # 1 system + 20 conversation
            self.conversations[user_id] = [
                self.conversations[user_id][0]  # Keep system message
            ] + self.conversations[user_id][-20:]  # Keep last 20
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversations[user_id],
                temperature=0.7,
                max_tokens=800,
                top_p=1.0,
                frequency_penalty=0.5,
                presence_penalty=0.5
            )
            
            # Extract assistant's response
            assistant_message = response.choices[0].message.content
            
            # Add to conversation history
            self.conversations[user_id].append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return {
                'success': True,
                'response': assistant_message,
                'model': self.model,
                'tokens_used': response.usage.total_tokens if response.usage else 0,
                'detected_symptoms': detected_symptoms or []
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response': "I apologize, but I'm having trouble processing your request right now. Please try again in a moment."
            }
    
    def get_streaming_response(self, user_message: str, user_id: int,
                               detected_symptoms: List[str] = None,
                               language: str = 'en'):
        """Get streaming response for real-time chat feel"""
        
        if user_id not in self.conversations:
            self.conversations[user_id] = [
                {"role": "system", "content": self.medical_context}
            ]
        
        symptom_context = ""
        if detected_symptoms:
            symptom_context = f"\n[Detected symptoms: {', '.join(detected_symptoms)}]"
        
        lang_instruction = ""
        if language == 'hi':
            lang_instruction = "\nRespond in Hindi language."
        
        enhanced_message = user_message + symptom_context + lang_instruction
        
        self.conversations[user_id].append({
            "role": "user", 
            "content": enhanced_message
        })
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversations[user_id],
                temperature=0.7,
                max_tokens=800,
                stream=True
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
            
            # Save complete response to history
            self.conversations[user_id].append({
                "role": "assistant",
                "content": full_response
            })
            
        except Exception as e:
            yield f"I apologize, but I'm having trouble right now. Error: {str(e)}"
    
    def analyze_symptoms_with_gpt(self, symptoms: List[str], user_context: Dict) -> Dict:
        """Use GPT to analyze symptoms and provide insights"""
        
        prompt = f"""As a healthcare AI, analyze these symptoms and provide insights:

Symptoms: {', '.join(symptoms)}
User Context: {json.dumps(user_context)}

Provide a JSON response with:
1. possible_conditions: List of possible conditions (not diagnoses)
2. urgency_level: low/medium/high/emergency
3. recommended_actions: What the user should do
4. questions_to_ask: Follow-up questions for better understanding
5. self_care_tips: Practical advice for symptom relief

Format as valid JSON only."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a medical analysis AI. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=600,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return {
                'success': True,
                'analysis': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_health_recommendations(self, user_profile: Dict, goals: List[str]) -> Dict:
        """Get personalized health recommendations using GPT"""
        
        prompt = f"""Based on this user profile, provide personalized health recommendations:

User Profile: {json.dumps(user_profile)}
Health Goals: {', '.join(goals)}

Provide recommendations for:
1. Diet and nutrition
2. Exercise and physical activity
3. Sleep hygiene
4. Stress management
5. Preventive health measures

Be specific, practical, and encouraging."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a health and wellness coach."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            return {
                'success': True,
                'recommendations': response.choices[0].message.content
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def clear_conversation(self, user_id: int):
        """Clear conversation history for a user"""
        if user_id in self.conversations:
            del self.conversations[user_id]
    
    def get_conversation_summary(self, user_id: int) -> str:
        """Get summary of conversation for context"""
        if user_id not in self.conversations:
            return "No conversation history"
        
        # Extract just the user messages for summary
        user_messages = [m['content'] for m in self.conversations[user_id] 
                        if m['role'] == 'user']
        
        if not user_messages:
            return "New conversation"
        
        return f"Conversation with {len(user_messages)} messages"


# Initialize GPT assistant (will be configured with API key in app.py)
gpt_assistant = None

def init_gpt_assistant(api_key: str):
    """Initialize GPT assistant with API key"""
    global gpt_assistant
    gpt_assistant = GPTHealthcareAssistant(api_key)
    return gpt_assistant