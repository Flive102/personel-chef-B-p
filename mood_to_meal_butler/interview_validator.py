# Interview Validation & Error Recovery Engine
# Ensures data quality, handles edge cases, suggests corrections

from typing import Dict, Tuple, List

class InterviewValidator:
    """Validate interview answers and provide intelligent corrections"""
    
    def __init__(self):
        self.validation_rules = self._setup_rules()
        self.error_messages = {}
    
    def _setup_rules(self) -> Dict:
        """Define validation rules for each question"""
        return {
            "mood": {
                "valid_values": ["tired", "happy", "stressed", "sad", "neutral"],
                "min_length": 2,
                "allow_synonyms": True
            },
            "craving": {
                "valid_values": ["spicy", "sweet", "light", "rich", "surprise"],
                "min_length": 2,
                "allow_synonyms": True
            },
            "group": {
                "valid_values": ["solo", "couple", "group", "family"],
                "min_length": 2,
                "allow_synonyms": True
            },
            "budget": {
                "valid_values": ["budget", "moderate", "splurge"],
                "min_length": 2,
                "allow_synonyms": True
            },
            "time": {
                "valid_values": ["quick", "normal", "slow"],
                "min_length": 2,
                "allow_synonyms": True
            },
            "diet": {
                "valid_values": ["none", "vegetarian", "no_seafood", "no_red_meat"],
                "min_length": 2,
                "allow_synonyms": True
            }
        }
    
    def validate_answer(self, question_key: str, answer: str) -> Tuple[bool, str, Dict]:
        """
        Validate a single answer
        Returns: (is_valid, message, suggestions)
        """
        if not answer or answer.strip() == "":
            return False, "Answer cannot be empty", {
                "suggestion": "Please provide an answer",
                "severity": "high"
            }
        
        # Length check
        rules = self.validation_rules.get(question_key, {})
        min_len = rules.get("min_length", 2)
        if len(answer.strip()) < min_len:
            return False, f"Answer too short (min {min_len} characters)", {
                "suggestion": "Please provide a more complete answer",
                "severity": "medium"
            }
        
        return True, "Valid", {}
    
    def validate_complete_interview(self, answers: Dict) -> Tuple[bool, Dict]:
        """
        Validate entire interview response
        Returns: (is_complete_and_valid, issues_dict)
        """
        required_fields = ["mood", "craving", "group", "budget", "time", "diet"]
        issues = {
            "missing_fields": [],
            "empty_fields": [],
            "warnings": []
        }
        
        for field in required_fields:
            if field not in answers:
                issues["missing_fields"].append(field)
            elif not answers[field] or answers[field].strip() == "":
                issues["empty_fields"].append(field)
        
        is_valid = len(issues["missing_fields"]) == 0 and len(issues["empty_fields"]) == 0
        return is_valid, issues
    
    def suggest_correction(self, question_key: str, answer: str) -> Dict:
        """Suggest correction for a problematic answer"""
        suggestions = {
            "original": answer,
            "possible_corrections": [],
            "confidence": 0.0,
            "reasoning": ""
        }
        
        # Common typos/mistakes
        typo_corrections = {
            "mood": {
                "tired": ["tires", "tired", "tire", "tird"],
                "happy": ["happi", "happie", "happy", "hippy"],
                "stressed": ["stress", "stressed", "stresed"],
                "sad": ["sad", "sade", "sade"],
                "neutral": ["neutral", "nutral", "nuetral"]
            }
        }
        
        if question_key in typo_corrections:
            for correct, variants in typo_corrections[question_key].items():
                for variant in variants:
                    if variant.lower() in answer.lower():
                        suggestions["possible_corrections"].append(correct)
                        suggestions["confidence"] = 0.85
                        suggestions["reasoning"] = f"Likely meant '{correct}'"
                        break
        
        return suggestions
    
    def get_validation_report(self, answers: Dict) -> Dict:
        """Generate validation report for interview session"""
        is_valid, issues = self.validate_complete_interview(answers)
        
        report = {
            "session_valid": is_valid,
            "completion_percentage": self._calculate_completion(answers),
            "field_quality": self._assess_field_quality(answers),
            "issues": issues,
            "recommendations": self._generate_recommendations(issues)
        }
        
        return report
    
    def _calculate_completion(self, answers: Dict) -> float:
        """Calculate interview completion percentage"""
        required = 6
        filled = sum(1 for k in ["mood", "craving", "group", "budget", "time", "diet"] 
                    if k in answers and answers[k])
        return round((filled / required) * 100, 1)
    
    def _assess_field_quality(self, answers: Dict) -> Dict:
        """Assess quality of each field"""
        quality = {}
        for key in ["mood", "craving", "group", "budget", "time", "diet"]:
            if key not in answers:
                quality[key] = "missing"
            elif not answers[key] or answers[key].strip() == "":
                quality[key] = "empty"
            elif len(answers[key]) < 3:
                quality[key] = "too_short"
            else:
                quality[key] = "valid"
        return quality
    
    def _generate_recommendations(self, issues: Dict) -> List[str]:
        """Generate recommendations based on issues"""
        recs = []
        
        if issues["missing_fields"]:
            recs.append(f"Complete missing fields: {', '.join(issues['missing_fields'])}")
        
        if issues["empty_fields"]:
            recs.append(f"Fill empty fields: {', '.join(issues['empty_fields'])}")
        
        if not recs:
            recs.append("Interview data looks good! Ready for meal recommendations.")
        
        return recs
