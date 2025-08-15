from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionGenerateSkincareRoutine(Action):
    
    def name(self) -> Text:
        return "action_generate_skincare_routine"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        skin_type = tracker.get_slot("skin_type")
        age = tracker.get_slot("age")
        skin_issues = tracker.get_slot("skin_issues")
        
        # Generate personalized routine based on collected information
        morning_routine, evening_routine = self.generate_routine(skin_type, age, skin_issues)
        
        routine_message = f"""
        **Your Personalized Skincare Routine**
        Based on your {skin_type} skin type, {age} age range, and concerns about {skin_issues}, here's your customized routine:
        
        🌅 **MORNING ROUTINE:**
        {morning_routine}
        🌙 **EVENING ROUTINE:**
        {evening_routine}

        **Important Tips:**
        - Always patch test new products
        - Introduce new products gradually
        - Use sunscreen daily (SPF 30+)
        - Be consistent for best results
        """
        print(routine_message)
        dispatcher.utter_message(text=routine_message)
        
        return []
    
    def generate_routine(self, skin_type: str, age: str, skin_issues: str) -> tuple:
        """Generate morning and evening routines based on user profile"""
        
        # Base routines by skin type
        routines = {
            "oily": {
                "morning": [
                    "1. Gentle foaming cleanser",
                    "2. Niacinamide serum (oil control)",
                    "3. Lightweight, oil-free moisturizer",
                    "4. Broad-spectrum SPF 30+ sunscreen"
                ],
                "evening": [
                    "1. Double cleanse (oil cleanser + foaming cleanser)",
                    "2. BHA/Salicylic acid (2-3x per week)",
                    "3. Hyaluronic acid serum",
                    "4. Gel-based night moisturizer"
                ]
            },
            "dry": {
                "morning": [
                    "1. Gentle, creamy cleanser",
                    "2. Hyaluronic acid serum",
                    "3. Rich, hydrating moisturizer",
                    "4. Broad-spectrum SPF 30+ sunscreen"
                ],
                "evening": [
                    "1. Gentle, creamy cleanser",
                    "2. Hydrating toner/essence",
                    "3. Face oil or serum",
                    "4. Rich night cream"
                ]
            },
            "combination": {
                "morning": [
                    "1. Gentle gel cleanser",
                    "2. Niacinamide serum (T-zone) + Hyaluronic acid (cheeks)",
                    "3. Lightweight moisturizer",
                    "4. Broad-spectrum SPF 30+ sunscreen"
                ],
                "evening": [
                    "1. Double cleanse",
                    "2. BHA on T-zone (2x per week)",
                    "3. Hydrating serum on dry areas",
                    "4. Balanced moisturizer"
                ]
            },
            "sensitive": {
                "morning": [
                    "1. Gentle, fragrance-free cleanser",
                    "2. Soothing serum (centella or ceramides)",
                    "3. Gentle, fragrance-free moisturizer",
                    "4. Mineral SPF 30+ sunscreen"
                ],
                "evening": [
                    "1. Gentle, fragrance-free cleanser",
                    "2. Calming toner",
                    "3. Barrier repair serum",
                    "4. Rich, soothing night cream"
                ]
            },
            "normal": {
                "morning": [
                    "1. Gentle cleanser",
                    "2. Vitamin C serum",
                    "3. Lightweight moisturizer",
                    "4. Broad-spectrum SPF 30+ sunscreen"
                ],
                "evening": [
                    "1. Gentle cleanser",
                    "2. Retinol (start 1x per week)",
                    "3. Hyaluronic acid serum",
                    "4. Night moisturizer"
                ]
            }
        }
        
        base_routine = routines.get(skin_type, routines["normal"])
        # print(base_routine)
        morning_steps = base_routine["morning"].copy()
        # print(morning_steps)
        evening_steps = base_routine["evening"].copy()
        
        # Modify based on age
        if age in ["thirties", "forties", "fifties_plus"]:
            # Add anti-aging focus
            if "Vitamin C serum" not in "\n".join(morning_steps):
                morning_steps.insert(2, "2.5. Vitamin C serum (antioxidant)")
            if "Retinol" not in "\n".join(evening_steps):
                evening_steps.insert(2, "2.5. Retinol serum (start slowly)")
        
        # Modify based on specific skin issues
        if skin_issues:
            issues_lower = skin_issues.lower()
            
            if "acne" in issues_lower:
                evening_steps.insert(2, "2.5. Benzoyl peroxide or salicylic acid treatment")
            
            if "dark spots" in issues_lower or "hyperpigmentation" in issues_lower:
                morning_steps.insert(2, "2.5. Vitamin C serum")
                evening_steps.insert(2, "2.5. Kojic acid or arbutin serum")
            
            if "wrinkles" in issues_lower or "fine lines" in issues_lower:
                evening_steps.insert(2, "2.5. Retinol or peptide serum")
            
            if "dull" in issues_lower:
                evening_steps.insert(2, "2.5. AHA/Glycolic acid (1-2x per week)")
        
        return "\n".join(morning_steps), "\n".join(evening_steps)