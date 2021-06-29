import os

class ImageTool(object):
    @staticmethod
    def get_img_list(path):
        return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
