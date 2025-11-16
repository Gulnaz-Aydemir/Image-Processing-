# 🎨 Geçmişin Renkleri: Prokudin-Gorskii Restorasyonu

Bu proje, Sergei Mikhailovich Prokudin-Gorskii tarafından 20. yüzyılın başlarında çekilen üç kanallı (Mavi, Yeşil, Kırmızı) cam plaka negatiflerini, **NumPy** kütüphanesi kullanarak sıfırdan hizalamaya ve restore etmeye odaklanmaktadır. Projede `cv2.matchTemplate` veya benzeri hazır hizalama fonksiyonları kullanılmamıştır.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/Numpy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-ffffff?style=for-the-badge&logo=matplotlib&logoColor=blue)

---

## 🎯 Uygulanan Teknikler ve Rapor Görünümü

Proje, çok adımlı bir görüntü işleme hattı (pipeline) olarak tasarlanmıştır. Tüm adımlar `1.jpg` görüntüsü üzerinde gösterilmiştir.

### 1. Görüntü Bölme ve Ham Hali
Giriş olarak verilen uzun `.jpg` dosyası, NumPy dizi dilimleme (array slicing) kullanılarak üç eşit parçaya (Mavi, Yeşil, Kırmızı kanallar) bölünmüştür. Bu, kanalların hizalanmadan önceki ham halidir.

![Hizalanmamış Görüntü](sonuç/1_1_hizalanmamis.jpg)

### 2. Kanal Hizalama (SSD & NCC)
Mavi kanal referans (sabit) alınarak, Yeşil ve Kırmızı kanalların Mavi kanala göre en uygun `(dx, dy)` kaydırma vektörleri bulunmuştur. Bu işlem için iki farklı metrik sıfırdan kodlanmıştır:
* **SSD (Sum of Squared Differences):** Hızlı, ancak parlaklık değişimlerine duyarlı.
* **NCC (Normalized Cross-Correlation):** Yavaş, ancak parlaklık değişimlerine karşı dayanıklı.

![SSD ile Hizalanmış Görüntü](sonuç/1-2-hizalanmis-ssd.jpg)

### 3. Görüntü İyileştirme
Hizalanmış görüntünün kalitesini artırmak ve tarihi fotoğrafların karanlık yapısını canlandırmak için üç farklı teknik uygulanmıştır:
1.  **Gama Düzeltme:** `output = 255 * (input / 255)^gamma` formülü ile karanlık alanlar aydınlatıldı (En başarılı sonuç).
2.  **Histogram Eşitleme:** Görüntünün global kontrastı artırıldı.
3.  **Laplasyen Filtreleme:** Kenarlar keskinleştirilerek detaylar vurgulandı.

![Gama ile İyileştirilmiş Sonuç](rsonuç/1_5_iyilestirilmis-gamma.jpg)

### 4. Bonus: Piramit Tabanlı Hızlandırma
Yüksek çözünürlüklü (`.tif`) dosyalarda geniş arama pencerelerinde (örn: `[-100, 100]`) yaşanan yavaşlığı aşmak için piramit tabanlı (çok-ölçekli) bir hizalama yöntemi uygulanmıştır. Bu yöntem, hesaplama süresini `~5-6` saniyeden `~0.4` saniyeye düşürmüştür.

### 5. Bonus: Otomatik Kenar Kırpma
Hizalama işlemi sonrası kanalların kenarlarında oluşan bozuk çerçeveler (borders), piksellerin standart sapması analiz edilerek otomatik olarak tespit edilmiş ve kırpılmıştır.

---

## 🚀 Kurulum ve Çalıştırma

1.  Gerekli kütüphanelerin yüklü olduğundan emin olun:
    ```bash
    pip install numpy matplotlib opencv-python
    ```
2.  Proje dosyalarını klonlayın ve resimlerin `resimler` klasöründe olduğundan emin olun.
3.  Aşağıdaki komut ile script'i çalıştırın (script adınızı `proje.py` olarak varsayarsak):
    ```bash
    python proje.py --input resimler/1.jpg
    ```
4.  Script, tüm görsel çıktıları `sonuclar/` klasörüne kaydedecektir.

---

## 👤 Proje Sahibi
Yapay Zeka Mühendisliği Öğrencisi

* **Gülnaz Aydemir**
* Ostim Teknik Üniversitesi
