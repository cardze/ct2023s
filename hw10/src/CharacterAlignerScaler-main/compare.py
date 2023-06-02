import os
import random
import matplotlib.pyplot as plt
from matplotlib.image import imread
from matplotlib.patches import Rectangle


def display_images(before_folder, after_folder, sample_count=10):
    before_files = sorted(os.listdir(before_folder))
    after_files = sorted(os.listdir(after_folder))

    sampled_files = random.sample(list(zip(before_files, after_files)), sample_count)

    for before_file, after_file in sampled_files:
        before_image_path = os.path.join(before_folder, before_file)
        after_image_path = os.path.join(after_folder, after_file)

        before_image = imread(before_image_path)
        after_image = imread(after_image_path)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        ax1.imshow(before_image)
        ax1.set_title("Before: " + before_file)
        ax1.axis("off")

        # Add a border around the before image
        border = Rectangle((0, 0), before_image.shape[1]-1, before_image.shape[0]-1, linewidth=2, edgecolor='r', facecolor='none')
        ax1.add_patch(border)

        ax2.imshow(after_image)
        ax2.set_title("After: " + after_file)
        ax2.axis("off")

        plt.show()


before_folder = "./1_138"
after_folder = "1_138_after"
display_images(before_folder, after_folder, 10)
