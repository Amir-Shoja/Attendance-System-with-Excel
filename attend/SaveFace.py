import os
import cv2 as cv
import face_recognition as fr

# مسیر پوشه حاوی تصاویر
images_folder = "images"

# مسیر پوشه خروجی برای ذخیره تصاویر جدید
output_folder = "output"

# ایجاد پوشه خروجی اگر وجود نداشته باشد
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# لیست تمام فایل‌های تصویر در پوشه
image_files = os.listdir(images_folder)

for image_file in image_files:
    image_path = os.path.join(images_folder, image_file)
    image = fr.load_image_file(image_path)

    # تشخیص چهره‌ها در تصویر
    face_locations = fr.face_locations(image)
    if len(face_locations) == 0:
        print(f"Dosen't Exist {image_file} ")
        continue

    # استخراج ویژگی‌های چهره
    face_encodings = fr.face_encodings(image, face_locations)

    # جایگزینی تصویر با چهره شناسایی شده
    for face_location, face_encoding in zip(face_locations, face_encodings):
        # تصویر جدید با چهره شناسایی شده
        top, right, bottom, left = face_location
        new_image = image.copy()
        new_image = new_image[top:bottom, left:right]

        # ذخیره تصویر جدید در پوشه خروجی
        new_image_path = os.path.join(output_folder, f"{image_file}")
        # تبدیل تصویر به حالت رنگی
        new_image_rgb = cv.cvtColor(new_image, cv.COLOR_BGR2RGB)
        cv.imwrite(new_image_path, new_image_rgb)

        print(
            f"Save new img of {image_file} in path {new_image_path}")
