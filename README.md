# 🎨 Colors of the Past: Prokudin-Gorskii Restoration

This project focuses on aligning and restoring the three-channel (Blue, Green, Red) glass plate negatives taken by Sergei Mikhailovich Prokudin-Gorskii in the early 20th century, implemented from scratch using the **NumPy** library. The project **does not** use built-in alignment functions such as `cv2.matchTemplate` or similar.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/Numpy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-ffffff?style=for-the-badge&logo=matplotlib&logoColor=blue)

---

## 🎯 Applied Techniques and Report View

The project is designed as a multi-step image processing **pipeline**. All steps are demonstrated using the `1.jpg` image.

### 1. Image Splitting and Raw State
The long input `.jpg` file is split into three equal parts (Blue, Green, Red channels) using **NumPy array slicing**. This represents the raw state of the channels before alignment.

![Un-aligned Image](sonuç/10_1_hizalanmamis.jpg)

### 2. Channel Alignment (SSD & NCC)
Taking the Blue channel as the reference (fixed), the optimal **`(dx, dy)` shift vectors** for the Green and Red channels relative to the Blue channel were found. Two different metrics were coded from scratch for this operation:
* **SSD (Sum of Squared Differences):** Fast, but sensitive to brightness changes.
* **NCC (Normalized Cross-Correlation):** Slow, but robust against brightness changes.

![Image Aligned with SSD](sonuç/10_2_hizalanmis_ssd.jpg)

### 3. Image Enhancement
Three different techniques were applied to improve the quality of the aligned image and revitalize the dark structure characteristic of historical photographs:
1.  **Gamma Correction:** Dark areas were brightened using the formula `output = 255 * (input / 255)^gamma` (The most successful result).
2.  **Histogram Equalization:** The global contrast of the image was increased.
3.  **Laplacian Filtering:** Edges were sharpened to emphasize details.

![Gamma Corrected Final Result](sonuç/10_5_iyilestirilmis_gamma.jpg)

### 4. Bonus: Pyramid-Based Speedup
A pyramid-based (multi-scale) alignment method was implemented to overcome the slowdown experienced in high-resolution (`.tif`) files within large search windows (e.g., `[-100, 100]`). This method reduced the computation time from `~5-6` seconds to `~0.4` seconds.

### 5. Bonus: Automatic Border Cropping
The distorted frames (borders) that appear at the edges of the channels after the alignment process were automatically detected and cropped by analyzing the **standard deviation of the pixels**.

---

## 🚀 Setup and Running

1.  Make sure the necessary libraries are installed:
    ```bash
    pip install numpy matplotlib opencv-python
    ```
2.  Clone the project files and ensure the images are in the `resimler` (images) folder.
3.  Run the script with the following command (assuming your script name is `proje.py`):
    ```bash
    python proje.py --input resimler/1.jpg
    ```
4.  The script will save all visual outputs to the `sonuclar/` (results) folder.

---

## 👤 Project Owner
Artificial Intelligence Engineering Student

* **Gülnaz Aydemir**
* Ostim Technical University
