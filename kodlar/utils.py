import numpy as np
import cv2

def split_image(image):
    """
    Giriş görüntüsünü yukaridan aşağiya B, G, R kanallarina (üç eşit parçaya) böler.
    """
    h = image.shape[0] // 3
    blue = image[0:h, :]
    green = image[h:2*h, :]
    red = image[2*h:3*h, :]
    return blue, green, red

def auto_crop(image):
    """
    Görüntünün kenarlarindaki renkli veya siyah çerçeveleri otomatik olarak kirpar.
    Renk kanallarindaki standart sapmayi analiz eder.
    """
    # Görüntünün kanallarını ayırdım
    b, g, r = cv2.split(image)
    
    
    threshold = 5 

    # Mavi kanal için sınırlar
    y_start_b = 0
    for i, row in enumerate(b):
        if np.std(row) > threshold: y_start_b = i; break
    y_end_b = b.shape[0]
    for i, row in enumerate(reversed(b)):
        if np.std(row) > threshold: y_end_b = b.shape[0] - i; break
    x_start_b = 0
    for i, col in enumerate(b.T):
        if np.std(col) > threshold: x_start_b = i; break
    x_end_b = b.shape[1]
    for i, col in enumerate(reversed(b.T)):
        if np.std(col) > threshold: x_end_b = b.shape[1] - i; break
    
    # Yeşil kanal için sınırlar
    y_start_g = 0
    for i, row in enumerate(g):
        if np.std(row) > threshold: y_start_g = i; break
    y_end_g = g.shape[0]
    for i, row in enumerate(reversed(g)):
        if np.std(row) > threshold: y_end_g = g.shape[0] - i; break
    x_start_g = 0
    for i, col in enumerate(g.T):
        if np.std(col) > threshold: x_start_g = i; break
    x_end_g = g.shape[1]
    for i, col in enumerate(reversed(g.T)):
        if np.std(col) > threshold: x_end_g = g.shape[1] - i; break

    # Kırmızı kanal için sınırlar
    y_start_r = 0
    for i, row in enumerate(r):
        if np.std(row) > threshold: y_start_r = i; break
    y_end_r = r.shape[0]
    for i, row in enumerate(reversed(r)):
        if np.std(row) > threshold: y_end_r = r.shape[0] - i; break
    x_start_r = 0
    for i, col in enumerate(r.T):
        if np.std(col) > threshold: x_start_r = i; break
    x_end_r = r.shape[1]
    for i, col in enumerate(reversed(r.T)):
        if np.std(col) > threshold: x_end_r = r.shape[1] - i; break

    # Üç kanalın bulduğu sınırlardan en içeride olanlar
    
    y_start = max(y_start_b, y_start_g, y_start_r)
    y_end = min(y_end_b, y_end_g, y_end_r)
    x_start = max(x_start_b, x_start_g, x_start_r)
    x_end = min(x_end_b, x_end_g, x_end_r)
    
    # Bulunan koordinatlara göre orijinal renkli görüntüyü kırptım.
    cropped_image = image[y_start:y_end, x_start:x_end]
    
    print(f"  Yeni yöntemle otomatik kirpma yapildi. Orijinal: {image.shape}, Kirpilmiş: {cropped_image.shape}")
    return cropped_image