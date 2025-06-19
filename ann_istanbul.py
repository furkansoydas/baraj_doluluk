import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping

def evaluate_forecast(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    return round(mae, 4), round(rmse, 4), round(mape, 2)

def create_sequences(data, window_size=7):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i + window_size])
        y.append(data[i + window_size])
    return np.array(X), np.array(y)

dosya = "veri_tarih_ekli.xlsx"
df = pd.read_excel(dosya)
df["Tarih"] = pd.to_datetime(df["Tarih"])

barajlar = ["Ömerli", "Darlık", "Elmalı", "Terkos", "Alibey",
            "Büyükçekmece", "Sazlıdere", "Kazandere", "Pabuçdere", "Istrancalar"]

df["İstanbul_Ortalama"] = df[barajlar].mean(axis=1)
veri_serisi = df["İstanbul_Ortalama"].values
tarih_serisi = df["Tarih"].values

X, y = create_sequences(veri_serisi)
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, shuffle=False)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, shuffle=False)
tarih_test = tarih_serisi[-len(y_test):]

model = Sequential([
    Dense(64, activation='relu', input_shape=(7,)),
    Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam', loss='mean_squared_error')
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=100,
    callbacks=[early_stop],
    shuffle=False,
    verbose=0
)

y_pred = model.predict(X_test).flatten()
mae, rmse, mape = evaluate_forecast(y_test, y_pred)

son_pencere = veri_serisi[-7:]
gelecek_tahmin = []
for _ in range(30):
    tahmin = model.predict(son_pencere.reshape(1, -1))[0, 0]
    gelecek_tahmin.append(tahmin)
    son_pencere = np.append(son_pencere[1:], tahmin)

tahmin_tarihleri = pd.date_range(start=df["Tarih"].iloc[-1] + pd.Timedelta(days=1), periods=30)

plt.figure(figsize=(14, 6))

plt.plot(tarih_serisi[-90:], veri_serisi[-90:], label="Gerçek Veri (Son 90 Gün)", color="red", linewidth=2)

y_pred_df = pd.DataFrame({"tarih": tarih_test, "tahmin": y_pred})
y_pred_df = y_pred_df.tail(100)
plt.plot(y_pred_df["tarih"], y_pred_df["tahmin"],
         label="Model Test Tahmini (Son 100 Gün)",
         linestyle="--", color="royalblue", linewidth=2)

plt.plot(tahmin_tarihleri, gelecek_tahmin, label="Gelecek 30 Gün Tahmini", linestyle=":", color="forestgreen", linewidth=2)

plt.axvline(x=tarih_serisi[-1], color='gray', linestyle='--', alpha=0.5)

plt.title(f"Yapay Sinir Ağları ile İstanbul Geneli Baraj Doluluğu Tahmini \nMAE={mae}, RMSE={rmse}, MAPE={mape}%", fontsize=13)

plt.xlabel("Tarih")
plt.ylabel("Ortalama Doluluk Oranı")
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='upper left')

import matplotlib.dates as mdates
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))

plt.tight_layout()
plt.savefig("istanbul_ysa_tahmin.png", dpi=300)
plt.show()

print("\n--- İstanbul Geneli Yapay Sinir Ağları Başarı Metrikleri ---")
print(f"MAE:  {mae}")
print(f"RMSE: {rmse}")
print(f"MAPE: {mape}%")
