# Checkpoint 4 (Xəta İdarəetməsi + Strukturlaşdırılmış Çıxış)

Bu checkpoint əvvəlki versiyanın üzərinə iki yeni imkan əlavə edir: **xəta idarəetməsi** (məsələn, API açarının səhv olması, şəbəkə problemi və s. hallarda tətbiqin qəflətən çökməməsi) və **strukturlaşdırılmış (JSON formatlı) çıxış** — istəyə əsasən cavabın sərbəst mətn əvəzinə maşın tərəfindən oxuna bilən JSON formatında qaytarılması.

## 📋 Xüsusiyyətlər

- Terminal üzərindən interaktiv sual-cavab rejimi
- NVIDIA API vasitəsilə LLM-ə sorğu göndərilməsi
- Streaming cavab: model tokeni yaratdıqca ekrana real vaxtda yazılır
- **Xəta idarəetməsi**: şəbəkə xətası, yanlış API açarı və digər gözlənilməz hallarda tətbiq çökmür, istifadəçiyə anlaşılan mesaj göstərilir
- **Strukturlaşdırılmış (JSON) çıxış**: sualın əvvəlinə `json:` yazmaqla cavabı JSON formatında almaq mümkündür
- Modelin düşüncə prosesinin (`[Düşüncə prosesi]`) və son cavabının (`[Cavab]`) ayrı-ayrı göstərilməsi (adi rejimdə)
- Mövzu məhdudlaşdırması: bot yalnız universitet, ixtisas seçimi və qəbul prosesi mövzularında cavab verir
- `exit` əmri ilə proqramdan çıxış imkanı

## ⚙️ Quraşdırma

### 1. Virtual mühit yaradın

```bash
python -m venv venv
venv\Scripts\activate
```

> Qeyd: Yuxarıdakı aktivasiya əmri Windows üçündür. macOS/Linux istifadəçiləri `source venv/bin/activate` əmrindən istifadə etməlidir.

### 2. Asılılıqları yükləyin

```bash
pip install -r requirements.txt
```

### 3. Mühit dəyişənlərini konfiqurasiya edin

`.env.example` faylını `.env` adı ilə kopyalayın:

```bash
cp .env.example .env
```

Sonra `.env` faylını açıb `NVIDIA_API_KEY` dəyərini öz real API açarınızla əvəz edin:

```
NVIDIA_API_KEY=sizin_api_acariniz
```

### 4. Tətbiqi işə salın

```bash
python main.py
```

### 5. Strukturlaşdırılmış (JSON) çıxış üçün

Sualınızın əvvəlinə `json:` prefiksini əlavə edin. Məsələn:

```
json:ADNSU necə universitetdir?
```

## 🚀 İstifadə

Proqram işə düşdükdən sonra terminalda sualınızı yazıb Enter düyməsinə basın:

- **Adi sorğu** — cavab `[Düşüncə prosesi]` və `[Cavab]` bölmələri ilə, sərbəst mətn formatında, streaming şəklində göstərilir.
- **`json:` prefiksli sorğu** — cavab birbaşa strukturlaşdırılmış JSON obyekti kimi qaytarılır.

Yeni sual verə, ya da `exit` yazaraq proqramdan çıxa bilərsiniz.

### Nümunə sessiya

**Adi sorğu:** `ADNSU necə universitetdir?`

```
[Düşüncə prosesi]
Azərbaycan Dövlət Neft və Sənaye Universiteti (ADNSU) haqqında soruşur...
ADNSU-nun əsas güclü tərəfləri neft-qaz, kimya mühəndisliyi, energetika və
sənaye sahələrindədir...

[Cavab]
Azərbaycan Dövlət Neft və Sənaye Universiteti (ADNSU) ölkənin ən qədim texniki
universitetlərindən biridir.
- Güclü tərəfləri: neft-qaz mühəndisliyi, kimya texnologiyası, energetika,
  geologiya və sənaye sahələrində tanınmışdır
- Təhsil forması: əyani, qiyabi və magistratura səviyyəsində təhsil imkanı var
- Beynəlxalq əlaqələr: xarici universitetlərlə birgə proqramlar və təcrübə
  mübadiləsi mövcuddur

Hansı ixtisasla maraqlandığınızı desəniz, həmin istiqamət üzrə daha konkret
məlumat verə bilərəm. Qəbul balları üçün rəsmi mənbə kimi tələ.edu.az
saytını yoxlamağı tövsiyə edirəm.
```

**Strukturlaşdırılmış sorğu:** `json:ADNSU necə universitetdir?`

```json
{
  "kateqoriya": "universitet",
  "qisa_cavab": "ADNSU (Azərbaycan Dövlət Neft və Sənaye Universiteti) texniki və mühəndislik sahələrində, xüsusilə neft-qaz sənayesi üzrə güclü təhsil verən nüfuzlu dövlət universitetidir.",
  "yonlendirme_lazimdir": false
}
```

## 🗂️ Layihə strukturu

```
.
├── main.py             # Tətbiqin əsas giriş nöqtəsi (streaming, xəta idarəetməsi, JSON rejimi daxil)
├── requirements.txt    # Layihənin asılılıqları
├── .env.example         # Mühit dəyişənləri nümunəsi
├── .env                 # Real API açarını saxlayan fayl (git-ə əlavə edilmir)
└── README.md            # Layihə sənədləşdirməsi
```

## 🛠️ Texnologiyalar

- Python
- NVIDIA API (LLM inteqrasiyası, streaming rejimində)
- JSON (strukturlaşdırılmış çıxış üçün)

## 📌 Qeydlər

- `.env` faylı həssas məlumat (API açarı) saxladığı üçün versiya nəzarətinə (`.gitignore`) əlavə edilməməlidir.
- Bu checkpoint-də əsas fərqlər:
  - **Xəta idarəetməsi** — API açarı yanlış olduqda, şəbəkə əlaqəsi kəsildikdə və ya sorğu uğursuz olduqda tətbiq gözlənilməz şəkildə dayanmır, istifadəçiyə aydın xəta mesajı göstərilir.
  - **Strukturlaşdırılmış çıxış** — `json:` prefiksi ilə göndərilən sorğularda cavab `kateqoriya`, `qisa_cavab` və `yonlendirme_lazimdir` sahələrindən ibarət JSON obyekti kimi qaytarılır ki, bu da nəticənin başqa sistemlərdə (məs. veb tətbiqdə) proqramatik şəkildə istifadəsini asanlaşdırır.
