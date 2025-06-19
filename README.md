# 💧 Baraj Doluluk Tahmin Projesi

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

Bu proje, İstanbul’daki 10 büyük barajın  
(Ömerli, Darlık, Elmalı, Terkos, Alibey, Büyükçekmece, Sazlıdere, Kazandere, Pabuçdere, Istrancalar)  
günlük doluluk oranlarına dayalı olarak **kısa ve orta vadeli tahminler** üreten bir zaman serisi analiz çalışmasıdır.

📈 Projede hem klasik hem de modern tahmin algoritmaları karşılaştırmalı olarak uygulanmış ve başarı metrikleri değerlendirilmiştir.

---

## 🧠 Kullanılan Modeller

- 📈 **Hareketli Ortalama (Moving Average)**
- 📊 **Basit Üstsel Düzeltme (Simple Exponential Smoothing)**
- 📈 **Holt-Winters Mevsimsel Modeli**
- 🔁 **ARIMA (AutoRegressive Integrated Moving Average)**
- 🧠 **Yapay Sinir Ağı (Artificial Neural Networks - ANN)**

Her model:
- Hem **baraj bazında**
- Hem de **İstanbul genel ortalama serisi** üzerinde test edilmiştir.

---

## 🚀 Projeyi Başlatmak

Aşağıdaki adımları takip ederek projeyi kendi bilgisayarınızda çalıştırabilirsiniz:

### 📥 Klonlama

```bash
git clone https://github.com/furkansoydas/baraj_doluluk.git
cd baraj_doluluk

### Gereksinimlerin Kurulması
pip install -r requirements.txt

## 🐳 Docker ile Kurulum (Opsiyonel)

Projeyi Docker kullanarak izole bir ortamda çalıştırmak istersen aşağıdaki adımları takip edebilirsin.

### 🔧 Gereksinimler

- Docker: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

### 📦 Docker Image Oluşturma ve Çalıştırma

1. Proje dizinine geç:

    ```bash
    cd baraj_doluluk
    ```

2. Docker image oluştur:

    ```bash
    docker build -t baraj-doluluk .
    ```

3. Container başlat:

    ```bash
    docker run -it --rm baraj-doluluk
    ```

> `--rm` flag’i işlem bitince konteyneri otomatik olarak siler. Geliştirme sürecinde kalıcılık istenirse volume bağlanabilir.

### 📝 Notlar

- `Dockerfile` içerisinde Python bağımlılıkları ve ortam ayarları tanımlanmıştır.
- Eğer veri dosyaların (örneğin `veri_tarih_ekli.xlsx`) proje dışındaysa, klasörü volume olarak bağlayarak erişebilirsin:

    ```bash
    docker run -it --rm -v $(pwd)/data:/app/data baraj-doluluk
    ```

    > `$(pwd)` komutu bulunduğun dizini referans alır. Windows kullanıcıları için: `%cd%`
