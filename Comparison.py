import os
import time
import numpy as np
import face_recognition as fr
import matplotlib.pyplot as plt


start_time = time.time()

# مسیر پوشه حاوی تصاویر چهره‌ها و تست و چارت
train_folder = "train"
charts_folder = "charts"
test_folder = "test"

# لیست تمام فایل‌های تصویر در پوشه images و test
image_files = os.listdir(train_folder)
test_files = os.listdir(test_folder)

num_images = len(image_files)
num_tests = len(test_files)

num_images_per_category = num_tests // num_images

# ساخت آرایه برای ذخیره درصدهای تشخیص درست برای هر شخص
accuracies = np.zeros((num_images,))

# داده‌های مربوط به هر دسته را در لیست‌های جداگانه ذخیره کنید
category_data = []

image_files_without_extension = [file.split('.')[0] for file in image_files]

for i in range(num_images):
    image_file = image_files[i]
    image_path = os.path.join(train_folder, image_file)
    image = fr.load_image_file(image_path)
    image_encodings = fr.face_encodings(image)

    if len(image_encodings) == 0:
        print(f" No face found in : {image_file}")
        continue

    correct_predictions = 0

   # بررسی تصاویر تست مربوط به هر دسته
    for j in range(num_images_per_category):
        test_file = test_files[i * num_images_per_category + j]
        test_image_path = os.path.join(test_folder, test_file)
        test_image = fr.load_image_file(test_image_path)
        test_image_encodings = fr.face_encodings(test_image)

        if len(test_image_encodings) == 0:
            print(f" No face found in : {test_file}")
            continue

        # مقایسه تصاویر تست با تمام تصاویر چهره
        match_results = fr.compare_faces(
            image_encodings, test_image_encodings[0])

        if all(match_results):
            correct_predictions += 1
        else:
            print(f"No face found in: {test_file}")

    # محاسبه درصد تشخیص درست
    accuracy = correct_predictions / num_images_per_category * 100
    accuracies[i] = accuracy

    category_data.append([accuracies[i], 100 - accuracies[i]])

    # داده‌های مربوط به دسته فعلی
    current_category_data = category_data[i]

    # نام دسته فعلی
    current_category_name = image_files_without_extension[i]

    # رسم نمودار دایره‌ای
    plt.figure()
    plt.pie(current_category_data, labels=['Correct', 'Incorrect'], colors=['blue', 'red'],
            autopct='%1.1f%%', wedgeprops={'edgecolor': 'white', 'linewidth': 1})
    plt.title(f'Recognition Accuracy for {current_category_name}')
    # ذخیره نمودار در فایل
    plt.savefig(os.path.join(charts_folder,
                f'{current_category_name}_chart.png'))
    plt.close()  # بستن شکل

    print("Charts saved.")

    if accuracy == 100:
        # تغییر رنگ به سبز
        print(
            f"for:\033[92m{os.path.splitext(image_file)[0]}\033[0m, Percentage of correct recognition: \033[92m{accuracy:.2f}%\033[0m\n")
    else:
        # تغییر رنگ به قرمز
        print(
            f"for:\033[91m{os.path.splitext(image_file)[0]}\033[0m, Percentage of correct recognition: \033[91m{accuracy:.2f}%\033[0m\n")


end_time = time.time()
execution_time = end_time - start_time
minutes, seconds = divmod(execution_time, 60)
print("\033[94mExecution Time:", int(minutes), ":", int(seconds), "\033[0m")


bar_width = 0.35
index = np.arange(num_images)
opacity = 0.8

# رسم نمودار میله‌ای گروهی
colors = ['red' if acc != 100 else 'blue' for acc in accuracies]  # تنظیم رنگ‌ها
bars = plt.bar(index, accuracies, bar_width, alpha=opacity, color=colors)

# تنظیم نام هر میله بر روی محور x بدون نمایش پسوند
plt.xticks(index, image_files_without_extension, rotation=45)

# تنظیم برچسب محور x و y
plt.xlabel('People')
plt.ylabel('Accuracy (%)')

# تنظیم عنوان نمودار
plt.title('Correct Recognition Accuracy for Each Person')

# نمایش درصد در بالای هر میله
for i, bar in enumerate(bars):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() +
             1, f'{accuracies[i]:.2f}', ha='center', va='bottom')

# نمایش نمودار
plt.tight_layout()
plt.savefig(os.path.join(charts_folder, 'Figure_1.png'))
plt.show()
