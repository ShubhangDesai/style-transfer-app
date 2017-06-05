# utils.py

from modules import Camera
from modules import StyleCNN

from PIL import Image
from StringIO import StringIO
import torchvision.transforms as transforms
from torch.autograd import Variable
import scipy.misc

loader = transforms.Compose([
    transforms.Scale(256),
    transforms.CenterCrop(256),
    transforms.ToTensor()])

unloader = transforms.ToPILImage()

style_cnn = StyleCNN()
styles = ["styles/starry_night.jpg", "styles/great_wave.jpg", "styles/candy.jpg", "styles/udnie.jpg"]

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def image_loader(image):
    image = Variable(loader(image))
    image = image.unsqueeze(0)
    return image

def unload_image(image):
    image = image.data.clone().cpu()
    image = image.view(3, 256, 256)
    return unloader(image)

def get_pil_pic(camera):
    pic = camera.get_pic()
    return Image.fromarray(pic)

def generate_styles():
    pic = get_pil_pic(Camera())
    content_img = image_loader(pic)

    for i, style in enumerate(styles):
        style_img = image_loader(Image.open(style))
        pastiche = style_cnn.eval(content_img, style_img)
        result = unload_image(pastiche)
        scipy.misc.imsave("app/static/img/style" + str(i+1) + ".png", result)
