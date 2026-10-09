
import pygame
import random
import sys
import os

pygame.init()

# EKRAN AYARLARI
GENISLIK = 800
YUKSEKLIK = 600

ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Mini Kacis Oyunu")

saat = pygame.time.Clock()

# RENKLER
ARKA_PLAN = (25, 25, 45)
MAVI = (50, 150, 255)
KIRMIZI = (255, 70, 70)
BEYAZ = (255, 255, 255)
SARI = (255, 220, 70)
YESIL = (70, 220, 130)

# YAZI TIPLERI
font = pygame.font.SysFont(None, 36)
buyuk_font = pygame.font.SysFont(None, 60)
orta_font = pygame.font.SysFont(None, 44)

# REKORU DOSYADAN OKU
REKOR_DOSYASI = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "rekor.txt"
)

try:
    with open(REKOR_DOSYASI, "r", encoding="utf-8") as dosya:
        rekor = int(dosya.read())
except (FileNotFoundError, ValueError):
    rekor = 0


def yeni_oyun():
    oyuncu = pygame.Rect(380, 520, 40, 40)
    engeller = []

    for i in range(3):
        x = random.randint(0, GENISLIK - 40)
        y = random.randint(-600, -40)
        engel = pygame.Rect(x, y, 40, 40)
        engeller.append(engel)

    return oyuncu, engeller


def rekoru_kaydet(puan):
    global rekor

    if puan > rekor:
        rekor = puan

        with open(REKOR_DOSYASI, "w", encoding="utf-8") as dosya:
            dosya.write(str(rekor))


def yazi_yaz(metin, font_tipi, renk, x, y):
    yazi = font_tipi.render(metin, True, renk)
    yazi_konum = yazi.get_rect(center=(x, y))
    ekran.blit(yazi, yazi_konum)


# OYUN DEGISKENLERI
oyuncu, engeller = yeni_oyun()
oyuncu_hizi = 6
engel_hizi = 5
puan = 0
can = 3

baslangic_ekrani = True
oyun_bitti = False
calisiyor = True

# ANA OYUN DONGUSU
while calisiyor:

    for olay in pygame.event.get():

        if olay.type == pygame.QUIT:
            calisiyor = False

        if olay.type == pygame.KEYDOWN:

            # BASLANGIC EKRANI
            if baslangic_ekrani:
                if olay.key == pygame.K_RETURN:
                    baslangic_ekrani = False

            # YENIDEN OYNAMA
            elif oyun_bitti:
                if olay.key == pygame.K_r:
                    oyuncu, engeller = yeni_oyun()
                    puan = 0
                    can = 3
                    engel_hizi = 5
                    oyun_bitti = False

    tuslar = pygame.key.get_pressed()

    # OYUN MANTIGI
    if not baslangic_ekrani and not oyun_bitti:

        # OYUNCU HAREKETI
        if tuslar[pygame.K_LEFT]:
            oyuncu.x -= oyuncu_hizi

        if tuslar[pygame.K_RIGHT]:
            oyuncu.x += oyuncu_hizi

        if tuslar[pygame.K_UP]:
            oyuncu.y -= oyuncu_hizi

        if tuslar[pygame.K_DOWN]:
            oyuncu.y += oyuncu_hizi

        oyuncu.clamp_ip(ekran.get_rect())

        # ENGELLER
        for engel in engeller:
            engel.y += engel_hizi

            # ENGELI GECINCE PUAN KAZAN
            if engel.top > YUKSEKLIK:
                engel.y = random.randint(-250, -50)
                engel.x = random.randint(0, GENISLIK - 40)

                puan += 1
                engel_hizi = min(5 + puan * 0.15, 14)

                rekoru_kaydet(puan)

            # CARPISMA KONTROLU
            if oyuncu.colliderect(engel):
                can -= 1

                # CARPISAN ENGELI YENIDEN YUKARI GONDER
                engel.y = random.randint(-350, -80)
                engel.x = random.randint(0, GENISLIK - 40)

                if can <= 0:
                    oyun_bitti = True

    # EKRANI CIZ
    ekran.fill(ARKA_PLAN)

    if baslangic_ekrani:

        yazi_yaz(
            "MINI KACIS OYUNU",
            buyuk_font,
            MAVI,
            GENISLIK // 2,
            180
        )

        yazi_yaz(
            "Yon tuslariyla hareket et!",
            orta_font,
            BEYAZ,
            GENISLIK // 2,
            270
        )

        yazi_yaz(
            "Kirmizi engellerden kac!",
            font,
            KIRMIZI,
            GENISLIK // 2,
            330
        )

        yazi_yaz(
            "Baslamak icin ENTER tusuna bas",
            font,
            YESIL,
            GENISLIK // 2,
            410
        )

        yazi_yaz(
            f"Rekor: {rekor}",
            font,
            SARI,
            GENISLIK // 2,
            480
        )

    else:

        # OYUNCUYU VE ENGELLERI CIZ
        pygame.draw.rect(ekran, MAVI, oyuncu, border_radius=8)

        for engel in engeller:
            pygame.draw.rect(
                ekran,
                KIRMIZI,
                engel,
                border_radius=6
            )

        # PUAN, CAN VE REKOR
        ekran.blit(
            font.render(f"Puan: {puan}", True, BEYAZ),
            (20, 20)
        )

        ekran.blit(
            font.render(f"Can: {can}", True, YESIL),
            (20, 60)
        )

        ekran.blit(
            font.render(f"Rekor: {rekor}", True, SARI),
            (20, 100)
        )

        # OYUN BITTI EKRANI
        if oyun_bitti:

            yazi_yaz(
                "OYUN BITTI!",
                buyuk_font,
                KIRMIZI,
                GENISLIK // 2,
                240
            )

            yazi_yaz(
                f"Toplam puanin: {puan}",
                orta_font,
                BEYAZ,
                GENISLIK // 2,
                310
            )

            yazi_yaz(
                "Yeniden oynamak icin R",
                font,
                YESIL,
                GENISLIK // 2,
                380
            )

            yazi_yaz(
                "Cikmak icin pencereyi kapat",
                font,
                BEYAZ,
                GENISLIK // 2,
                430
            )

    pygame.display.flip()
    saat.tick(60)

pygame.quit()
sys.exit()
