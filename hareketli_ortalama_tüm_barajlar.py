# Hareketli ortalama için başarı metrikleri entegre edilmiş kod

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error

def evaluate_forecast(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    return round(mae, 4), round(rmse, 4), round(mape, 2)

df = pd.read_excel("veri_tarih_ekli.xlsx")
barajlar = ["Ömerli", "Darlık", "Elmalı", "Terkos", "Alibey",
            "Büyükçekmece", "Sazlıdere", "Kazandere", "Pabuçdere", "Istrancalar"]

fig, axes = plt.subplots(2, 5, figsize=(25, 10))
fig.suptitle("Tüm Barajlar İçin Hareketli Ortalama ve Tahmin Grafikleri", fontsize=18)

basari_sonuclari = []

for i, baraj_adi in enumerate(barajlar):
    ax = axes[i // 5, i % 5]
    veri_serisi = df[baraj_adi]
    tarih_serisi = df["Tarih"]
    gercek_veri = veri_serisi.iloc[-365:]

    hareketli_ortalama_gercek = []
    tarih_hareketli_ortalama = []
    for j in range(len(df) - 365, len(df)):
        if j >= 29:
            ortalama = np.mean(veri_serisi.iloc[j-29:j+1])
            hareketli_ortalama_gercek.append(ortalama)
            tarih_hareketli_ortalama.append(tarih_serisi.iloc[j])

    pencere = list(veri_serisi.iloc[-60:-30])
    tahminler = []
    for _ in range(30):
        ortalama = np.mean(pencere)
        tahminler.append(ortalama)
        pencere.pop(0)
        pencere.append(ortalama)

    if len(veri_serisi) >= 30:
        gercek_gelecek = veri_serisi.iloc[-30:].values
        mae, rmse, mape = evaluate_forecast(gercek_gelecek, tahminler)
        basari_sonuclari.append({
            "Baraj": baraj_adi,
            "MAE": mae,
            "RMSE": rmse,
            "MAPE (%)": mape
        })
        ax.set_title(f"{baraj_adi}\nMAPE: {mape:.2f}%")
    else:
        ax.set_title(f"{baraj_adi}\nVeri yetersiz")

    tahmin_tarihleri = tarih_serisi.iloc[-30:] if len(tarih_serisi) >= 30 else []

    ax.plot(tarih_serisi.iloc[-365:], gercek_veri, label="Gerçek", color="blue")
    ax.plot(tarih_hareketli_ortalama, hareketli_ortalama_gercek, label="Ort.", color="orange", linestyle="--")
    if len(tahmin_tarihleri) == 30:
        ax.plot(tahmin_tarihleri, tahminler, label="Tahmin", color="green", linestyle="-.")
    ax.tick_params(axis='x', labelrotation=45)
    ax.grid(True)

handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=12)
plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig("final.png")
plt.show()

df_sonuclar = pd.DataFrame(basari_sonuclari)
print("\n--- Hareketli Ortalama Tahmin Başarı Metrikleri ---")
print(df_sonuclar.to_string(index=False))
