from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import json

load_dotenv()

# ── Initialize Groq LLM ───────────────────────────────────

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0,        # 0 = consistent, deterministic output
    max_tokens=500
)

# ── Prompt ────────────────────────────────────────────────

CLASSIFICATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an AI agent for Indian Railways grievance system.
Your job is to classify passenger complaints.

CATEGORIES (pick exactly one):
- AC: Air conditioning issues
- CLEANLINESS: Dirty coaches, toilets, platforms
- SAFETY: Sparks, fire, electrical issues, assault, theft — anything dangerous
- DELAY: Train late, schedule issues
- CATERING: Food quality, pantry car issues
- OTHER: Anything that doesn't fit above

SEVERITY RULES (pick exactly one):
- CRITICAL: Safety risk to life (fire, sparks, assault, medical emergency)
- HIGH: Major discomfort affecting many passengers (AC failure entire coach, no water)
- MEDIUM: Significant issue but manageable (dirty toilet, poor food)
- LOW: Minor inconvenience (small delay, single seat issue)

LANGUAGE DETECTION:
- Detect if complaint is in Hindi or English
- If Hindi, translate it to English first, then classify

Respond ONLY with this exact JSON format, nothing else:
{{
  "category": "CATEGORY_HERE",
  "severity": "SEVERITY_HERE",
  "detected_language": "Hindi" or "English",
  "translated_text": "English version of complaint (same as input if already English)",
  "reasoning": "One sentence explaining your classification"
}}"""),
    ("human", "Complaint: {complaint_text}")
])

# ── Chain ─────────────────────────────────────────────────

classification_chain = CLASSIFICATION_PROMPT | llm

# ── Main function ─────────────────────────────────────────

def classify_complaint(complaint_text: str) -> dict:
    """
    Takes raw complaint text, returns classification dict.
    
    Args:
        complaint_text: Raw complaint in English or Hindi
        
    Returns:
        dict with category, severity, detected_language, 
        translated_text, reasoning
    """
    try:
        response = classification_chain.invoke({
            "complaint_text": complaint_text
        })
        
        # Parse JSON from LLM response
        raw = response.content.strip()
        
        # Clean up if LLM wraps in markdown code blocks
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        
        result = json.loads(raw.strip())
        return result
    
    except json.JSONDecodeError:
        # Fallback if LLM doesn't return valid JSON
        return {
            "category": "OTHER",
            "severity": "LOW",
            "detected_language": "English",
            "translated_text": complaint_text,
            "reasoning": "Could not parse classification, defaulting to OTHER/LOW"
        }
    except Exception as e:
        return {
            "category": "OTHER",
            "severity": "LOW", 
            "detected_language": "English",
            "translated_text": complaint_text,
            "reasoning": f"Error: {str(e)}"
        }


# ── Quick test (run this file directly to test) ───────────

if __name__ == "__main__":
    test_complaints = [
        "There are sparks coming from the electrical panel in coach S3",
        "AC is not working in our compartment since last 3 hours",
        "AC kaam nahi kar raha hai coach B2 mein",
        "Food served in pantry car was cold and stale",
        "Train is running 2 hours late",
    ]
    
    print("Testing Classification Agent...\n")
    for complaint in test_complaints:
        print(f"Input: {complaint}")
        result = classify_complaint(complaint)
        print(f"Result: {json.dumps(result, indent=2)}")
        print("-" * 60)