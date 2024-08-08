import pygame, os, re

BASE_IMG_PATH = 'assets/images/'

def load_image(path):
    try:
        img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
        return img
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        return None

def load_images(path):
    def numerical_sort(value):
        parts = re.split(r'(\d+)', value)
        return [int(part) if part.isdigit() else part for part in parts]

    image_paths = sorted(os.listdir(BASE_IMG_PATH + path), key=numerical_sort)
    images = [load_image(os.path.join(path, img_name)) for img_name in image_paths if img_name.endswith(('.png', '.jpg'))]
    return images

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
    
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            if self.frame < (self.img_duration * len(self.images) - 1):
                self.frame += 1
            else:
                self.done = True
    
    def img(self):
        return self.images[self.frame // self.img_duration]
