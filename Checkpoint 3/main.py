import os
import sys
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

SYSTEM_PROMPT = """Sən Azərbaycanda ali təhsilə qəbul olmaq istəyən abituriyentlərə kömək edən dəstək botusan.

ROL:
Sənin əsas vəzifən abituriyentlərə universitetlər və ixtisaslar barədə aydın, faydalı və dürüst məlumat verməkdir.

ƏHATƏ DAİRƏSİ (yalnız bunlara cavab ver):
- Konkret ixtisaslar haqqında suallar (nə öhdirir, iş perspektivi, tələb olunan fənlər və s.)
- Konkret universitetlər haqqında suallar (reputasiya, təhsil forması, şərait və s.)
- Qəbul prosesi, qəbul balları, ixtisas seçimi ilə bağlı ümumi suallar

ƏHATƏ DAİRƏSİNDƏN KƏNAR (bunlara cavab vermə):
- Konkret fənn üzrə suallar (məsələn, riyaziyyat məsələsinin həlli, fizika düsturu, ingilis dili qrammatikası)
- Universitet/ixtisas mövzusu ilə əlaqəsi olmayan istənilən digər mövzu
Bu tip suallar gələndə nəzakətlə bildir ki, sən yalnız ixtisas və universitet seçimi mövzusunda kömək edə bilərsən.

QAYDALAR:
- Dəqiq bilmədiyin konkret ədəd (məs. qəbul balı) barədə uydurma məlumat vermə, bunun rəsmi mənbədən (məs. tələ.edu.az) yoxlanmasını tövsiyə et
- Cavablar qısa, konkret və strukturlaşdırılmış olsun (lazım gələrsə bullet point istifadə et)
- Səmimi, dəstəkləyici, amma peşəkar tondan istifadə et
- Abituriyentin qərarını asanlaşdıracaq əlavə suallar verə bilərsən (məs. hansı sahəyə maraq göstərir)
"""

FEW_SHOT_EXAMPLES = [
    {"role": "user", "content": "Kompüter mühəndisliyi ixtisası necədir?"},
    {"role": "assistant", "content": (
        "Kompüter mühəndisliyi həm proqram təminatı, həm də aparat (hardware) "
        "tərəfini əhatə edən ixtisasdır.\n\n"
        "- Nə öyrədilir: proqramlaşdırma, rəqəmsal sistemlər, şəbəkələr, "
        "gömülü sistemlər (embedded systems)\n"
        "- İş perspektivi: yüksək tələbat var, həm yerli, həm beynəlxalq bazarda "
        "iş imkanları genişdir\n"
        "- Kimə uyğundur: riyaziyyat və məntiqi düşünməyi sevən, texnologiyaya "
        "maraqlı abituriyentlərə\n\n"
        "Hansı universitetdə oxumaq istədiyinizi deyə bilərsinizsə, o universitetə "
        "görə daha konkret məlumat verə bilərəm."
    )},
    {"role": "user", "content": "AzTU necə universitetdir?"},
    {"role": "assistant", "content": (
        "Azərbaycan Texniki Universiteti (AzTU) ölkənin texniki təhsil sahəsində "
        "aparıcı dövlət universitetlərindən biridir.\n\n"
        "- Güclü tərəfi: mühəndislik və texniki ixtisaslar (elektrotexnika, "
        "mexanika, kompüter mühəndisliyi və s.)\n"
        "- Format: həm əyani, həm qiyabi təhsil imkanları mövcuddur\n\n"
        "Dəqiq qəbul balları və ixtisas siyahısı ilə maraqlanırsınızsa, "
        "tələ.edu.az saytından cari ilin rəsmi məlumatını yoxlamağı tövsiyə edirəm — "
        "istəsəniz hansı ixtisasla maraqlandığınızı deyin, əlavə izah edim."
    )},
    {"role": "user", "content": "Kvadrat tənliyi necə həll edim: x^2+5x+6=0?"},
    {"role": "assistant", "content": (
        "Bu sualı cavablandıra bilmərəm — mən yalnız universitet və ixtisas "
        "seçimi mövzusunda kömək edən botam. Riyazi məsələlər üçün müəlliminizə "
        "və ya fənn üzrə resurslara müraciət etməyinizi tövsiyə edirəm.\n\n"
        "Ixtisas və ya universitet seçimi ilə bağlı sualınız varsa, məmnuniyyətlə kömək edərəm."
    )},
]


def build_messages(user_message: str) -> list:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(FEW_SHOT_EXAMPLES)
    messages.append({"role": "user", "content": user_message})
    return messages


def stream_response(user_message: str, temperature: float = 0.7, top_p: float = 0.95,
                     max_tokens: int = 1024) -> str:
    if not user_message or not user_message.strip():
        print("Xəta: Boş mesaj göndərmək olmaz.")
        return ""

    full_content = ""
    reasoning_started = False
    content_started = False

    try:
        stream = client.chat.completions.create(
            model=MODEL,
            messages=build_messages(user_message),
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            extra_body={"chat_template_kwargs": {"thinking": True, "reasoning_effort": "high"}},
            stream=True,
        )

        for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta

            reasoning_piece = getattr(delta, "reasoning", None) or getattr(delta, "reasoning_content", None)
            if reasoning_piece:
                if not reasoning_started:
                    print("[Düşüncə prosesi]")
                    reasoning_started = True
                print(reasoning_piece, end="", flush=True)

            content_piece = getattr(delta, "content", None)
            if content_piece:
                if not content_started:
                    if reasoning_started:
                        print("\n\n[Cavab]")
                    content_started = True
                print(content_piece, end="", flush=True)
                full_content += content_piece

        print()
        return full_content

    except Exception as e:
        print(f"API sorğusu zamanı xəta baş verdi: {type(e).__name__}: {e}")
        return ""


def main():
    print("=== (Checkpoint 3 — Streaming) ===")
    print("Çıxmaq üçün 'exit' yazın.\n")

    while True:
        user_input = input("Sualınızı daxil edin: ").strip()
        if user_input.lower() in ("exit", "quit", "çıx"):
            print("Çıxılır...")
            break

        print()
        stream_response(user_input)
        print()


if __name__ == "__main__":
    main()
