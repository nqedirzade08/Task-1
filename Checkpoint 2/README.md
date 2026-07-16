# Abituriyent Dəstək Botu — Checkpoint 2

Bu layihə, abituriyentlərə universitet və ixtisas seçimi mövzusunda kömək etmək məqsədilə hazırlanmış, NVIDIA API əsaslı LLM tətbiqidir. Bot yalnız universitetlər, ixtisaslar və qəbul prosesi ilə bağlı suallara cavab verir, əhatə dairəsindən kənar suallarda isə istifadəçini məlumatlandıraraq nəzakətlə imtina edir.

## 📋 Xüsusiyyətlər

- Terminal üzərindən interaktiv sual-cavab rejimi
- NVIDIA API vasitəsilə LLM-ə sorğu göndərilməsi
- Modelin düşüncə prosesinin (`[Düşüncə prosesi]`) və son cavabının (`[Cavab]`) ayrı-ayrı göstərilməsi
- **Mövzu məhdudlaşdırması**: bot yalnız universitet, ixtisas seçimi və qəbul prosesi mövzularında cavab verir; əhatə dairəsindən kənar suallarda (məs. riyaziyyat məsələsi) istifadəçiyə bunu bildirib müvafiq resurslara yönləndirir
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
=== Abituriyent Dəstək Botu (Checkpoint 2) ===
Çıxmaq üçün 'exit' yazın.

Sualınızı daxil edin: ADA necə universitetdir?
Sorğu göndərilir, gözləyin...

Cavab:
[Düşüncə prosesi]
Bu sual AzTU haqqında əvvəlki sualdan fərqli olaraq konkret bir universitet haqqında
məlumat tələb edir. Mənim əhatə dairəmə universitetlər haqqında suallar daxildir, ona
görə də ADA Universiteti haqqında məlumat verə bilərəm...

[Cavab]
ADA Universiteti Azərbaycanda beynəlxalq standartlara uyğun təhsil verən özəl
universitetdir.

**Güclü tərəfləri:**
- Tədris dili əsasən ingilis dilindədir
- Beynəlxalq əlaqələri genişdir (xarici universitetlərlə mübadilə proqramları)
- Xüsusilə diplomatiya, beynəlxalq münasibətlər, IT və biznes ixtisasları ilə tanınır
- Müasir kampus və infrastruktur

**Qeyd:** Qəbul balları və ixtisas siyahısı hər il dəyişə bilər. Dəqiq məlumat üçün
rəsmi saytı (ada.edu.az) və ya tələ.edu.az portalını yoxlamağı tövsiyə edirəm.

Hansı ixtisasla maraqlandığınızı deyə bilərsiniz? O ixtisas haqqında daha konkret
məlumat verə bilərəm.

Sualınızı daxil edin: Kvadrat tənliyi necə həll edə bilərəm?
Sorğu göndərilir, gözləyin...

Cavab:
[Düşüncə prosesi]
Bu sual riyazi məsələnin həllinə aiddir, yəni fənn üzrə sualdır. Mənim əhatə dairəm
yalnız universitet/ixtisas seçimi və qəbul prosesi ilə bağlıdır. Ona görə də nəzakətlə
bildirirəm ki, bu mövzuda kömək edə bilmərəm...

[Cavab]
Bu mövzu mənim əhatə dairəmə daxil deyil. Mən yalnız universitetlər, ixtisas seçimi
və qəbul prosesi ilə bağlı suallara cavab verirəm.

Riyazi məsələlər üçün dərsliklərinizə, onlayn təhsil platformalarına və ya
müəlliminizə müraciət etməyinizi tövsiyə edirəm.

Universitet/ixtisas seçimi ilə bağlı başqa sualınız varmı?

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
- Bu checkpoint-də əsas fərq — botun yalnız **universitet, ixtisas və qəbul prosesi** mövzularına aid suallara cavab verməsi, bundan kənar sualları isə (məs. riyaziyyat, ümumi bilik və s.) rədd edib istifadəçini müvafiq mənbələrə yönləndirməsidir.
