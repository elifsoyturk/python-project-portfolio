
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# -------------------------------
# AYARLAR
# -------------------------------

DOSYA_YOLU = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "ders_gorevleri.json"
)

ARKA_PLAN = "#F3F6FC"
LACIVERT = "#243B64"
MAVI = "#4776E6"
YESIL = "#21875A"
KIRMIZI = "#D94848"
BEYAZ = "#FFFFFF"
GRI = "#64748B"

gorevler = []


# -------------------------------
# VERILERI YUKLE VE KAYDET
# -------------------------------

def verileri_yukle():
    global gorevler

    if not os.path.exists(DOSYA_YOLU):
        gorevler = []
        return

    try:
        with open(DOSYA_YOLU, "r", encoding="utf-8") as dosya:
            veri = json.load(dosya)

        if isinstance(veri, list):
            gorevler = [
                gorev for gorev in veri
                if isinstance(gorev, dict)
                and all(
                    anahtar in gorev
                    for anahtar in (
                        "ders", "gorev", "tarih",
                        "oncelik", "tamamlandi"
                    )
                )
            ]
        else:
            gorevler = []
            messagebox.showwarning(
                "Veri uyarisi",
                "Kayit dosyasinin formati gecersiz."
            )

    except (json.JSONDecodeError, OSError):
        gorevler = []
        messagebox.showwarning(
            "Kayit uyarisi",
            "Kayit dosyasi okunamadi. Yeni bir listeyle baslanacak."
        )


def verileri_kaydet():
    try:
        with open(DOSYA_YOLU, "w", encoding="utf-8") as dosya:
            json.dump(
                gorevler,
                dosya,
                ensure_ascii=False,
                indent=4
            )
        return True

    except OSError:
        messagebox.showerror(
            "Kayit hatasi",
            "Veriler dosyaya kaydedilemedi."
        )
        return False


# -------------------------------
# GOREV LISTESINI GUNCELLE
# -------------------------------

def listeyi_guncelle():
    for oge in tablo.get_children():
        tablo.delete(oge)

    for sira, gorev in enumerate(gorevler):
        if gorev["tamamlandi"]:
            durum = "Tamamlandi"
        else:
            durum = "Bekliyor"

        tablo.insert(
            "",
            "end",
            iid=str(sira),
            values=(
                gorev["ders"],
                gorev["gorev"],
                gorev["tarih"],
                gorev["oncelik"],
                durum
            )
        )

    toplam = len(gorevler)
    tamamlanan = sum(
        1 for gorev in gorevler
        if gorev["tamamlandi"]
    )
    kalan = toplam - tamamlanan

    istatistik.config(
        text=(
            f"Toplam gorev: {toplam}     "
            f"Tamamlanan: {tamamlanan}     "
            f"Kalan: {kalan}"
        )
    )


# -------------------------------
# YENI GOREV EKLE
# -------------------------------

def gorev_ekle():
    ders = ders_girdisi.get().strip()
    gorev = gorev_girdisi.get().strip()
    tarih = tarih_girdisi.get().strip()
    oncelik = oncelik_secimi.get()

    if not ders or not gorev or not tarih:
        messagebox.showwarning(
            "Eksik bilgi",
            "Lutfen ders, gorev ve son tarih alanlarini doldur."
        )
        return

    try:
        datetime.strptime(tarih, "%Y-%m-%d")
    except ValueError:
        messagebox.showwarning(
            "Hatali tarih",
            "Tarihi YYYY-AA-GG formatinda gir.\nOrnek: 2026-10-20"
        )
        return

    yeni_gorev = {
        "ders": ders,
        "gorev": gorev,
        "tarih": tarih,
        "oncelik": oncelik,
        "tamamlandi": False
    }

    gorevler.append(yeni_gorev)

    if verileri_kaydet():
        listeyi_guncelle()
        ders_girdisi.delete(0, tk.END)
        gorev_girdisi.delete(0, tk.END)
        tarih_girdisi.delete(0, tk.END)
        oncelik_secimi.set("Orta")


# -------------------------------
# GOREVI TAMAMLA
# -------------------------------

def gorevi_tamamla():
    secim = tablo.selection()

    if not secim:
        messagebox.showinfo(
            "Gorev sec",
            "Once listeden bir gorev sec."
        )
        return

    indeks = int(secim[0])

    if gorevler[indeks]["tamamlandi"]:
        messagebox.showinfo(
            "Bilgi",
            "Bu gorev zaten tamamlanmis."
        )
        return

    gorevler[indeks]["tamamlandi"] = True

    if verileri_kaydet():
        listeyi_guncelle()


# -------------------------------
# GOREVI SIL
# -------------------------------

