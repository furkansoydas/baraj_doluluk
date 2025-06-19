# istanbul genelini barajların günlük ortalamsını kullanarak tahmin eden arima modeli
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

df["İstanbul_Ortalama"] = df[barajlar].mean(axis=1)
seri = df["İstanbul_Ortalama"].dropna()

def check_stationarity(ts):
    return adfuller(ts)[1] < 0.05

def select_p_q(ts, nlags=30):
    acf_vals = acf(ts, nlags=nlags)
    pacf_vals = pacf(ts, nlags=nlags)
    q = next((i for i, val in enumerate(acf_vals[1:], 1) if abs(val) < 0.2), 1)
    p = next((i for i, val in enumerate(pacf_vals[1:], 1) if abs(val) < 0.2), 1)
    return p, q

son_120 = seri[-120:]
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
forecast = fit.get_forecast(steps=steps)
y_pred = forecast.predicted_mean
conf_int = forecast.conf_int()
forecast_index = pd.date_range(start=seri.index[-1] + pd.Timedelta(days=1), periods=steps)

mae = mean_absolute_error(test, y_pred)
rmse = np.sqrt(mean_squared_error(test, y_pred))
mape = np.mean(np.abs((test - y_pred) / test)) * 100

plt.figure(figsize=(12, 6))
plt.plot(seri[-90:], label="Gerçek Veri (Son 90 Gün)")
plt.plot(forecast_index, y_pred, label="30 Günlük Tahmin", color="green")
plt.fill_between(forecast_index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='green', alpha=0.3)
plt.title(f"İstanbul Geneli Ortalama - ARIMA({p},{d},{q}) Tahmini\nMAE={mae:.4f}, RMSE={rmse:.4f}, MAPE={mape:.2f}%")
plt.xlabel("Tarih")
plt.ylabel("Ortalama Doluluk Oranı")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("istanbul_arima_tahmin.png", dpi=300)
plt.show()
