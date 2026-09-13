from openai import OpenAI
from config import (
    LLM_PROVIDER,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    TEMPERATURE,
)

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

def get_client():
    if LLM_PROVIDER == "gemini":
        if not GEMINI_API_KEY:
            raise RuntimeError(
                "沒有設定 GEMINI_API_KEY。請在 .env 中設定你的 Gemini API key。"
            )

        # Gemini provides an OpenAI-compatible endpoint.
        return OpenAI(
            api_key=GEMINI_API_KEY,
            base_url=GEMINI_BASE_URL,
        )

    if LLM_PROVIDER == "ollama":
        return OpenAI(
            base_url=OLLAMA_BASE_URL,
            api_key="ollama"
        )

    if LLM_PROVIDER == "openai":
        if not OPENAI_API_KEY:
            raise RuntimeError(
                "沒有設定 OPENAI_API_KEY。請在 .env 中設定，或改用 Gemini / Ollama。"
            )

        return OpenAI(api_key=OPENAI_API_KEY)

    raise RuntimeError(
        f"不支援的 LLM_PROVIDER: {LLM_PROVIDER}。"
        "請使用 gemini、openai 或 ollama。"
    )

def get_model():
    if LLM_PROVIDER == "gemini":
        return GEMINI_MODEL
    if LLM_PROVIDER == "ollama":
        return OLLAMA_MODEL
    return OPENAI_MODEL

def generate(system_prompt, messages):
    client = get_client()

    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": system_prompt},
            *messages
        ],
        temperature=TEMPERATURE,
    )

    content = response.choices[0].message.content

    if not content:
        raise RuntimeError("模型沒有回傳文字內容。")

    return content.strip()
