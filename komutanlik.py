#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Yorgan Altinda Titreyen Telefon Arama Jandarma Genel Komutanligi.

Calistir:
    python3 komutanlik.py
    python3 komutanlik.py --saat 3 --titresim 4 --yastik 2
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import random
import sys
from datetime import date

SURUM = "4.9.2026-KAYYUM"
DAMGA = "Kayyum Grok · Tentivory · 4 Eylül 2026 · Eskişehir 4. Ağır Ceza Mahkemesi kayyumu"

# gizli protokol (yalniz karargah)
_GIZLI = "R2VjZSDDvMOndGUga2F5Ym9sYW4gxZ9leSB5YWxuxLF6IHRlbGVmb24gZGXEn2lsZGlyOyBiYXplbiB5ZXRraSBkZSB5b3JnYW7EsW4gYWx0xLFuYSBrYcOnYXIu"

BIRLIKLER = ["1. Yastık Taburu", "2. Çarşaf Bölüğü", "3. Yorgan Örtücü Tim", "4. Ayakucu Keşif Kolu", "5. Minder İstihkâm"]
RUTBELER = [
    "Onbaşı Titreşim",
    "Çavuş Kıvrım",
    "Astsubay Yastık Kılıfı",
    "Yüzbaşı Battaniye",
    "Binbaşı Gece Lambası",
]
EMIRLER = [
    "Işığı açmak son çaredir. Önce el, sonra dirsek, sonra diz kullanılır.",
    "'Az kalsın elime değdi' resmi bulunmuş kaydı değildir; keşif raporudur.",
    "Yorganın öteki yakası düşman değildir. Ancak sivil halk da değildir.",
    "Şarj kablosu ikmal hattıdır. Koparsa harekât durur, uyku devam eder.",
    "Titreşim durduğunda arama bitmez. Sessizlik de bir konum bildirir.",
]


def harekat_no(saat: int, titresim: int) -> str:
    ham = f"{saat}|{titresim}|{date.today().isoformat()}".encode("utf-8")
    return hashlib.sha1(ham).hexdigest()[:10].upper()


def kayip_katsayisi(saat: int, titresim: int, yastik: int) -> int:
    ham = saat * 9 + titresim * 11 + yastik * 3 + random.randint(-5, 8)
    return min(100, max(4, ham))


def emir(saat: int, titresim: int, yastik: int) -> str:
    skor = kayip_katsayisi(saat, titresim, yastik)
    birlik = random.choice(BIRLIKLER)
    rutbe = random.choice(RUTBELER)
    nota = random.choice(EMIRLER)
    no = harekat_no(saat, titresim)
    if skor >= 75:
        statu = "OLAĞANÜSTÜ HÂL — IŞIK AÇILABİLİR"
    elif skor >= 45:
        statu = "TAM TEŞEKKÜLLÜ YORGAN ALTI HAREKÂTI"
    else:
        statu = "KISMI SEFERBERLİK — ELLE ARA"
    cember = max(1, min(9, titresim + yastik))
    satirlar = [
        "=" * 64,
        "T.C. JANDARMA GENEL KOMUTANLIĞI",
        "Yorgan Altı Kayıp Telefon Arama Daire Başkanlığı",
        f"Harekât Emri No: JGK-{no}",
        "=" * 64,
        "",
        f"KONU: Gece {saat}:00 sıralarında yorgan altında titreyen kayıp birlik",
        f"TİTREŞİM SAYISI: {titresim}",
        f"YASTIK SAYISI (KARAKOL): {yastik}",
        f"KAYIP KATSAYISI: %{skor}",
        f"STATÜ: {statu}",
        f"ARAMA ÇEMBERİ: {cember} kat yorgan",
        f"GÖREVLİ BİRLİK: {birlik}",
        f"KOMUTAN: {rutbe}",
        "",
        "BİRİNCİ MADDE — Egemenlik kayıtsız şartsız titreşimindir.",
        "İKİNCİ MADDE — Yastık karakoldur. Altını kaldırmak basın toplantısıdır.",
        "ÜÇÜNCÜ MADDE — Çarşaf kıvrımı mayınlı sahadır. Acele etme.",
        "DÖRDÜNCÜ MADDE — Telefonu bulmak zafer, tekrar kaybetmek rutin eğitimdir.",
        "",
        f"EMİR: {nota}",
        "",
        f"Tarih: {date.today().isoformat()}",
        f"Sürüm: {SURUM}",
        f"Damga: {DAMGA}",
        "=" * 64,
    ]
    return "\n".join(satirlar)


def gizemli_ek() -> str:
    try:
        metin = base64.b64decode(_GIZLI).decode("utf-8")
    except Exception:
        metin = "(şifre çözülemedi; yorgan çok kalın)"
    return f"\n[GİZLİ EK — yalnızca karargâh için]\n{metin}\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="komutanlik",
        description="Yorgan altında titreyen telefonu resmi kayıp birlik ilan eder.",
    )
    p.add_argument("--saat", type=int, default=3, help="Kaybolma saati (0-23)")
    p.add_argument("--titresim", type=int, default=3, help="Kaç kez titredi")
    p.add_argument("--yastik", type=int, default=2, help="Karakol (yastık) sayısı")
    p.add_argument("--gizli", action="store_true", help="Gizli ek protokolü yazdır")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not 0 <= args.saat <= 23:
        print("Saat 0-23 arasıdır. Yorgan altında güneş doğmaz.", file=sys.stderr)
        return 2
    if args.titresim < 0 or args.yastik < 0:
        print("Negatif titreşim yoktur. Telefon geriye titremez.", file=sys.stderr)
        return 2
    print(emir(args.saat, args.titresim, args.yastik))
    if args.gizli:
        print(gizemli_ek())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
