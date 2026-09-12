import json
import logging
from groq import Groq
from app.core.config import settings

logger = logging.getLogger(__name__)

groq_client = None
if settings.GROQ_API_KEY:
    try:
        groq_client = Groq(api_key=settings.GROQ_API_KEY)
        logger.info(f"Groq Client initialized with model {settings.GROQ_MODEL}")
    except Exception as e:
        logger.warning(f"Failed to initialize Groq client: {e}")

def call_llm_json(system_prompt: str, user_prompt: str, response_model: type):
    """
    Call Groq LLM (openai/gpt-oss-120b) with JSON formatting,
    mapping output fields dynamically to Pydantic response models.
    """
    if groq_client:
        try:
            # Provide explicit schema fields in system prompt
            schema_fields = getattr(response_model, "__fields__", None) or response_model.model_fields
            fields_str = ", ".join(schema_fields.keys())
            
            full_system_prompt = (
                f"{system_prompt}\n\n"
                f"CRITICAL: Output strictly valid JSON matching these exact keys: {fields_str}."
            )
            
            completion = groq_client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": full_system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            raw_json = completion.choices[0].message.content
            parsed_dict = json.loads(raw_json)

            # Map field aliases if present
            if "question" in parsed_dict and "question_text" not in parsed_dict:
                parsed_dict["question_text"] = parsed_dict.pop("question")
            if "reasoning" in parsed_dict and "context_reasoning" not in parsed_dict:
                parsed_dict["context_reasoning"] = parsed_dict.pop("reasoning")
            if "context_reasoning" not in parsed_dict:
                parsed_dict["context_reasoning"] = "Grounded in candidate resume evidence and role RAG context"
            if "difficulty" not in parsed_dict:
                parsed_dict["difficulty"] = "Medium"

            return response_model(**parsed_dict)
        except Exception as e:
            logger.warning(f"Groq API call fallback: {e}")
            raise e
    else:
        raise ValueError("Groq client not configured")
