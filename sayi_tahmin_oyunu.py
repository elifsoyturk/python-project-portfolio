
import random

print("=== SAYI TAHMİN OYUNU ===")

while True:
    print("\nZorluk Seviyesi Seç:")
    print("1 - Kolay")
    print("2 - Orta")
    print("3 - Zor")

    seviye = input("Seçimin (1/2/3): ")

    if seviye == "1":
        ust_sinir = 50
        tahmin_hakki = 10
    elif seviye == "2":
        ust_sinir = 100
        tahmin_hakki = 7
    elif seviye == "3":
        ust_sinir = 200
        tahmin_hakki = 5
    else:
        print("Geçersiz seçim! Tekrar dene.")
        continue

    tutulan_sayi = random.randint(1, ust_sinir)
    puan = 0
    kazanildi = False

    print(f"\n1 ile {ust_sinir} arasında bir sayı tuttum!")
    print(f"{tahmin_hakki} tahmin hakkın var.")

    while tahmin_hakki > 0:
        try:
            tahmin = int(input("Tahminin: "))
        except ValueError:
            print("Lütfen bir tam sayı gir.")
            continue

        if not 1 <= tahmin <= ust_sinir:
            print(f"1 ile {ust_sinir} arasında bir sayı gir.")
            continue

        if tahmin == tutulan_sayi:
            puan = tahmin_hakki * 10
            print("Tebrikler! Doğru tahmin ettin!")
            print(f"Kazandığın puan: {puan}")
            kazanildi = True
            break
        elif tahmin < tutulan_sayi:
            print("Daha büyük bir sayı dene.")
        else:
            print("Daha küçük bir sayı dene.")

        tahmin_hakki -= 1
        print(f"Kalan hakkın: {tahmin_hakki}")

    if not kazanildi:
        print(f"Oyun bitti! Sayı {tutulan_sayi} idi.")

    tekrar = input("\nTekrar oynamak ister misin? (e/h): ").lower()

    if tekrar != "e":
        print("Oynadığın için teşekkürler!")
        break
