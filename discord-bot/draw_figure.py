import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import io
import discord

KATEGORILER = {
    "Atak":     ["Orta Açma", "Bitiricilik", "Kafa İsabeti", "Kısa Pas", "Voleler"],
    "Savunma":  ["Ayakta Müdahale", "Kayarak Müdahale", "Top Kesme"],
    "Beceri":   ["Dribbling", "Falso", "Serbest Vuruş İsabeti", "Uzun Pas", "Top Kontrolü"],
    "Güç":      ["Şut Gücü", "Zıplama", "Dayanıklılık", "Güç", "Uzaktan Şut"],
    "Hareket":  ["Hızlanma", "Sprint Hızı", "Çeviklik", "Reaksiyonlar", "Denge"],
    "Mentalite":["Agresiflik", "Pozisyon Alma", "Görüş", "Penaltı"],
    "Kaleci":   ["Kaleci Atlayışı", "Kaleci Top Kontrolü", "Kaleci Vuruşu", "Kaleci Pozisyon Alma", "Kaleci Refleksler"],
}

KAT_RENKLER = {
    "Atak":      "#e74c3c",
    "Savunma":   "#3498db",
    "Beceri":    "#9b59b6",
    "Güç":       "#e67e22",
    "Hareket":   "#2ecc71",
    "Mentalite": "#f1c40f",
    "Kaleci":    "#1abc9c",
}

def generate_figure(isim: str, nitelikler: dict) -> discord.File:
    kategoriler_liste = list(KATEGORILER.keys())
    kategori_ortalamalar = []
    for kat, nit_list in KATEGORILER.items():
        vals = [nitelikler.get(n, 0) for n in nit_list]
        ortalama = sum(vals) / len(vals) if vals else 0
        kategori_ortalamalar.append(ortalama)

    N = len(kategoriler_liste)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values = kategori_ortalamalar + [kategori_ortalamalar[0]]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#16213e')

    ax.plot(angles, values, 'o-', linewidth=2, color='#7c3aed')
    ax.fill(angles, values, alpha=0.35, color='#7c3aed')

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(kategoriler_liste, color='white', fontsize=11, fontweight='bold')
    ax.set_yticklabels([])
    ax.set_ylim(0, 49)

    for spine in ax.spines.values():
        spine.set_edgecolor('#2d2d4e')
    ax.grid(color='#2d2d4e', linestyle='--', linewidth=0.8)

    ax.set_title(f"⚽ {isim} — Oyuncu Analizi", color='white', fontsize=14, fontweight='bold', pad=20)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close(fig)
    return discord.File(buf, filename="analiz.png")
