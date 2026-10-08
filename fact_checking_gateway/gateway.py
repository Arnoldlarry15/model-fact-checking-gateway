import re
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class VerifiedStatement:
    statement_id: int
    assertion: str
    verified: bool
    confidence_score: float
    supporting_reference: str

@dataclass
class GatewayVerificationReport:
    total_assertions: int
    verified_assertions: int
    faithfulness_score: float
    is_approved: bool
    statements: List[VerifiedStatement] = field(default_factory=list)

class FactCheckingGateway:
    """Verifies atomic factual assertions in model outputs against trusted knowledge bases."""

    def __init__(self, verification_threshold: float = 0.55):
        self.threshold = verification_threshold

    def verify_output(self, generated_text: str, knowledge_base: Dict[str, str]) -> GatewayVerificationReport:
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", generated_text.strip()) if s.strip()]
        statements = []
        verified_count = 0

        combined_kb = " ".join(knowledge_base.values()).lower()
        kb_words = set(re.findall(r"\w+", combined_kb))

        for idx, s in enumerate(sentences, start=1):
            s_words = set(re.findall(r"\w+", s.lower()))
            stopwords = {"the", "and", "that", "this", "with", "for", "are", "can", "you", "from"}
            clean_words = s_words - stopwords

            if not clean_words:
                score = 1.0
            else:
                matches = len(clean_words.intersection(kb_words))
                score = matches / len(clean_words)

            is_ver = score >= self.threshold
            if is_ver:
                verified_count += 1
                ref = "VERIFIED_AGAINST_KNOWLEDGE_BASE"
            else:
                ref = "UNSUPPORTED_OR_DRIFTED_ASSERTION"

            statements.append(VerifiedStatement(
                statement_id=idx,
                assertion=s,
                verified=is_ver,
                confidence_score=score,
                supporting_reference=ref
            ))

        tot = len(sentences)
        f_score = (verified_count / tot) if tot else 1.0
        approved = f_score >= 0.70

        return GatewayVerificationReport(
            total_assertions=tot,
            verified_assertions=verified_count,
            faithfulness_score=f_score,
            is_approved=approved,
            statements=statements
        )
