# from config import VK_API_KEY
import vk_api
from PIL import Image
import os


def get_base_resize_coords(image: Image, columns: int = 2) -> tuple:
    image_width, image_height = image.size
    image_width = int(image_width)
    image_height = int((image_width / 3) * columns)
    return image_width, image_height


def get_parts_crop_coords(step: int) -> tuple:
    crop_coords = ((0, 0, step, step),
                   (step, 0, step * 2, step),
                   (step * 2, 0, step * 3, step),
                   (0, step, step, step * 2),
                   (step, step, step * 2, step * 2),
                   (step * 2, step, step * 3, step * 2),
                   (0, step, step, step * 2),
                   (step, step, step * 2, step * 2),
                   (step * 2, step, step * 3, step * 2)
                   )
    return crop_coords


def crop(image_id: int, columns: int = 2) -> None:
    image_id = str(image_id)

    # Open image and resize
    base_image_path = 'source/service/{}.jpg'.format(image_id)
    image = Image.open(base_image_path).convert('RGB')
    image = image.resize(get_base_resize_coords(image, columns))

    # create path from save crop images
    results_path = ('source/service/results/%s/' % image_id).encode('utf-8')
    os.makedirs(results_path, exist_ok=True)

    # save full crop image
    processed_image_path = 'source/service/results/%s/full__processed.jpg' % image_id
    image.save(processed_image_path)
    image.close()

    # save image parts

    # get coords
    base_processed_path = 'source/service/results/%s/' % image_id
    crop_img = Image.open(processed_image_path)
    width, height = crop_img.size
    step = int(height / 2)

    # crop and save
    for num, coords in enumerate(get_parts_crop_coords(step), 1):
        img = crop_img.crop(coords)
        img.save(base_processed_path + '{}__processed.jpg'.format(num))
        img.close()




def list_to_matrix(lst, rows, cols):
    matrix = []
    for i in range(0, len(lst), cols):
        row = lst[i:i + cols]
        matrix.append(row)
    return matrix


def make_template(image_id):
    path = 'source/service/results/{}/'.format(image_id)
    photos = ['{}{}__processed.jpg'.format(path, item) for item in range(1, 7)]
    photos = list_to_matrix(photos, 2, 3)

    template_image = Image.open('source/service/template.jpg').convert('RGB')

    start_x = 47
    start_y = 210

    for x in photos:
        for y in x:
            overlay_image = Image.open(y)
            overlay_image = overlay_image.resize((348, 350))
            template_image.paste(overlay_image, (start_x, start_y))
            overlay_image.close()
            start_x += 355
        start_x = 47
        start_y += 356
    template_image.save('source/service/result_template.jpg')
    template_image.close()