import os
import random
import shutil

train_img = r"D:\Crack_defect_project\dataset\images\train"
train_lbl = r"D:\Crack_defect_project\dataset\labels\train"

valid_img = r"D:\Crack_defect_project\dataset\images\valid"
valid_lbl = r"D:\Crack_defect_project\dataset\labels\valid"

test_img = r"D:\Crack_defect_project\dataset\images\test"
test_lbl = r"D:\Crack_defect_project\dataset\labels\test"

images = [f for f in os.listdir(train_img)
          if f.endswith((".jpg", ".jpeg", ".png"))]

random.shuffle(images)

n = len(images)
valid_count = int(n * 0.2)
test_count = int(n * 0.1)

valid_images = images[:valid_count]
test_images = images[valid_count:valid_count + test_count]

for img in valid_images:
    shutil.move(
        os.path.join(train_img, img),
        os.path.join(valid_img, img)
    )

    label = os.path.splitext(img)[0] + ".txt"
    shutil.move(
        os.path.join(train_lbl, label),
        os.path.join(valid_lbl, label)
    )

for img in test_images:
    shutil.move(
        os.path.join(train_img, img),
        os.path.join(test_img, img)
    )

    label = os.path.splitext(img)[0] + ".txt"
    shutil.move(
        os.path.join(train_lbl, label),
        os.path.join(test_lbl, label)
    )

print("Dataset split complete!")
print("Train:", len(os.listdir(train_img)))
print("Valid:", len(os.listdir(valid_img)))
print("Test :", len(os.listdir(test_img)))