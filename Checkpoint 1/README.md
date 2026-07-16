# LLM Əsaslı Tətbiq — Checkpoint 1

Bu layihə, NVIDIA API vasitəsilə böyük dil modeli (LLM) ilə terminal üzərindən əlaqə qurmağa imkan verən sadə bir konsol tətbiqidir. İstifadəçi terminala sual yazır, model isə düşüncə prosesini və son cavabını qaytarır.

## 📋 Xüsusiyyətlər

- Terminal üzərindən interaktiv sual-cavab rejimi
- NVIDIA API vasitəsilə LLM-ə sorğu göndərilməsi
- Modelin düşüncə prosesinin (`[Düşüncə prosesi]`) və son cavabının (`[Cavab]`) ayrı-ayrı göstərilməsi
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

Proqram işə düşdükdən sonra terminalda sualınızı yazıb Enter düyməsinə basın. Cavabdan sonra yeni sual verə, ya da `exit` yazaraq proqramdan çıxa bilərsiniz.

### Nümunə sessiya

```
=== LLM Əsaslı Tətbiq (Checkpoint 1) ===
Çıxmaq üçün 'exit' yazın.
Sualınızı daxil edin: Salam. Necəsən?
Sorğu göndərilir, gözləyin...
Cavab:
[Düşüncə prosesi]
Salam, necəsən? - Bu, Azərbaycan dilində bir sualdır. İstifadəçi mənə salam verib
və halımı soruşur. Mən süni intellekt olduğum üçün halım yoxdur, amma cavab
verməliyəm...
[Cavab]
Salam! Mən yaxşıyam, sağ ol. Sən necəsən? Nə ilə bağlı kömək lazımdır?
Sualınızı daxil edin: exit
Çıxılır...
```

## 🗂️ Layihə strukturu

```
.
├── main.py             # Tətbiqin əsas giriş nöqtəsi
├── requirements.txt    # Layihənin asılılıqları
├── .env.example         # Mühit dəyişənləri nümunəsi
├── .env                 # Real API açarını saxlayan fayl (git-ə əlavə edilmir)
└── README.md            # Layihə sənədləşdirməsi
```

## 🛠️ Texnologiyalar

- Python
- NVIDIA API (LLM inteqrasiyası)

## 📌 Qeydlər

- `.env` faylı həssas məlumat (API açarı) saxladığı üçün versiya nəzarətinə (`.gitignore`) əlavə edilməməlidir.
- Bu, layihənin ilk checkpoint-idir və əsas funksionallıq — terminal üzərindən LLM-ə sorğu göndərmək və cavab almaqdır.
