
## 🚀 Projeyi Başlatmak

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları takip edebilirsiniz:

### 1. 📥 Klonlama

```bash
git clone https://github.com/furkansoydas/baraj_doluluk.git
cd baraj_doluluk
```

### 2. 🧰 Bağımlılıkların Kurulumu

Projedeki tüm Python kütüphanelerini yüklemek için:

```bash
pip install -r requirements.txt
```

---

## 🐳 Docker ile Kurulum (Opsiyonel)

Docker kullanarak projeyi izole bir ortamda çalıştırmak istersen şu adımları takip edebilirsin:

> 📌 **Not:** Bu projedeki `Dockerfile`, Apache2 kurulu bir Ubuntu tabanlı imaj kullanır.  
> Bu image’in oluşturulma amacı, başlangıçta proje çıktısı olan grafiklerin ve kod parametrelerinin  
> **interaktif şekilde değiştirilerek** grafik sonuçları ve başarı metriklerindeki etkilerin kullanıcıya  
> **dinamik olarak sunulması** hedeflenmiştir.  
> Bu etkileşimli yapı şu anda aktif değildir; ancak **ileride projeye entegre edilmesi planlanmaktadır.**


### 🔧 Gereksinimler

- Docker yüklü olmalıdır:  
  https://www.docker.com/products/docker-desktop

### 📦 Image Oluşturma

Proje dizinindeyken aşağıdaki komutla bir Docker image oluştur:

```bash
docker build -t baraj-doluluk .
```

### ▶️ Container’ı Çalıştırma

Oluşturduğun imajdan bir konteyner başlatmak için:

```bash
docker run -it --rm baraj-doluluk
```

> `--rm` flag’i konteyner kapandıktan sonra otomatik olarak silinmesini sağlar.  
> Geliştirme ortamında kalıcılık gerekiyorsa volume (bağlı klasör) kullanabilirsin.

### 📂 Dış Veri Dosyalarını Bağlamak (Opsiyonel)

Eğer veri dosyaların (örneğin `veri_tarih_ekli.xlsx`) proje dışında bir dizindeyse:

```bash
docker run -it --rm -v $(pwd)/data:/app/data baraj-doluluk
```

> `$(pwd)` Unix/macOS sistemler için geçerlidir.  
> Windows kullanıcıları `%cd%` kullanmalıdır:

```bash
docker run -it --rm -v %cd%/data:/app/data baraj-doluluk
```

---
