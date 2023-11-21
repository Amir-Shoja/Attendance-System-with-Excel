import os

# مسیر پوشه حاوی تصاویر
folder_path = "test"

# لیست تمام فایل‌های تصویر در پوشه
image_files = os.listdir(folder_path)

for i, image_file in enumerate(image_files):
    image_path = os.path.join(folder_path, image_file)
    # new_image_path = os.path.join(folder_path, f"Bill Gates_{i+1}.jpg")
    # new_image_path = os.path.join(folder_path, f"Elon Musk_{i+1}.jpg")
    # new_image_path = os.path.join(folder_path, f"Jeff Bezos_{i+1}.jpg")
    # new_image_path = os.path.join(folder_path, f"Mark Zuckerberg_{i+1}.jpg")
    new_image_path = os.path.join(folder_path, f"Steve Jobs_{i+1}.jpg")

    # تغییر نام فایل
    os.rename(image_path, new_image_path)

    print(
        f"{image_file} <to> {os.path.basename(new_image_path)} changed")
