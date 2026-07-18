# Checkpoint 5 (Çıxış Parsing/Validasiya)

Bu checkpoint əvvəlki versiyanın üzərinə **çıxış parsing və validasiya** qatını əlavə edir. Model tərəfindən qaytarılan JSON (strukturlaşdırılmış) cavab birbaşa istifadə olunmur — əvvəlcə mətndən düzgün JSON obyekti çıxarılır (parsing), sonra isə həmin obyektin tələb olunan sahələri, tipləri və icazə verilən dəyərləri ehtiva etdiyi yoxlanılır (validasiya). Bu proses həm real API cavabları, həm də daxili offline test dəstləri üzərində sınanır.

## 📋 Xüsusiyyətlər

- Terminal üzərindən interaktiv sual-cavab rejimi
- NVIDIA API vasitəsilə LLM-ə sorğu göndərilməsi
- Streaming cavab: model tokeni yaratdıqca ekrana real vaxtda yazılır
- Xəta idarəetməsi: şəbəkə xətası, yanlış API açarı və digər gözlənilməz hallarda tətbiq çökmür
- Strukturlaşdırılmış (JSON) çıxış: sualın əvvəlinə `json:` yazmaqla cavabı JSON formatında almaq mümkündür
- **Çıxış parsing**: modelin qaytardığı mətndən (izahla əhatələnmiş və ya markdown kod blokunda olsa belə) JSON obyekti düzgün şəkildə çıxarılır
- **Çıxış validasiyası**: çıxarılan JSON-un tələb olunan sahələri (`kateqoriya`, `qisa_cavab`, `yonlendirme_lazimdir`), düzgün tipləri və icazə verilən dəyər çərçivəsi yoxlanılır; uyğunsuzluq aşkarlandıqda aydın xəta mesajı ilə rədd edilir
- **Offline parsing/validasiya testləri**: `test:parsing` yazaraq, API-yə sorğu göndərmədən parsing/validasiya məntiqinin 9 fərqli ssenaridə düzgün işlədiyini yoxlamaq mümkündür
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

### 6. Offline parsing/validasiya testlərini görmək üçün

Terminala `test:parsing` yazın. Bu, API-yə sorğu göndərmədən, JSON parsing və validasiya məntiqinin müxtəlif ssenarilərdə (təmiz JSON, markdown kod blokunda JSON, qırıq JSON, çatışmayan sahə, yanlış tipli sahə, etibarsız kateqoriya dəyəri, boş cavab və s.) düzgün işlədiyini yoxlayan daxili testləri işə salır.

## 🚀 İstifadə

Proqram işə düşdükdən sonra terminalda sualınızı yazıb Enter düyməsinə basın:

- **Adi sorğu** — cavab `[Düşüncə prosesi]` və `[Cavab]` bölmələri ilə, sərbəst mətn formatında, streaming şəklində göstərilir.
- **`json:` prefiksli sorğu** — cavab modeldən alındıqdan sonra parsing və validasiya mərhələlərindən keçir; nəticə uğurlu olarsa strukturlaşdırılmış JSON obyekti, uğursuz olarsa isə səbəbini izah edən xəta mesajı göstərilir.
- **`test:parsing`** — API-yə müraciət etmədən, daxili test dəstini işə salaraq parsing/validasiya məntiqinin doğruluğunu yoxlayır.

Yeni sual verə, ya da `exit` yazaraq proqramdan çıxa bilərsiniz.

### Nümunə sessiya

**Sorğu:** `test:parsing`

```
Sualınızı daxil edin: test:parsing
=== Offline Parsing/Validasiya Testləri ===
[OK] Təmiz JSON
  Gözlənilən: keçər | Nəticə: keçdi
[OK] Ətrafında izah olan JSON
  Gözlənilən: keçər | Nəticə: keçdi
[OK] Markdown kod blokunda JSON
  Gözlənilən: keçər | Nəticə: keçdi
[OK] Yarımçıq/qırıq JSON
  Gözlənilən: rədd edilir | Nəticə: rədd edildi (Parsing xətası: Mətndə JSON obyekti tapılmadı.)
[OK] Çatışmayan sahə
  Gözlənilən: rədd edilir | Nəticə: rədd edildi (Validasiya xətası: Tələb olunan sahə çatışmır: 'yonlendirme_lazimdir')
[OK] Yanlış tipli sahə
  Gözlənilən: rədd edilir | Nəticə: rədd edildi (Validasiya xətası: 'yonlendirme_lazimdir' sahəsinin tipi yanlışdır: gözlənilən bool, alınan str)
[OK] Etibarsız kateqoriya dəyəri
  Gözlənilən: rədd edilir | Nəticə: rədd edildi (Validasiya xətası: 'kateqoriya' dəyəri etibarsızdır: 'diger' (icazə verilən: {'ixtisas', 'universitet', 'kənar'}))
[OK] Tamamilə JSON olmayan mətn
  Gözlənilən: rədd edilir | Nəticə: rədd edildi (Parsing xətası: Mətndə JSON obyekti tapılmadı.)
[OK] Boş cavab
  Gözlənilən: rədd edilir | Nəticə: rədd edildi (Parsing xətası: Mətndə JSON obyekti tapılmadı.)
Nəticə: 9/9 test gözlənilən kimi davrandı.
```

## 🗂️ Layihə strukturu

```
.
├── main.py             # Tətbiqin əsas giriş nöqtəsi (streaming, xəta idarəetməsi, JSON rejimi, parsing/validasiya daxil)
├── requirements.txt    # Layihənin asılılıqları
├── .env.example         # Mühit dəyişənləri nümunəsi
├── .env                 # Real API açarını saxlayan fayl (git-ə əlavə edilmir)
└── README.md            # Layihə sənədləşdirməsi
```

## 🛠️ Texnologiyalar

- Python
- NVIDIA API (LLM inteqrasiyası, streaming rejimində)
- JSON (strukturlaşdırılmış çıxış, parsing və validasiya üçün)

## 📌 Qeydlər

- `.env` faylı həssas məlumat (API açarı) saxladığı üçün versiya nəzarətinə (`.gitignore`) əlavə edilməməlidir.
- Bu checkpoint-də əsas fərq — modeldən gələn JSON cavabının etibarlılığının **iki mərhələdə** yoxlanılmasıdır:
  1. **Parsing** — mətn içindən (izahla əhatələnmiş və ya markdown kod blokunda olsa belə) düzgün JSON obyektinin çıxarılması.
  2. **Validasiya** — çıxarılan obyektin tələb olunan sahələri (`kateqoriya`, `qisa_cavab`, `yonlendirme_lazimdir`), düzgün tip və icazə verilən dəyərləri ehtiva etdiyinin yoxlanılması.
- `test:parsing` əmri bu iki mərhələni real API çağırışı olmadan, 9 müxtəlif ssenari üzərində sınayaraq məntiqin etibarlılığını sürətli şəkildə təsdiqləməyə imkan verir.
