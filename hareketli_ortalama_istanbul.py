# Hareketli ortalama ile istanbul geneli tahmini ve başarı metrikleri entegrasyonu yapılan kod
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error

def evaluate_forecast(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    return round(mae, 4), round(rmse, 4), round(mape, 2)

def moving_average_forecast(series, window=30, steps=30):
    pencere = list(series[-window:])
    tahminler = []
    for _ in range(steps):
        ort = np.mean(pencere)
        tahminler.append(ort)
        pencere.pop(0)
        pencere.append(ort)
    return tahminler

df = pd.read_excel("veri_tarih_ekli.xlsx")
df["Tarih"] = pd.to_datetime(df["Tarih"])

barajlar = ["Ömerli", "Darlık", "Elmalı", "Terkos", "Alibey",
            "Büyükçekmece", "Sazlıdere", "Kazandere", "Pabuçdere", "Istrancalar"]

df["İstanbul_Ortalama"] = df[barajlar].mean(axis=1)
tarih_serisi = df["Tarih"]
veri_serisi = df["İstanbul_Ortalama"]

gercek_veri = veri_serisi.iloc[-365:]
hareketli_ortalama_gercek = []
tarih_hareketli_ortalama = []

for i in range(len(df) - 365, len(df)):
    if i >= 29:
        ort = np.mean(veri_serisi.iloc[i-29:i+1])
        hareketli_ortalama_gercek.append(ort)
        tarih_hareketli_ortalama.append(tarih_serisi.iloc[i])

tahminler = moving_average_forecast(veri_serisi, window=30, steps=30)
tahmin_tarihleri = pd.date_range(start=tarih_serisi.iloc[-1] + pd.Timedelta(days=1), periods=30)

gercek_gelecek = veri_serisi.iloc[-30:].values
mae, rmse, mape = evaluate_forecast(gercek_gelecek, tahminler)

plt.figure(figsize=(12, 6))
plt.plot(tarih_serisi.iloc[-365:], gercek_veri, label="Gerçek Veri (Son 365 Gün)", color="blue")
plt.plot(tarih_hareketli_ortalama, hareketli_ortalama_gercek, label="30 Günlük Hareketli Ortalama", color="orange", linestyle="--")
plt.plot(tahmin_tarihleri, tahminler, label="30 Günlük Tahmin", color="green", linestyle="-.")
plt.title(f"İstanbul Geneli Hareketli Ortalama Tahmini\nMAE={mae}, RMSE={rmse}, MAPE={mape}%")
plt.xlabel("Tarih")
plt.ylabel("Ortalama Baraj Doluluk Oranı")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("istanbul_hareketli_ort_tahmin.png", dpi=300)
plt.show()

print("\n--- İstanbul Geneli Başarı Metrikleri ---")
print(f"MAE:  {mae}")
print(f"RMSE: {rmse}")
print(f"MAPE: {mape}%")
