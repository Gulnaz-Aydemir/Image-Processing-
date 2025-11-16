import cv2
import numpy as np
import os
import time
from alignment import align_channels, align_channels_ncc, pyramid_align
from enhancement import equalize_histogram, adjust_gamma, sharpen_laplacian
from utils import auto_crop, split_image

if __name__ == '__main__':
    data_folder = 'resimler/'
    results_folder = 'sonuç/'
    if not os.path.exists(results_folder): os.makedirs(results_folder)

    image_filenames = os.listdir(data_folder)

    for filename in image_filenames:
        if not (filename.lower().endswith('.jpg') or filename.lower().endswith('.tif')):
            continue

        print(f"--- {filename} işleniyor... ---")
        image_path = os.path.join(data_folder, filename)
        image = cv2.imread(image_path, 0)

        if image is not None:
            base_filename = os.path.splitext(filename)[0]
            blue, green, red = split_image(image)

            # 1. Hizalanmamış Görüntü
            unaligned_image = cv2.merge([blue, green, red])
            cv2.imwrite(os.path.join(results_folder, f'{base_filename}_1_hizalanmamis.jpg'), unaligned_image)

            # 2. SSD ile Hizalama
            start_time_ssd = time.time()
            shift_g_ssd, shift_r_ssd = align_channels(blue, green, 15), align_channels(blue, red, 15)
            end_time_ssd = time.time()
            elapsed_time_ssd = end_time_ssd - start_time_ssd
            aligned_image_ssd = cv2.merge([blue, np.roll(np.roll(green, shift_g_ssd[1], axis=0), shift_g_ssd[0], axis=1), np.roll(np.roll(red, shift_r_ssd[1], axis=0), shift_r_ssd[0], axis=1)])
            cv2.imwrite(os.path.join(results_folder, f'{base_filename}_2_hizalanmis_ssd.jpg'), aligned_image_ssd)
            print(f"  SSD Sonuçlari: Yeşil={shift_g_ssd}, Kirmizi={shift_r_ssd}, Süre={elapsed_time_ssd:.2f}s")

            # 3. NCC ile Hizalama
            start_time_ncc = time.time()
            shift_g_ncc, shift_r_ncc = align_channels_ncc(blue, green, 15), align_channels_ncc(blue, red, 15)
            end_time_ncc = time.time()
            elapsed_time_ncc = end_time_ncc - start_time_ncc
            aligned_image_ncc = cv2.merge([blue, np.roll(np.roll(green, shift_g_ncc[1], axis=0), shift_g_ncc[0], axis=1), np.roll(np.roll(red, shift_r_ncc[1], axis=0), shift_r_ncc[0], axis=1)])
            cv2.imwrite(os.path.join(results_folder, f'{base_filename}_3_hizalanmis_ncc.jpg'), aligned_image_ncc)
            print(f"  NCC Sonuçlari: Yeşil={shift_g_ncc}, Kırmızı={shift_r_ncc}, Süre={elapsed_time_ncc:.2f}s")

            #  PİRAMİT İLE HIZLI HİZALAMA
            print("\n  --- Bonus: Piramit Tabanli Hizalama ---")
            start_time_pyr = time.time()
            shift_g_pyr = pyramid_align(blue, green)
            shift_r_pyr = pyramid_align(blue, red)
            end_time_pyr = time.time()
            elapsed_time_pyr = end_time_pyr - start_time_pyr

            shifted_green_pyr = np.roll(np.roll(green, shift_g_pyr[1], axis=0), shift_g_pyr[0], axis=1)
            shifted_red_pyr = np.roll(np.roll(red, shift_r_pyr[1], axis=0), shift_r_pyr[0], axis=1)
            aligned_image_pyr = cv2.merge([blue, shifted_green_pyr, shifted_red_pyr])
            cv2.imwrite(os.path.join(results_folder, f'{base_filename}_8_aligned_pyramid.jpg'), aligned_image_pyr)
            print(f"  Piramit Sonuçlari: Yeşil={shift_g_pyr}, Kirmizi={shift_r_pyr}, Süre={elapsed_time_pyr:.2f}s")
            

            # 4. Otomatik Kırpma (SSD sonucunu baz aldım.)
            # --- OTOMATİK KIRPMA ---
        print("  Otomatik kirpma uygulaniyor...")
        
        cropped_image = auto_crop(aligned_image_ssd)
        cv2.imwrite(os.path.join(results_folder, f'{base_filename}_7_kirpilmis.jpg'), cropped_image)

         # 5. Görüntü İyileştirme
        hist_image = equalize_histogram(cropped_image)
        cv2.imwrite(os.path.join(results_folder, f'{base_filename}_4_iyilestirilmis_hist.jpg'), hist_image)

        gamma_image = adjust_gamma(cropped_image, gamma=0.75)
        cv2.imwrite(os.path.join(results_folder, f'{base_filename}_5_iyilestirilmis_gamma.jpg'), gamma_image)

        laplacian_image = sharpen_laplacian(cropped_image)
        cv2.imwrite(os.path.join(results_folder, f'{base_filename}_6_iyilestirilmis_laplacian.jpg'), laplacian_image)
            
        print(f"  '{filename}' için tüm sonuçlar '{results_folder}' klasörüne kaydedildi.\n")

    print("--- TÜM GÖRÜNTÜLERİN İŞLENMESİ TAMAMLANDI ---")