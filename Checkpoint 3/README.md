# Checkpoint 3 (Streaming)

Bu checkpoint əvvəlki versiyanın üzərinə **streaming (axın şəklində cavab)** funksionallığı əlavə edir. Artıq model cavabı tam formalaşana qədər gözləmək əvəzinə, hər token yarandıqca birbaşa ekrana yazılır — bu, xüsusilə uzun cavablarda istifadəçi üçün gözləmə hissini xeyli azaldır.

## 📋 Xüsusiyyətlər

- Terminal üzərindən interaktiv sual-cavab rejimi
- NVIDIA API vasitəsilə LLM-ə sorğu göndərilməsi
- **Streaming cavab**: model cavabı token-token yaratdıqca ekrana real vaxtda yazılır, tam cavab gözlənilmir
- Modelin düşüncə prosesinin (`[Düşüncə prosesi]`) və son cavabının (`[Cavab]`) ayrı-ayrı göstərilməsi
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

## 🚀 İstifadə

Proqram işə düşdükdən sonra terminalda sualınızı yazıb Enter düyməsinə basın. Cavab, əvvəlki checkpoint-lərdən fərqli olaraq, tam hazır olmasını gözləmədən token-token ekrana yazılacaq. Yeni sual verə, ya da `exit` yazaraq proqramdan çıxa bilərsiniz.

### Nümunə sessiya

**Sorğu:** `salam`

```
[Düşüncə prosesi]
Salamlaşma sualı gəldi. İstifadəçi sadəcə salam deyib, konkret mövzu yox.
Mənim əhatə dairəm universitet/ixtisas seçimi ilə bağlıdır. Salamlaşmaya
qarşılıq verib, sonra onu maraqlandıran mövzuya yönəltməliyəm.

[Cavab]
Salam! 👋
Mən sənə universitet və ixtisas seçimi mövzusunda kömək edə bilərəm.
Hansı sahəyə marağın var? Və ya konkret bir sualın?
```

**Sorğu:** `BDU necə universitetdir?`

```
[Düşüncə prosesi]
Bakı Dövlət Universiteti (BDU) haqqında sual verilib. Bu, Azərbaycanın ən
köklü və tanınmış ali təhsil müəssisələrindən biridir. Cavabda BDU-nun əsas
xüsusiyyətlərini qeyd etməliyəm...

[Cavab]
Bakı Dövlət Universiteti (BDU) Azərbaycanın ən qədim və nüfuzlu ali təhsil
müəssisələrindən biridir.
- Reputasiya: Ölkədə ən yüksək reytinqli universitetlər sırasındadır, xüsusən
  humanitar, təbiət və dəqiq elmlər sahəsində güclüdür.
- İxtisas spektri: Hüquq, iqtisadiyyat, biologiya, fizika, riyaziyyat,
  filologiya kimi geniş sahələri əhatə edir.
- Şərait: Bakı şəhər mərkəzində yerləşir, kitabxana və laboratoriya
  imkanları genişdir.

Qeyd edim ki, kompüter mühəndisliyi kimi texniki ixtisaslarda AzTU daha
spesifikdir, BDU isə daha çox nəzəri və klassik elmlərə önəm verir.
Hansı ixtisasla maraqlandığınızı deyin, sizə daha konkret müqayisə apara
bilərəm.
```

> **Qeyd:** Hər iki halda cavab istifadəçiyə göndərilməzdən əvvəl tam yaranmasını gözləmək əvəzinə, model tokeni yaratdıqca ekrana yazılıb — bu, xüsusilə uzun cavablarda gözləmə hissini azaldır.

## 🗂️ Layihə strukturu

```
.
├── main.py             # Tətbiqin əsas giriş nöqtəsi (streaming məntiqi daxil olmaqla)
├── requirements.txt    # Layihənin asılılıqları
├── .env.example         # Mühit dəyişənləri nümunəsi
├── .env                 # Real API açarını saxlayan fayl (git-ə əlavə edilmir)
└── README.md            # Layihə sənədləşdirməsi
```

## 🛠️ Texnologiyalar

- Python
- NVIDIA API (LLM inteqrasiyası, streaming rejimində)

## 📌 Qeydlər

- `.env` faylı həssas məlumat (API açarı) saxladığı üçün versiya nəzarətinə (`.gitignore`) əlavə edilməməlidir.
- Bu checkpoint-də əsas fərq — cavabın **streaming (axın)** şəklində, yəni model tokeni yaratdıqca real vaxtda ekrana çıxarılmasıdır. Bu, istifadəçi təcrübəsini yaxşılaşdırır, xüsusilə uzun və ya düşüncə prosesli cavablarda.
