import sys
from io import BytesIO

from PIL import Image
from log_settings import log


def compress_img(image_name, new_size_ratio=0.9, quality=98, width=None, height=None, ext='JPEG'):
    # load the image to memory
    img = Image.open(image_name)
    # print the original image shape
    print("[*] Image size:", img.size)
    # get the original image size in bytes
    image_size = sys.getsizeof(image_name)
    ratio = 1
    image_compressed = None
    while image_size > 700000 and ratio >= 0.1:
        img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.LANCZOS)
        image_compressed = BytesIO()
        img.save(image_compressed, quality=quality, optimize=True, format=ext)
        image_size = sys.getsizeof(image_compressed)
        log.info('new image size = %s bytes', image_size)
        ratio -= 0.05

    if not image_compressed:
        log.info('Image was not compressed as it <= 700 Kb')
        return image_name
    log.info("[+] New Image shape: %s", img.size)
    return image_compressed

    # # print the size before compression/resizing
    # print("[*] Size before compression:", get_size_format(image_size))
    # if new_size_ratio < 1.0:
    #     # if resizing ratio is below 1.0, then multiply width & height with this ratio to reduce image size
    #     img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.LANCZOS)
    #     # print new image shape
    #     print("[+] New Image shape:", img.size)
    # elif width and height:
    #     # if width and height are set, resize with them instead
    #     img = img.resize((width, height), Image.LANCZOS)
    #     # print new image shape
    #     print("[+] New Image shape:", img.size)
    # image_compressed = BytesIO()
    # try:
    #     # save the image with the corresponding quality and optimize set to True
    #     img.save(image_compressed, quality=quality, optimize=True, format=ext)
    # except OSError:
    #     print('OSERROR')
    #     # convert the image to RGB mode first
    #     img = img.convert("RGB")
    #     # save the image with the corresponding quality and optimize set to True
    #     img.save(image_compressed, quality=quality, optimize=True, format=ext)
    # print("[+] New file saved:")
    # # get the new image size in bytes
    # new_image_size = sys.getsizeof(image_compressed)
    # # print the new size in a good format
    # print("[+] Size after compression:", get_size_format(new_image_size))
    # if new_image_size <= 200000:
    #     img = Image.open(image_name)
    #     img = img.resize((int(img.size[0] * 0.9), int(img.size[1] * 0.9)), Image.LANCZOS)
    #     # print new image shape
    #     print("[+] New Image shape:", img.size)
    #     try:
    #         # save the image with the corresponding quality and optimize set to True
    #         img.save(image_compressed, quality=quality, optimize=True, format=ext)
    #     except OSError:
    #         # convert the image to RGB mode first
    #         img = img.convert("RGB")
    #         # save the image with the corresponding quality and optimize set to True
    #         img.save(image_compressed, quality=quality, optimize=True, format=ext)
    #     new_image_size = sys.getsizeof(image_compressed)
    #
    #     print("[+] Size after compression:", get_size_format(new_image_size))
    #
    # # calculate the saving bytes
    # saving_diff = new_image_size - image_size
    # # print the saving percentage
    # print(f"[+] Image size change: {saving_diff / image_size * 100:.2f}% of the original image size.")
    # return image_compressed


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"
