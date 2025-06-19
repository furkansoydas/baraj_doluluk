import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping

excel_dosyasi = "veri_tarih_ekli.xlsx"
barajlar = ["Ömerli", "Darlık", "Elmalı", "Terkos", "Alibey",
            "Büyükçekmece", "Sazlıdere", "Kazandere", "Pabuçdere", "Istrancalar"]

df = pd.read_excel(excel_dosyasi)
df["Tarih"] = pd.to_datetime(df["Tarih"])
veri = df.drop(columns=["Tarih"])

def create_sequences(data, window_size=7):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i+window_size])
        y.append(data[i+window_size])
    return np.array(X), np.array(y)

fig, axs = plt.subplots(2, 5, figsize=(20, 8))
axs = axs.flatten()

for idx, baraj_adi in enumerate(barajlar):
    data = veri[baraj_adi].dropna().values
    X, y = create_sequences(data, window_size=7)

    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, shuffle=False)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, shuffle=False)

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

    y_pred = model.predict(X_test)

    axs[idx].plot(y_test[:60], label='Gerçek', color='blue')
    axs[idx].plot(y_pred[:60], label='Tahmin', color='orange')
    axs[idx].set_title(baraj_adi)
    axs[idx].tick_params(labelsize=8)
    axs[idx].grid(True)

fig.suptitle("Tüm Barajlar İçin ANN Tahmin Grafikleri", fontsize=16)
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.legend(["Gerçek", "Tahmin"], loc="lower center", ncol=2, fontsize=12)

plt.show()
