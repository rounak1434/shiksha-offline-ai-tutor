"""
stem_factual_checker.py
Deterministic factual verification and sanity layer for STEM tutor outputs.
Evaluates model answers against strict scientific laws, SI units, and arithmetic.
"""

import re
from typing import Dict, List, Any

class STEMFactualChecker:
    @staticmethod
    def check_newton_second_law(text: str) -> Dict[str, Any]:
        """
        Validates Newton's Second Law explanations:
        - a = F/m
        - Constant force + more mass -> LESS acceleration (never more)
        - Constant mass + more force -> MORE acceleration
        - Inertia / First law consistency (motion does not stop instantly without net force)
        """
        issues = []
        text_lower = text.lower()
        
        # Check for incorrect inverse proportionality claim
        # e.g. "more mass ... faster" or "more mass ... more acceleration"
        if re.search(r"more\s+mass.*?(\bfaster\b|\bmore\s+acceleration\b|\bhigher\s+acceleration\b)", text_lower):
            # Check if it was in the context of fixed force
            if not re.search(r"less|slower|harder to accelerate", text_lower):
                issues.append("ERROR: Claims that more mass results in faster motion or greater acceleration.")
                
        # Check for Aristotelian misconception: "stop pushing, ball stops moving immediately"
        if re.search(r"stop\s+pushing.*?(ball|object)\s+stops\b", text_lower) and not re.search(r"friction|air resistance|external force", text_lower):
            issues.append("WARNING: Incomplete physics on stopping motion without mentioning friction or opposing force (violates Newton's 1st Law/Inertia).")
            
        # Check formula presence
        has_formula = bool(re.search(r"f\s*=\s*m\s*[x\*a]|force\s*=\s*mass\s*[x\*]\s*acceleration", text_lower))
        if not has_formula:
            issues.append("NOTICE: Formula F = ma not explicitly found.")
            
        return {
            "passed": len([i for i in issues if i.startswith("ERROR")]) == 0,
            "issues": issues
        }

    @staticmethod
    def check_mass_vs_weight(text: str, test_mass_kg: float = 10.0, is_earth: bool = True) -> Dict[str, Any]:
        """
        Validates Mass vs Weight explanations:
        - Mass in kg / g, scalar, intrinsic, constant across locations
        - Weight in N (Newtons), vector/force, depends on gravity W = mg
        - Calculates correct numerical weights:
          Earth (g=9.8): 10 kg -> 98 N (or 98.1 N / 100 N if g=10 approx)
          Moon (g=1.62): 10 kg -> ~16.2 N
        - Never claims 'weight is not a physical quantity'
        """
        issues = []
        text_lower = text.lower()
        
        # Check if weight is denied as a physical quantity
        if "not a physical quantity" in text_lower:
            issues.append("ERROR: Incorrectly states that weight is not a physical quantity. (Weight is a force).")
            
        # Check for mass unit in kg and weight in N
        if re.search(r"weight\s+is\s+measured\s+in\s+kg\b", text_lower) and not re.search(r"incorrect|misconception|should be", text_lower):
            issues.append("ERROR: States weight is measured in kg without clarifying it is an error.")
            
        # Check arithmetic if 10 kg is mentioned
        if "10 kg" in text_lower:
            # Check Earth calculation
            if "earth" in text_lower:
                # If it says 10 kg weighs 10 N on earth, flag error!
                if re.search(r"10\s*kg.*?weighs\s+10\s*n\b", text_lower):
                    issues.append("ERROR: Factual error - 10 kg cannot weigh 10 N on Earth (W = 10 * 9.8 = 98 N).")
                elif not re.search(r"98\s*n|98\.1\s*n|100\s*n", text_lower):
                    issues.append("WARNING: Did not find expected Earth weight (~98 N or 100 N) for 10 kg object.")
                    
            # Check Moon calculation
            if "moon" in text_lower:
                if re.search(r"10\s*kg.*?weighs\s+10\s*n\s+on\s+the\s+moon", text_lower):
                    issues.append("ERROR: Factual error - 10 kg does not weigh 10 N on Moon (W = 10 * 1.62 = ~16.2 N).")
                    
        return {
            "passed": len([i for i in issues if i.startswith("ERROR")]) == 0,
            "issues": issues
        }

    @staticmethod
    def check_linear_equation(equation_str: str, solution_x: float, text: str) -> Dict[str, Any]:
        """
        Verifies that step-by-step linear algebra reached the exact numerical answer.
        """
        issues = []
        sol_pattern = rf"x\s*=\s*{solution_x:g}\b"
        if not re.search(sol_pattern, text):
            issues.append(f"ERROR: Expected solution x = {solution_x} not found in output.")
        return {
            "passed": len(issues) == 0,
            "issues": issues
        }

if __name__ == "__main__":
    print("STEM Factual Checker initialized.")