def gorevi_sil():
    secim = tablo.selection()

    if not secim:
        messagebox.showinfo(
            "Gorev sec",
            "Silmek icin once bir gorev sec."
        )
        return

    indeks = int(secim[0])
    secilen_gorev = gorevler[indeks]

    cevap = messagebox.askyesno(
        "Gorevi sil",
        f"'{secilen_gorev['gorev']}' gorevini silmek istiyor musun?"
    )

    if cevap:
        silinen = gorevler.pop(indeks)

        if not verileri_kaydet():
            gorevler.insert(indeks, silinen)
            return

        listeyi_guncelle()


# -------------------------------
# FILTRELEME
# -------------------------------

def filtrele(*args):
    arama = arama_girdisi.get().strip().casefold()
    filtre = durum_secimi.get()

    for oge in tablo.get_children():
        tablo.delete(oge)

    for sira, gorev in enumerate(gorevler):
        if filtre == "Bekleyenler" and gorev["tamamlandi"]:
            continue

        if filtre == "Tamamlananlar" and not gorev["tamamlandi"]:
            continue

        aranacak = (
            gorev["ders"] + " " + gorev["gorev"]
        ).casefold()

        if arama not in aranacak:
            continue

        durum = (
            "Tamamlandi"
            if gorev["tamamlandi"]
            else "Bekliyor"
        )

        tablo.insert(
            "",
            "end",
            iid=str(sira),
            values=(
                gorev["ders"],
                gorev["gorev"],
                gorev["tarih"],
                gorev["oncelik"],
                durum
            )
        )


def filtreleri_temizle():
    arama_girdisi.delete(0, tk.END)
    durum_secimi.set("Tum gorevler")
    listeyi_guncelle()


# -------------------------------
# ARAYUZ
# -------------------------------

pencere = tk.Tk()
pencere.title("Akilli Ders ve Gorev Takipcisi")
pencere.geometry("1050x720")
pencere.minsize(850, 620)
pencere.configure(bg=ARKA_PLAN)

stil = ttk.Style()
stil.theme_use("clam")

stil.configure(
    "Treeview",
    background=BEYAZ,
    foreground=LACIVERT,
    rowheight=34,
    fieldbackground=BEYAZ,
    font=("Arial", 10)
)

stil.configure(
    "Treeview.Heading",
    background=LACIVERT,
    foreground=BEYAZ,
    font=("Arial", 10, "bold"),
    padding=9
)

stil.map(
    "Treeview",
    background=[("selected", MAVI)],
    foreground=[("selected", BEYAZ)]
)

# UST BASLIK
baslik_alani = tk.Frame(pencere, bg=LACIVERT, pady=20)
baslik_alani.pack(fill="x")

tk.Label(
    baslik_alani,
    text="AKILLI DERS VE GOREV TAKIPCISI",
    font=("Arial", 21, "bold"),
    bg=LACIVERT,
    fg=BEYAZ
).pack()

tk.Label(
    baslik_alani,
    text="Derslerini planla, gorevlerini takip et, hedeflerine ulas!",
    font=("Arial", 11),
    bg=LACIVERT,
    fg="#DCE7FF"
).pack(pady=(6, 0))

# ANA ALAN
ana_alan = tk.Frame(pencere, bg=ARKA_PLAN, padx=22, pady=16)
ana_alan.pack(fill="both", expand=True)

# GOREV EKLEME KARTI
kart = tk.LabelFrame(
    ana_alan,
    text=" Yeni gorev ekle ",
    font=("Arial", 12, "bold"),
    bg=BEYAZ,
    fg=LACIVERT,
    padx=14,
    pady=12
)
kart.pack(fill="x", pady=(0, 14))

tk.Label(
    kart, text="Ders adi", bg=BEYAZ, fg=LACIVERT
).grid(row=0, column=0, sticky="w", padx=5)

tk.Label(
    kart, text="Gorev / konu", bg=BEYAZ, fg=LACIVERT
).grid(row=0, column=1, sticky="w", padx=5)

tk.Label(
    kart, text="Son tarih (YYYY-AA-GG)", bg=BEYAZ, fg=LACIVERT
).grid(row=0, column=2, sticky="w", padx=5)

tk.Label(
    kart, text="Oncelik", bg=BEYAZ, fg=LACIVERT
).grid(row=0, column=3, sticky="w", padx=5)

ders_girdisi = ttk.Entry(kart, width=19)
ders_girdisi.grid(row=1, column=0, padx=5, pady=8, sticky="ew")

gorev_girdisi = ttk.Entry(kart, width=24)
gorev_girdisi.grid(row=1, column=1, padx=5, pady=8, sticky="ew")

