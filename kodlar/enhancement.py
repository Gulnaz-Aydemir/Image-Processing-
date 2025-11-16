import numpy as np
import cv2

def equalize_histogram(image):
    
  
    
   
    img_ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    
    y, cr, cb = cv2.split(img_ycrcb)
    
    
    y_equalized = cv2.equalizeHist(y)
    
    
    equalized_img_ycrcb = cv2.merge([y_equalized, cr, cb])
    
   
    final_image = cv2.cvtColor(equalized_img_ycrcb, cv2.COLOR_YCrCb2BGR)
    
    return final_image
def adjust_gamma(image, gamma=1.0):
    """
    Gama düzeltmesi kullanarak görüntünün parlaklığını ayarlar.
    gamma < 1.0 -> Görüntüyü aydınlatır
    gamma > 1.0 -> Görüntüyü karartır
    gamma = 1.0 -> Görüntü değişmez
    """
   
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    
   
    return cv2.LUT(image, table)
def sharpen_laplacian(image):
    """
    Laplasyen filtresi kullanarak görüntüyü keskinleştirir.
    """
   
    laplacian = cv2.Laplacian(image, ddepth=cv2.CV_64F)
    
   
    sharpened_laplacian = cv2.convertScaleAbs(laplacian)
    
    
    sharpened_image = cv2.addWeighted(image, 1.5, sharpened_laplacian, -0.5, 0)
    
    return sharpened_image