import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings

warnings.filterwarnings("ignore")

file_path = "veri_tarih_ekli.xlsx"
barajlar = ["Ömerli", "Darlık", "Elmalı", "Terkos", "Alibey",
            "Büyükçekmece", "Sazlıdere", "Kazandere", "Pabuçdere", "Istrancalar"]

df = pd.read_excel(file_path)
df["Tarih"] = pd.to_datetime(df["Tarih"])
df.set_index("Tarih", inplace=True)

def check_stationarity(ts):
    return adfuller(ts)[1] < 0.05

def select_p_q(ts, nlags=30):
    acf_vals = acf(ts, nlags=nlags)
    pacf_vals = pacf(ts, nlags=nlags)
    q = next((i for i, val in enumerate(acf_vals[1:], 1) if abs(val) < 0.2), 1)
    p = next((i for i, val in enumerate(pacf_vals[1:], 1) if abs(val) < 0.2), 1)
    return p, q

fig, axes = plt.subplots(2, 5, figsize=(25, 10))
axes = axes.flatten()

metrics = []

for i, baraj in enumerate(barajlar):
    ax = axes[i]
    try:
        series = df[baraj].dropna()
        son_120 = series[-120:]
        train = son_120[:-30]
        test = son_120[-30:]

        d = 0
        ts = train.copy()
        while not check_stationarity(ts):
            ts = ts.diff().dropna()
            d += 1

        p, q = select_p_q(ts)

        model = ARIMA(train, order=(p, d, q))
        fit = model.fit()

        steps = 30
        future = fit.get_forecast(steps=steps)
        y_pred = future.predicted_mean
        conf_int = future.conf_int()
        future_index = pd.date_range(series.index[-1] + pd.Timedelta(days=1), periods=steps)

        ax.plot(series[-90:], label="Son 90 Gün")
        ax.plot(future_index, y_pred, label="30 Günlük Tahmin", color="green")
        ax.fill_between(future_index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='green', alpha=0.3)
        ax.set_title(f"{baraj} (ARIMA({p},{d},{q}))")
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)

        mae = mean_absolute_error(test, y_pred)
        rmse = np.sqrt(mean_squared_error(test, y_pred))
        mape = np.mean(np.abs((test - y_pred) / test)) * 100


        metrics.append({
            "Baraj": baraj,
            "p,d,q": f"{p},{d},{q}",
            "MAE": round(mae, 4),
            "RMSE": round(rmse, 4),
            "MAPE (%)": round(mape, 2)
        })

    except Exception as e:
        ax.set_title(f"{baraj} - Hata")
        metrics.append({
            "Baraj": baraj,
            "p,d,q": "Hata",
            "MAE": None,
            "RMSE": None,
            "MAPE (%)": None,
            "Hata": str(e)
        })
        print(f"Hata ({baraj}): {e}")

fig.suptitle("Tüm Barajlar İçin ARIMA 30 Günlük Tahmin Grafikleri", fontsize=16)
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=3)
plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig("arima_tum_barajlar.png", dpi=300)
plt.show()

metrics_df = pd.DataFrame(metrics)
print("\n🎯 Başarı Metrikleri Tablosu (Son 30 Günlük Test Verisine Göre):")
print(metrics_df.to_string(index=False))

