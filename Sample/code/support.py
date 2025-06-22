from os import walk, path, getcwd
import pygame

def import_folder(folder_path):
    surface_list = []
    # print("Checking path:", folder_path)
    # print("Current working directory:", getcwd())
    # print("Absolute path being searched:", path.abspath(folder_path))
    
    # Check if path exists
    if not path.exists(folder_path):
        print("Path does not exist:", folder_path)
        return surface_list
    
    for root, dirs, img_files in walk(folder_path):
        # print("Found files:", img_files)
        for image in img_files:
            if image.endswith(('.png', '.jpg', '.jpeg')):  # Only load image files
                full_path = path.join(root, image)
                # print("Loading:", full_path)
                try:
                    img_surface = pygame.image.load(full_path).convert_alpha()
                    surface_list.append(img_surface)
                except pygame.error as e:
                    print("Error loading image:", full_path, e)
    return surface_list