tarih_girdisi = ttk.Entry(kart, width=19)
tarih_girdisi.grid(row=1, column=2, padx=5, pady=8, sticky="ew")

oncelik_secimi = ttk.Combobox(
    kart,
    values=["Dusuk", "Orta", "Yuksek"],
    state="readonly",
    width=10
)
oncelik_secimi.set("Orta")
oncelik_secimi.grid(row=1, column=3, padx=5, pady=8)

ekle_butonu = tk.Button(
    kart,
    text=" + Gorev ekle ",
    command=gorev_ekle,
    bg=MAVI,
    fg=BEYAZ,
    activebackground=LACIVERT,
    activeforeground=BEYAZ,
    relief="flat",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=7,
    cursor="hand2"
)
ekle_butonu.grid(
    row=1, column=4, padx=8, pady=8
)

for sutun in range(4):
    kart.grid_columnconfigure(sutun, weight=1)

# ISTATISTIK
istatistik = tk.Label(
    ana_alan,
    text="",
    bg=ARKA_PLAN,
    fg=LACIVERT,
    font=("Arial", 11, "bold"),
    anchor="w"
)
istatistik.pack(fill="x", pady=(0, 10))

# ARAMA VE FILTRE
filtre_alani = tk.Frame(ana_alan, bg=ARKA_PLAN)
filtre_alani.pack(fill="x", pady=(0, 10))

tk.Label(
    filtre_alani,
    text="Ara:",
    bg=ARKA_PLAN,
    fg=LACIVERT,
    font=("Arial", 10, "bold")
).pack(side="left", padx=(0, 6))

arama_girdisi = ttk.Entry(filtre_alani, width=24)
arama_girdisi.pack(side="left", padx=(0, 14))

tk.Label(
    filtre_alani,
    text="Durum:",
    bg=ARKA_PLAN,
    fg=LACIVERT,
    font=("Arial", 10, "bold")
).pack(side="left", padx=(0, 6))

durum_secimi = ttk.Combobox(
    filtre_alani,
    values=["Tum gorevler", "Bekleyenler", "Tamamlananlar"],
    state="readonly",
    width=18
)
durum_secimi.set("Tum gorevler")
durum_secimi.pack(side="left")

tk.Button(
    filtre_alani,
    text="Filtreleri temizle",
    command=filtreleri_temizle,
    bg="#E2E8F0",
    fg=LACIVERT,
    relief="flat",
    padx=10,
    pady=5,
    cursor="hand2"
).pack(side="left", padx=10)

# GOREV TABLOSU
tablo_alani = tk.Frame(ana_alan, bg=BEYAZ)
tablo_alani.pack(fill="both", expand=True)

sutunlar = (
    "ders", "gorev", "tarih", "oncelik", "durum"
)

tablo = ttk.Treeview(
    tablo_alani,
    columns=sutunlar,
    show="headings",
    selectmode="browse"
)

tablo.heading("ders", text="Ders")
tablo.heading("gorev", text="Gorev / konu")
tablo.heading("tarih", text="Son tarih")
tablo.heading("oncelik", text="Oncelik")
tablo.heading("durum", text="Durum")

tablo.column("ders", width=160, anchor="w")
tablo.column("gorev", width=300, anchor="w")
tablo.column("tarih", width=130, anchor="center")
tablo.column("oncelik", width=110, anchor="center")
tablo.column("durum", width=130, anchor="center")

kaydirma = ttk.Scrollbar(
    tablo_alani,
    orient="vertical",
    command=tablo.yview
)
tablo.configure(yscrollcommand=kaydirma.set)

tablo.pack(side="left", fill="both", expand=True)
kaydirma.pack(side="right", fill="y")

# ISLEM BUTONLARI
buton_alani = tk.Frame(ana_alan, bg=ARKA_PLAN)
buton_alani.pack(fill="x", pady=(12, 0))

tk.Button(
    buton_alani,
    text="✓ Tamamlandi olarak isaretle",
    command=gorevi_tamamla,
    bg=YESIL,
    fg=BEYAZ,
    relief="flat",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=9,
    cursor="hand2"
).pack(side="left", padx=(0, 8))

tk.Button(
    buton_alani,
    text="Secili gorevi sil",
    command=gorevi_sil,
    bg=KIRMIZI,
    fg=BEYAZ,
    relief="flat",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=9,
    cursor="hand2"
).pack(side="left")

# OLAYLARI FILTRELEMEYE BAGLA
arama_girdisi.bind("<KeyRelease>", filtrele)
durum_secimi.bind("<<ComboboxSelected>>", filtrele)

# UYGULAMAYI BASLAT
verileri_yukle()
listeyi_guncelle()

pencere.mainloop()
