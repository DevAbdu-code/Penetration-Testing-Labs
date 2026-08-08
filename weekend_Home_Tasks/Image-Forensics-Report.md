#  CTF Challenge 3: Image Forensics Report

 Location: Weekend_home_Tasks/Challenge3

---

## 🛠 Toolset Summary

| Tool | Primary Use Case | How I used it |
|---|---|---|
| strings | Extract printable text | Found hidden flags in raw data |
| exiftool | Read metadata | Checked for hidden comments |
| stegseek | Crack steganography passwords | Used rockyou.txt to find passphrase |
| binwalk | Detect embedded files | Found hidden ZIP inside image |
| dd | Extract data by offset | Extracted hidden ZIP manually |

---

##  Investigation Steps

### 1️⃣ Metadata & String Analysis

I started by checking easy hidden data using:

`bash
strings challenge3.jpg | grep -i flag
exiftool challenge3.jpg

 Lesson: Metadata can leak sensitive information!

---

## 2️⃣ Steganography Cracking

stegseek challenge3.jpg rockyou.txt
 Result:
- Password found: password123
- Extracted file: flag5.txt

---

## 3️⃣ Binary Carving

binwalk challenge3.jpg
 Found hidden ZIP → Extracted using:

dd if=challenge3.jpg bs=1 skip=75667 of=hidden_data.zip
Then decoded Base64 content to reveal the final flag.

#  Investigation Screenshots

### 🔹 Step 1: Strings & Metadata Analysis
(<img width="1366" height="662" alt="Screenshot_2026-03-26_01_55_55" src="https://github.com/user-attachments/assets/7877095e-7e82-4296-8229-6ba1e2369d4a" />
)

### 🔹 Step 2: Steganography Cracking
<img width="1366" height="662" alt="Screenshot_2026-03-26_01_44_13" src="https://github.com/user-attachments/assets/07ea3b75-b16a-4a24-9493-0289730bcbca" />


### 🔹 Step 3: Binwalk Detection
<img width="1366" height="662" alt="Screenshot_2026-03-26_01_55_43" src="https://github.com/user-attachments/assets/09a81857-58ad-42f9-b9dc-afebf3835d03" />


### 🔹 Step 4: Data Extraction
<img width="1366" height="662" alt="Screenshot_2026-03-26_01_55_55" src="https://github.com/user-attachments/assets/8502beff-cde5-46fd-9aed-c5e46e9c04a9" />
## 🏆 Captured Flags

- FLAG{ALWAYS_Check_Metadata}  
- FLAG{Strings_leak_information}  
- FLAG{YOUR_FLAG_3}  
- FLAG{YOUR_FLAG_4}  

---
