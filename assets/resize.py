import os 
from PIL import Image

def resize_images(old_folder,new_folder,scale_factor):
    for image_name in os.listdir(old_folder):
        input_path=os.path.join(old_folder,image_name)
        if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            with Image.open(input_path) as img:
                new_width=int(img.width * scale_factor)
                new_height=int(img.height * scale_factor)
                resized_image=img.resize((new_width,new_height))
                output_path=os.path.join(new_folder,image_name)
                resized_image.save(output_path)

old_folder=input('enter path to old folder:')
new_folder=input('enter path to new folder:')
scale_factor=eval(input('enter scale factor as %:'))
resize_images(old_folder,new_folder,scale_factor)