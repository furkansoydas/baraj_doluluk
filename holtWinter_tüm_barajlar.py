# Tüm barajlar için holt winter yöntemi, başarı metrikleri enteger edilmiş kod 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error

def evaluate_forecast(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    return round(mae, 4), round(rmse, 4), round(mape, 2)


dosya_adi = "veri_tarih_ekli.xlsx"
barajlar = ["Ömerli", "Darlık", "Elmalı", "Terkos", "Alibey",
            "Büyükçekmece", "Sazlıdere", "Kazandere", "Pabuçdere", "Istrancalar"]

df = pd.read_excel(dosya_adi, index_col="Tarih", parse_dates=True)
df.index.freq = 'D'

fig, axes = plt.subplots(2, 5, figsize=(22, 10))
axes = axes.flatten()
basari_sonuclari = []

for i, baraj in enumerate(barajlar):
    ax = axes[i]
    try:
        full_data = df[baraj].dropna().tail(240)
        if len(full_data) < 240:
            raise ValueError("Yetersiz veri")

        train = full_data.iloc[:180]
        test = full_data.iloc[180:]

        model = ExponentialSmoothing(train, trend='add', seasonal='add', seasonal_periods=7)
        fit = model.fit()

        forecast = fit.forecast(steps=60)

        mae, rmse, mape = evaluate_forecast(test.values, forecast.values)
        basari_sonuclari.append({
            "Baraj": baraj,
            "MAE": mae,
            "RMSE": rmse,
            "MAPE (%)": mape
        })

        future_index = pd.date_range(start=train.index[-1] + pd.Timedelta(days=1), periods=60)
        ax.plot(train.index, train, label="Eğitim")
        ax.plot(train.index, fit.fittedvalues, label="Fitted", linestyle='--')
        ax.plot(future_index, forecast, label="Tahmin", linestyle=':', color='red')
        ax.plot(test.index, test, label="Gerçek", color='black', linewidth=1)
        ax.set_title(f"{baraj}\nMAPE: {mape:.2f}%")
        ax.tick_params(axis='x', rotation=30)
        ax.grid(True)

    except Exception as e:
        ax.set_title(f"{baraj}\nHata: {e}")
        print(f"Hata ({baraj}): {e}")

fig.suptitle("Tüm Barajlar için Holt-Winters 60 Günlük Tahmin + Başarı Metrikleri", fontsize=16)
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3)
plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig("Exponential_Smoothing_Tum_Barajlar.png", dpi=300)
plt.show()

if basari_sonuclari:
    df_sonuclar = pd.DataFrame(basari_sonuclari)
    print("\n--- Başarı Metrikleri Tablosu ---")
    print(df_sonuclar.to_string(index=False))
else:
    print("Bir sorun var.")

