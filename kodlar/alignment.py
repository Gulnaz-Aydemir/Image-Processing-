import numpy as np
import cv2

def ssd_metric(img1, img2):
    
    #İki görüntü arasındaki SSD  değerini hesapladım.
    
   
    return np.sum((img1.astype("float") - img2.astype("float"))**2)

def align_channels(base_channel, align_channel, search_range):
    
    
    
    min_ssd = -1
    best_shift = (0, 0)

    # Kenarları %10 kırparak karşılaştırmayı denedim.
    h, w = base_channel.shape
    crop_y = int(h * 0.1)
    crop_x = int(w * 0.1)
    base_cropped = base_channel[crop_y : h - crop_y, crop_x : w - crop_x]

   
    for dy in range(-search_range, search_range + 1):
        for dx in range(-search_range, search_range + 1):
            
            # Hizalanacak kanalı (dx, dy) kadar kaydırmak
            shifted_align = np.roll(np.roll(align_channel, dy, axis=0), dx, axis=1)
            
            # Kaydırılmış kanalı da aynı şekilde kırptım.
            shifted_cropped = shifted_align[crop_y : h - crop_y, crop_x : w - crop_x]
            
            # SSD değerini hesaplamak için yukarıdaki ssd_metric fonksiyonunu çağır
            current_ssd = ssd_metric(base_cropped, shifted_cropped)
            
            # En iyi sonucu (en düşük SSD'yi) bulduysak kaydet
            if min_ssd == -1 or current_ssd < min_ssd:
                min_ssd = current_ssd
                best_shift = (dx, dy)
            
    return best_shift
def align_channels_ncc(base_channel, align_channel, search_range):
  
    
    max_ncc = -2 
    best_shift = (0, 0)

    h, w = base_channel.shape
    crop_y = int(h * 0.1)
    crop_x = int(w * 0.1)
    base_cropped = base_channel[crop_y : h - crop_y, crop_x : w - crop_x]

    print("NCC ile hizalama için arama başliyor.")
    
    for dy in range(-search_range, search_range + 1):
        for dx in range(-search_range, search_range + 1):
            
            shifted_align = np.roll(np.roll(align_channel, dy, axis=0), dx, axis=1)
            shifted_cropped = shifted_align[crop_y : h - crop_y, crop_x : w - crop_x]
            
            
            current_ncc = ncc_metric(base_cropped, shifted_cropped)
            
            
            if current_ncc > max_ncc:
                max_ncc = current_ncc
                best_shift = (dx, dy)
            
    print(f"Arama bitti. En iyi kaydirma: {best_shift}, Maksimum NCC: {max_ncc:.4f}")
    return best_shift
def ncc_metric(img1, img2):
    
    def ncc_metric(img1, img2):
        """NCC (Normalized Cross-Correlation) metriğini hesaplar."""
   
    img1_float = img1.astype("float")
    img2_float = img2.astype("float")

    
    mean1 = np.mean(img1_float)
    mean2 = np.mean(img2_float)

   
    norm_img1 = img1_float - mean1
    norm_img2 = img2_float - mean2
    
    
    numerator = np.sum(norm_img1 * norm_img2)
    
   
    denominator = np.sqrt(np.sum(norm_img1**2) * np.sum(norm_img2**2))
    
    
    if denominator == 0:
        return 0
    
    
    return numerator / denominator
    import cv2 

def pyramid_align(base_image, align_image, level=3, search_range=5):
    
    
    if level == 0 or base_image.shape[0] < 50 or base_image.shape[1] < 50:
        
        return align_channels(base_image, align_image, 15)

    
    next_base = cv2.resize(base_image, (base_image.shape[1] // 2, base_image.shape[0] // 2), interpolation=cv2.INTER_LINEAR)
    next_align = cv2.resize(align_image, (align_image.shape[1] // 2, align_image.shape[0] // 2), interpolation=cv2.INTER_LINEAR)

    
    sub_level_shift = pyramid_align(next_base, next_align, level - 1, search_range)

    
    estimated_shift = (sub_level_shift[0] * 2, sub_level_shift[1] * 2)

   
    shifted_align_image = np.roll(align_image, estimated_shift[1], axis=0)
    shifted_align_image = np.roll(shifted_align_image, estimated_shift[0], axis=1)

    
    refinement_shift = align_channels(base_image, shifted_align_image, search_range)

   
    final_shift = (estimated_shift[0] + refinement_shift[0], estimated_shift[1] + refinement_shift[1])

    return final_shift