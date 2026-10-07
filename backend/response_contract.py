"""
backend/response_contract.py
Stable Response & Event Protocol for SHIKSHA Offline AI Tutor.
Designed for seamless consumption by Flutter / Native Android frontends.
Exposes:
- Standard request & response structures
- Streaming chunk protocol
- Structured pedagogical parsing (steps, final answer, answer type)
- Real runtime performance metrics (no fabricated numbers)
"""

import re
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict

@dataclass
class RuntimeMetrics:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    tokens_per_second: float = 0.0
    prompt_tokens_per_second: float = 0.0
    load_time_ms: float = 0.0
    latency_ms: float = 0.0

@dataclass
class TutoringMetadata:
    answer_type: str = "general_academic"  # numerical_step_by_step, conceptual_explanation, misconception_correction, scope_refusal
    subject: Optional[str] = None
    grade: Optional[int] = None
    given: Optional[str] = None
    formula: Optional[str] = None
    steps: List[str] = field(default_factory=list)
    verification: Optional[str] = None
    final_answer: Optional[str] = None
    summary: Optional[str] = None

@dataclass
class InferenceResponse:
    request_id: str
    status: str  # "completed", "generating", "cancelled", "error"
    content: str
    done: bool = True
    error: Optional[str] = None
    metadata: Optional[TutoringMetadata] = None
    metrics: Optional[RuntimeMetrics] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d

@dataclass
class InferenceStreamChunk:
    request_id: str
    status: str  # "generating", "completed", "cancelled", "error"
    delta: str
    accumulated: str
    done: bool
    error: Optional[str] = None
    metadata: Optional[TutoringMetadata] = None
    metrics: Optional[RuntimeMetrics] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class StructuredTutorParser:
    """Parses model output into structured pedagogical components for rich UI display in Flutter."""
    
    @staticmethod
    def parse(content: str, grade: Optional[int] = None, subject: Optional[str] = None) -> TutoringMetadata:
        meta = TutoringMetadata(grade=grade, subject=subject)
        
        # 1. Detect scope refusal
        if any(term in content.lower() for term in ["outside the scope", "outside of the class", "curriculum topics"]):
            meta.answer_type = "scope_refusal"
            meta.summary = content.strip()
            return meta
            
        # 2. Detect misconception correction
        if "scientifically incorrect" in content.lower() or "statement is scientifically" in content.lower():
            meta.answer_type = "misconception_correction"
            
        # 3. Detect numerical / step-by-step
        elif "given:" in content.lower() or "formula:" in content.lower() or "final answer:" in content.lower():
            meta.answer_type = "numerical_step_by_step"
            
        # 4. Detect conceptual explanation
        elif "definition:" in content.lower() or "explanation:" in content.lower():
            meta.answer_type = "conceptual_explanation"
            
        # Parse fields
        lines = content.splitlines()
        current_section = None
        current_text = []
        
        section_map = {
            "given": "given",
            "required": "required",
            "formula": "formula",
            "calculation": "calculation",
            "verification": "verification",
            "final answer": "final_answer",
            "definition": "definition",
            "summary": "summary"
        }
        
        extracted = {}
        for line in lines:
            line_str = line.strip()
            matched_header = None
            for h in section_map:
                if line_str.lower().startswith(h + ":"):
                    matched_header = h
                    break
                    
            if matched_header:
                if current_section and current_text:
                    extracted[current_section] = "\n".join(current_text).strip()
                current_section = section_map[matched_header]
                remainder = line_str[len(matched_header) + 1:].strip()
                current_text = [remainder] if remainder else []
            else:
                if current_section:
                    current_text.append(line)
                    
        if current_section and current_text:
            extracted[current_section] = "\n".join(current_text).strip()
            
        if "given" in extracted:
            meta.given = extracted["given"]
        if "formula" in extracted:
            meta.formula = extracted["formula"]
        if "final_answer" in extracted:
            meta.final_answer = extracted["final_answer"]
        if "verification" in extracted:
            meta.verification = extracted["verification"]
        if "summary" in extracted:
            meta.summary = extracted["summary"]
            
        # Extract steps
        if "calculation" in extracted:
            calc_text = extracted["calculation"]
            step_matches = re.findall(r"(?:Step\s*\d+:|\d+\.)\s*([^\n]+)", calc_text)
            if step_matches:
                meta.steps = [s.strip() for s in step_matches]
            else:
                meta.steps = [calc_text.strip()]
                
        return meta
