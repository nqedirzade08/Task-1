# Checkpoint 6 (Token İzləmə və Xərc Xülasəsi)

Bu checkpoint əvvəlki versiyanın üzərinə **token istifadəsi izləmə** funksionallığı əlavə edir. Hər sorğudan sonra giriş (input), çıxış (output) və cəmi token sayı, həmçinin təxmini dollar xərci göstərilir. Əlavə olaraq, `usage:summary` əmri ilə bütün sessiya üzrə ümumi statistikanı görmək mümkündür.

## 📋 Xüsusiyyətlər

- Terminal üzərindən interaktiv sual-cavab rejimi
- NVIDIA API vasitəsilə LLM-ə sorğu göndərilməsi
- Streaming cavab: model tokeni yaratdıqca ekrana real vaxtda yazılır
- Xəta idarəetməsi: şəbəkə xətası, yanlış API açarı və digər gözlənilməz hallarda tətbiq çökmür
- Strukturlaşdırılmış (JSON) çıxış: sualın əvvəlinə `json:` yazmaqla cavabı JSON formatında almaq mümkündür
- Çıxış parsing və validasiyası, `test:parsing` əmri ilə offline test dəsti
- **Token istifadəsi izləmə**: hər cavabdan sonra giriş/çıxış/cəmi token sayı və təxmini xərc avtomatik göstərilir
- **Sessiya xülasəsi**: `usage:summary` əmri ilə cari sessiya ərzində göndərilən bütün sorğuların ümumi token sayı və təxmini ümumi xərci görünür
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

Terminala `test:parsing` yazın.

### 7. Sessiya üzrə token/xərc xülasəsini görmək üçün

Terminala `usage:summary` yazın. Bu, cari sessiyada göndərilmiş bütün sorğuların cəmi token sayını (giriş/çıxış/cəmi) və təxmini ümumi dollar xərcini göstərir.

## 🚀 İstifadə

Proqram işə düşdükdən sonra terminalda sualınızı yazıb Enter düyməsinə basın:

- **Adi sorğu** — cavab streaming şəklində göstərilir, sonunda həmin sorğuya aid token istifadəsi və təxmini xərc yazılır.
- **`json:` prefiksli sorğu** — cavab parsing/validasiyadan keçmiş JSON obyekti kimi qaytarılır.
- **`test:parsing`** — offline parsing/validasiya testlərini işə salır.
- **`usage:summary`** — sessiya başlanğıcından bu ana qədər göndərilən bütün sorğuların ümumi token və xərc statistikasını göstərir.

Yeni sual verə, ya da `exit` yazaraq proqramdan çıxa bilərsiniz.

### Nümunə sessiya

**Sorğu:** `Salam necəsən?`

```
[Cavab]
Salam, yaxşıyam, sağ ol! Sənə necə kömək edə bilərəm? Universitet və ya
ixtisas seçimi ilə bağlı sualın varmı?
[Token istifadəsi] giriş=1204, çıxış=278, cəmi=1482, təxmini xərc=$0.000408
```

**Sorğu:** `Mənə BMU haqqında məlumat ver`

```
[Cavab]
Bakı Mühəndislik Universiteti (BMU) 2016-cı ildə yaradılmış, müasir
yanaşmaları ilə seçilən gənc dövlət universitetidir.
- İxtisas profili: mühəndislik, texnologiya və dəqiq elmlər üzrə təhsil
  (kompüter mühəndisliyi, elektrik mühəndisliyi, sənaye mühəndisliyi və s.)
- Tədris dili: ingilis və Azərbaycan dillərində proqramlar mövcuddur
- Xüsusiyyətləri: xarici universitetlərlə əməkdaşlıq, müasir laboratoriyalar
[Token istifadəsi] giriş=1210, çıxış=517, cəmi=1727, təxmini xərc=$0.000552
```

**Sorğu:** `Kimya mühəndisliyi necədir?`

```
[Cavab]
Kimya mühəndisliyi kimya, fizika, riyaziyyat və iqtisadiyyatı birləşdirən
geniş sahədir...
[Token istifadəsi] giriş=1211, çıxış=406, cəmi=1617, təxmini xərc=$0.000486
```

**Sorğu:** `usage:summary`

```
=== Sessiya üzrə token/xərc xülasəsi ===
Sorğu sayı: 3
Giriş token: 3625
Çıxış token: 1201
Cəmi token: 4826
Təxmini ümumi xərc: $0.001446
```

## 🗂️ Layihə strukturu

```
.
├── main.py             # Tətbiqin əsas giriş nöqtəsi (streaming, xəta idarəetməsi, JSON rejimi, parsing/validasiya, token izləmə daxil)
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
- Bu checkpoint-də əsas fərq — hər sorğu üçün **token istifadəsinin** (giriş, çıxış, cəmi) və **təxmini xərcin** avtomatik hesablanıb göstərilməsi, həmçinin `usage:summary` əmri ilə bütün sessiya üzrə məcmu statistikanın alına bilməsidir.
- Təxmini xərc hesablanması istifadə olunan modelin qiymətləndirmə tarifinə əsaslanır və real hesab-fakturadan fərqli ola bilər; dəqiq xərc üçün NVIDIA hesabınızın rəsmi paneli yoxlanılmalıdır.
- Bu, Task 1-in sonuncu (6-cı) checkpoint-idir.
