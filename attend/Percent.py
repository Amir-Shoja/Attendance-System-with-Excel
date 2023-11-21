import os
import face_recognition

images_folder = "images"
test_folder = "test"

image_files = os.listdir(images_folder)
test_files = os.listdir(test_folder)

num_images = len(image_files)
num_tests = len(test_files)

# تعداد تصاویر در هر دسته
num_images_per_category = num_tests // num_images

# بررسی هر دسته از تصاویر
for i in range(num_images):
    image_file = image_files[i]
    image_path = os.path.join(images_folder, image_file)
    image = face_recognition.load_image_file(image_path)
    image_encodings = face_recognition.face_encodings(image)

    if len(image_encodings) == 0:
        print(f" No face found in : {image_file}")
        continue

    correct_predictions = 0

    # بررسی تصاویر تست مربوط به هر دسته
    for j in range(num_images_per_category):
        test_file = test_files[i * num_images_per_category + j]
        test_image_path = os.path.join(test_folder, test_file)
        test_image = face_recognition.load_image_file(test_image_path)
        test_image_encodings = face_recognition.face_encodings(test_image)

        if len(test_image_encodings) == 0:
            print(f" No face found in : {test_file}")
            continue

        # مقایسه تصاویر تست با تصویر چهره
        match_results = face_recognition.compare_faces(
            image_encodings, test_image_encodings[0])

        if any(match_results):
            correct_predictions += 1

    # محاسبه درصد تشخیص درست
    accuracy = correct_predictions / num_images_per_category * 100

    print(
        f"for : {image_file}, Percentage of correct recognition : {accuracy:.2f}%")
