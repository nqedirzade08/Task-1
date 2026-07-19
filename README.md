# Task 1 — Abituriyent Dəstək Botu (LLM Əsaslı Tətbiq)

## Layihənin izahı

Bu layihə Azərbaycanda ali təhsilə qəbul olmaq istəyən abituriyentlərə **universitet və ixtisas seçimi** mövzusunda kömək edən LLM-əsaslı dəstək botudur. Bot NVIDIA-nın hosted API-si (`integrate.api.nvidia.com`) üzərindən DeepSeek V4 Flash modelinə qoşulur və terminal interfeysi vasitəsilə istifadə olunur.

Botun məqsədli əhatə dairəsi bilərəkdən dar saxlanıb: yalnız konkret ixtisaslar, konkret universitetlər və qəbul prosesi ilə bağlı suallara cavab verir; fənn üzrə suallar (məsələn, riyaziyyat məsələsinin həlli) və mövzudan kənar sorğular nəzakətlə rədd edilir. Bu, system prompt səviyyəsində, few-shot nümunələrlə gücləndirilərək təmin olunub.

Layihə 6 ardıcıl checkpoint üzərində tədricən qurulub — hər checkpoint əvvəlkinin üzərinə yeni bir mühəndislik təcrübəsini (prompt engineering, streaming, xəta idarəetməsi, çıxış validasiyası, cost tracking) əlavə edib. Aşağıda hər checkpoint-in nə əlavə etdiyi qeyd olunub.

## Texnologiya seçimi

- **Dil:** Python
- **LLM provayder:** NVIDIA API (OpenAI-uyğun endpoint), model: `deepseek-ai/deepseek-v4-flash`
- **Kitabxanalar:** `openai` (rəsmi Python SDK, NVIDIA-nın OpenAI-uyğun endpoint-i ilə işləyir), `python-dotenv` (mühit dəyişənləri üçün)
- **İnterfeys:** Terminal/CLI (sadə, asılılıqsız, qiymətləndirməyə uyğun)

## Checkpoint-lər üzrə inkişaf

### Checkpoint 1 — API İnteqrasiyası (100 bal)
NVIDIA API-yə əsas qoşulma quruldu. `.env` faylından `python-dotenv` ilə API key oxunur (heç vaxt kodda hardcode edilmir). Boş mesaj yoxlanışı və əsas `try/except` bloku ilə ilk xəta idarəetməsi əlavə olundu.

### Checkpoint 2 — Prompt Engineering (25 bal)
Strukturlaşdırılmış system prompt (ROL / ƏHATƏ DAİRƏSİ / QAYDALAR bölmələri) və 3 few-shot nümunə əlavə olundu. Nümunələrdən biri məhz botun **əhatə dairəsindən kənar sualları necə rədd etdiyini** göstərir ki, model bu davranışı real sorğularda da təkrarlasın.

### Checkpoint 3 — Streaming Cavab İdarəetməsi (15 bal)
`stream=True` ilə API sorğusu göndərilir, model cavabı yaratdıqca token-token ekrana yazılır (`print(..., end="", flush=True)`). Modelin "düşüncə prosesi" (reasoning) və əsas cavabı ayrı-ayrı axın kimi göstərilir.

### Checkpoint 4 — Xəta İdarəetməsi + İlkin Strukturlaşdırılmış Çıxış (15 bal)
Xətalar iki qrupa bölündü:
- **Retry-lanan** (rate limit, timeout, server xətası) — exponential backoff ilə (1.5s → 3s → 6s) avtomatik yenidən cəhd
- **Retry-lanmayan** (auth, bad request) — dərhal aydın mesajla dayanma

Paralel olaraq, modeldən JSON formatında strukturlaşdırılmış cavab (sualın kateqoriyası + qısa cavab) istənilən yeni funksiya əlavə olundu, ilk dəfə JSON parse cəhdi və sadə retry məntiqi ilə.

### Checkpoint 5 — Çıxış Parsing/Validasiyası (20 bal)
JSON emalı iki qatlı sistemə çevrildi:
1. **Parsing** — markdown kod blokunu təmizləmə, birbaşa parse, uğursuz olsa regex ilə `{...}` çıxarma
2. **Schema validasiyası** — bütün tələb olunan sahələrin mövcudluğu, tiplərin düzgünlüyü, icazə verilən dəyərlərin yoxlanması

Modelin həmişə "təmiz" JSON qaytaracağı fərz edilmədi — bunu sübut etmək üçün 9 edge-case-dən ibarət **offline test dəsti** yazıldı (yarımçıq JSON, çatışmayan sahə, yanlış tip, etibarsız dəyər və s.), API-yə müraciət etmədən deterministik şəkildə işləyir və `test:parsing` əmri ilə istənilən vaxt işə salına bilər.

### Checkpoint 6 — Token/Xərc Loglaması (10 bal)
Hər sorğu üçün token istifadəsi (`prompt_tokens`, `completion_tokens`, `total_tokens`) həm konsola çap olunur, həm də `usage_log.jsonl` faylına strukturlaşdırılmış şəkildə yazılır. Sorğu başına təxmini dollar xərci hesablanır (`.env`-də konfiqurasiya edilə bilən tarif ilə — NVIDIA-nın hazırkı pulsuz/trial API-si üçün rəsmi qiymət mövcud olmadığından, bu, metodologiyanı göstərən nümunə tarifdir). Sessiya boyu cəmlənmiş istifadə `usage:summary` əmri ilə göstərilir.

## Ümumi təhlükəsizlik təcrübəsi

Bütün 6 checkpoint boyu eyni prinsip qorunub:
- API key yalnız `.env` faylındadır, kodda heç vaxt açıq yazılmayıb
- `.gitignore` `.env` faylını bütün checkpoint qovluqlarında istisna edir
- Hər checkpoint-in `.env.example` faylında yalnız placeholder dəyər var, real key yoxdur
- Push-dan əvvəl **Gitleaks** aləti ilə repository skan edilib, real key-in heç bir committed fayla düşmədiyi təsdiqlənib

## Qovluq strukturu (bu repository)

```
Task 1/
├── Checkpoint 1/    — API inteqrasiyası
├── Checkpoint 2/    — Prompt engineering
├── Checkpoint 3/    — Streaming
├── Checkpoint 4/    — Xəta idarəetməsi + ilkin JSON çıxış
├── Checkpoint 5/    — Çıxış parsing/validasiyası
└── Checkpoint 6/    — Token/xərc loglaması
```

Hər checkpoint qovluğu özündə tam işlək, müstəqil işə salına bilən layihə saxlayır (`main.py`, `.env.example`, `.gitignore`, `requirements.txt`, `README.md`) — sonrakı checkpoint əvvəlkinin üzərinə qurulsa da, hər biri ayrıca test edilib və sənədləşdirilib.

## İşə salma (istənilən checkpoint qovluğu üçün eyni)

```bash
cd "Checkpoint N"
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env         # sonra .env-də öz API key-inizi yazın
python main.py
```

Ətraflı izah və nümunə sorğu/cavab log-ları hər checkpoint-in öz `README.md` faylındadır.
