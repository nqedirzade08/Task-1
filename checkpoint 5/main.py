import os
import json
import re
import time
from dotenv import load_dotenv
from openai import (
    OpenAI,
    RateLimitError,
    APITimeoutError,
    APIConnectionError,
    InternalServerError,
    AuthenticationError,
    BadRequestError,
)

load_dotenv()

API_KEY = os.getenv("NVIDIA_API_KEY")
BASE_URL = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
MODEL = os.getenv("NVIDIA_MODEL", "deepseek-ai/deepseek-v4-flash")

if not API_KEY:
    raise ValueError(
        "NVIDIA_API_KEY tapılmadı. Zəhmət olmasa .env faylını yaradın "
        "və içinə NVIDIA_API_KEY=sizin_key_iniz yazın."
    )

client = OpenAI(base_url=BASE_URL, api_key=API_KEY, timeout=60, max_retries=0)

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

RETRYABLE_EXCEPTIONS = (RateLimitError, APITimeoutError, APIConnectionError, InternalServerError)


def build_messages(user_message: str, system_prompt: str = SYSTEM_PROMPT, few_shot: list = None) -> list:
    messages = [{"role": "system", "content": system_prompt}]
    if few_shot:
        messages.extend(few_shot)
    messages.append({"role": "user", "content": user_message})
    return messages


def call_with_retry(request_fn, max_attempts: int = 4, base_delay: float = 1.5, on_retry=None):
    last_error = None
    for attempt in range(1, max_attempts + 1):
        try:
            return request_fn(), None
        except (AuthenticationError, BadRequestError) as e:
            return None, f"Xəta (təkrar cəhd edilmir): {type(e).__name__}: {e}"
        except RETRYABLE_EXCEPTIONS as e:
            last_error = e
            if attempt == max_attempts:
                break
            delay = base_delay * (2 ** (attempt - 1))
            if on_retry:
                on_retry(e, attempt, max_attempts - 1, delay)
            time.sleep(delay)
        except Exception as e:
            return None, f"Gözlənilməz xəta: {type(e).__name__}: {e}"

    return None, f"Bütün cəhdlər uğursuz oldu: {type(last_error).__name__}: {last_error}"


def stream_response(user_message: str, temperature: float = 0.7, top_p: float = 0.95,
                     max_tokens: int = 1024) -> str:
    if not user_message or not user_message.strip():
        print("Xəta: Boş mesaj göndərmək olmaz.")
        return ""

    def request_fn():
        full_content = ""
        reasoning_started = False
        content_started = False

        stream = client.chat.completions.create(
            model=MODEL,
            messages=build_messages(user_message, few_shot=FEW_SHOT_EXAMPLES),
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

    def on_retry(error, attempt, max_retry_attempts, delay):
        print(f"\n[Xəbərdarlıq] {type(error).__name__} baş verdi, {delay:.1f} saniyədən sonra "
              f"{attempt}/{max_retry_attempts} təkrar cəhd edilir (axın yenidən başlayır)...\n")

    result, error = call_with_retry(request_fn, on_retry=on_retry)
    if error:
        print(error)
        return ""
    return result


def extract_json(raw_text: str):
    try:
        return json.loads(raw_text)
    except (json.JSONDecodeError, TypeError):
        pass

    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return None


JSON_SYSTEM_PROMPT = """Sən abituriyent suallarını təhlil edən strukturlaşdırılmış təsnifat sistemisən.

Hər istifadəçi sorğusu üçün YALNIZ aşağıdakı JSON formatında cavab ver, başqa heç bir mətn, izahat, markdown kod bloku (```), yaxud əlavə şərh əlavə etmə:

{"kateqoriya": "ixtisas" | "universitet" | "kənar", "qisa_cavab": "1-2 cümləlik qısa cavab", "yonlendirme_lazimdir": true | false}

Qaydalar:
- "kateqoriya": sual ixtisasla bağlıdırsa "ixtisas", universitetlə bağlıdırsa "universitet", əhatə dairəsindən kənardırsa (fənn sualı və s.) "kənar"
- "yonlendirme_lazimdir": kateqoriya "kənar" olduqda true, əks halda false
- Cavabın YALNIZ JSON obyektindən ibarət olmalıdır, əvvəlində/sonunda heç nə olmamalıdır
"""


def get_structured_response(user_message: str, max_json_attempts: int = 3) -> dict:
    if not user_message or not user_message.strip():
        return {"error": "Boş mesaj göndərmək olmaz."}

    current_prompt = JSON_SYSTEM_PROMPT
    raw_result = ""

    for json_attempt in range(1, max_json_attempts + 1):

        def request_fn():
            completion = client.chat.completions.create(
                model=MODEL,
                messages=build_messages(user_message, system_prompt=current_prompt),
                temperature=0.3,
                top_p=0.9,
                max_tokens=300,
                extra_body={"chat_template_kwargs": {"thinking": False}},
                stream=False,
            )
            return completion.choices[0].message.content

        def on_retry(error, attempt, max_retry_attempts, delay):
            print(f"[Xəbərdarlıq] {type(error).__name__} baş verdi, {delay:.1f} saniyədən sonra "
                  f"{attempt}/{max_retry_attempts} təkrar cəhd edilir...")

        raw_result, error = call_with_retry(request_fn, on_retry=on_retry)
        if error:
            return {"error": error}

        parsed = extract_json(raw_result)

        if parsed is not None and "kateqoriya" in parsed:
            return parsed

        print(f"[Xəbərdarlıq] JSON validasiyası uğursuz oldu (cəhd {json_attempt}/{max_json_attempts}), "
              f"model formatı pozub: {raw_result[:120]!r}")

        current_prompt = JSON_SYSTEM_PROMPT + (
            "\n\nDİQQƏT: əvvəlki cavabın formatı YANLIŞ idi. Sənin cavabın YALNIZ "
            "{ ilə başlayıb } ilə bitməlidir, başqa heç bir simvol olmamalıdır."
        )

    return {"error": f"{max_json_attempts} cəhddən sonra da düzgün JSON alına bilmədi.",
            "son_xam_cavab": raw_result}


def main():
    print("=== (Checkpoint 4 — Xəta idarəetməsi + Strukturlaşdırılmış çıxış) ===")
    print("Adi cavab üçün sualınızı yazın. JSON test rejimi üçün 'json:' prefiksi ilə yazın.")
    print("Çıxmaq üçün 'exit' yazın.\n")

    while True:
        user_input = input("Sualınızı daxil edin: ").strip()
        if user_input.lower() in ("exit", "quit", "çıx"):
            print("Çıxılır...")
            break

        if user_input.lower().startswith("json:"):
            query = user_input[5:].strip()
            print("Strukturlaşdırılmış sorğu göndərilir...")
            result = get_structured_response(query)
            print(f"\nJSON nəticə:\n{json.dumps(result, ensure_ascii=False, indent=2)}\n")
        else:
            print()
            stream_response(user_input)
            print()


if __name__ == "__main__":
    main()
