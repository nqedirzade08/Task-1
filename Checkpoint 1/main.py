import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("NVIDIA_API_KEY")
BASE_URL = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
MODEL = os.getenv("NVIDIA_MODEL", "deepseek-ai/deepseek-v4-flash")

if not API_KEY:
    raise ValueError(
        "NVIDIA_API_KEY tapılmadı. Zəhmət olmasa .env faylını yaradın "
        "və içinə NVIDIA_API_KEY=sizin_key_iniz yazın."
    )

client = OpenAI(base_url=BASE_URL, api_key=API_KEY, timeout=180, max_retries=2)


def get_response(user_message: str, temperature: float = 1, top_p: float = 0.95,
                  max_tokens: int = 16384) -> str:
    if not user_message or not user_message.strip():
        return "Xəta: Boş mesaj göndərmək olmaz."

    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": user_message}],
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            extra_body={"chat_template_kwargs": {"thinking": True, "reasoning_effort": "high"}},
            stream=False,
        )

        message = completion.choices[0].message
        reasoning = getattr(message, "reasoning", None) or getattr(message, "reasoning_content", None)

        if reasoning:
            return f"[Düşüncə prosesi]\n{reasoning}\n\n[Cavab]\n{message.content}"
        return message.content

    except Exception as e:
        return f"API sorğusu zamanı xəta baş verdi: {type(e).__name__}: {e}"


def main():
    print("=== LLM Əsaslı Tətbiq (Checkpoint 1) ===")
    print("Çıxmaq üçün 'exit' yazın.\n")

    while True:
        user_input = input("Sualınızı daxil edin: ").strip()
        if user_input.lower() in ("exit", "quit", "çıx"):
            print("Çıxılır...")
            break

        print("Sorğu göndərilir, gözləyin...")
        response = get_response(user_input)
        print(f"\nCavab:\n{response}\n")


if __name__ == "__main__":
    main()
