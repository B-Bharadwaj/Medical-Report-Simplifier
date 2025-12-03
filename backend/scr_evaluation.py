from sentence_transformers import SentenceTransformer, util
import textstat

# NEW: Import the expanded clinical ontology
from backend.medical_terms import CRITICAL_MEDICAL_TERMS

# Load embedding model
embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# -------------------------
# 1. Semantic Similarity
# -------------------------
def compute_semantic_similarity(original: str, simplified: str) -> float:
    if not original.strip() or not simplified.strip():
        return 0.0

    emb1 = embed_model.encode(original, convert_to_tensor=True)
    emb2 = embed_model.encode(simplified, convert_to_tensor=True)

    similarity = util.cos_sim(emb1, emb2).item()
    return float(similarity)


# -------------------------
# 2. Contraction / Expansion
# -------------------------
def compute_contraction(original: str, simplified: str) -> float:
    orig_len = len(original.split())
    simp_len = len(simplified.split())

    # Allow simplified text to be slightly longer (≤ +20%)
    if simp_len <= orig_len * 1.2:
        return max((orig_len - simp_len) / orig_len, 0)

    # Penalize heavy expansion
    expansion_penalty = (simp_len / orig_len) - 1
    return max(expansion_penalty, 0)


# -------------------------
# 3. SCR Score
# -------------------------
def compute_scr(original: str, simplified: str) -> float:
    similarity = compute_semantic_similarity(original, simplified)
    contraction = compute_contraction(original, simplified)

    # If meaning is lost badly → score = 0
    if similarity < 0.15:
        return 0.0

    # Softer penalty when contraction is extreme
    if contraction >= 0.8:
        scr = similarity * 0.5
    else:
        scr = similarity * (1 - contraction)

    # Scale score up (makes interpretation easier)
    scr *= 2.0

    return float(scr)


# -------------------------
# 4. SCR Labels
# -------------------------
def interpret_scr(scr_value: float) -> str:
    if scr_value >= 0.75:
        return "excellent"
    elif scr_value >= 0.55:
        return "good"
    elif scr_value >= 0.35:
        return "weak"
    else:
        return "poor"


# -------------------------
# 5. Negation Safety
# -------------------------
NEGATION_TERMS = [
    "no", "not", "without", "absence of",
    "ruled out", "negative for", "free of",
    "does not show", "cannot be seen"
]

def check_negation_safety(original: str, simplified: str) -> bool:
    o = original.lower()
    s = simplified.lower()

    for term in NEGATION_TERMS:
        if term in o and term not in s:
            return False  # Dangerous negation loss

    return True


# -------------------------
# 6. Critical Info Loss (Ontology-Based)
# -------------------------
def detect_critical_info_loss(original: str, simplified: str):
    missing_terms = []

    original_lower = original.lower()
    simplified_lower = simplified.lower()

    for term in CRITICAL_MEDICAL_TERMS:
        if term in original_lower and term not in simplified_lower:
            missing_terms.append(term)

    return missing_terms


# -------------------------
# 7. Safe Rewrite System
# -------------------------
def enforce_safe_rewrite(original: str, simplified: str) -> str:
    """Ensures that no critical medical term is lost."""

    missing = detect_critical_info_loss(original, simplified)
    if not missing:
        return simplified  # Nothing to fix

    patient_friendly_definitions = {
        "lesion": "a small abnormal area of tissue (called a lesion)",
        "mass": "a lump or growth (called a mass)",
        "tumor": "a growth of cells (called a tumor)",
        "embolism": "a blood clot blocking a vessel (called an embolism)",
        "aneurysm": "a bulging weak spot in a vessel (called an aneurysm)",
        "fracture": "a broken bone (called a fracture)",
        "pneumothorax": "a collapsed lung (called a pneumothorax)",
        "hemorrhage": "bleeding inside the body (called a hemorrhage)",
        "metastasis": "cancer that has spread (called metastasis)",
    }

    corrections = []

    for term in missing:
        if term in patient_friendly_definitions:
            corrections.append(f"- The report also notes {patient_friendly_definitions[term]}.")
        else:
            corrections.append(f"- The report contains an important finding: '{term}'. Please ask a doctor for clarification.")

    correction_text = (
        "\n\n⚠️ Important information was missing in the simplified explanation.\n"
        "To ensure medical safety, the following key findings have been added:\n"
        + "\n".join(corrections)
    )

    return simplified + correction_text


# -------------------------
# 8. Public Evaluation Wrapper
# -------------------------
def evaluate_all(original: str, simplified: str) -> dict:
    return {
        "scr_score": round(compute_scr(original, simplified), 3),
        "scr_label": interpret_scr(compute_scr(original, simplified)),
        "negation_safe": check_negation_safety(original, simplified),
        "critical_terms_missing": detect_critical_info_loss(original, simplified),
        "readability_grade": textstat.flesch_kincaid_grade(simplified)
    }
