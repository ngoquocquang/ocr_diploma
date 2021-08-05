import timeit
st = timeit.default_timer()
import argparse
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
from detect_text import detect_text

# import timeit
# st=timeit.default_timer()

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir_images", required= True, help= "Đường dẫn tới thư mục cha chứa các thư mục có ảnh cần OCR")
parser.add_argument("-w", "--weights", type= str, required= False, help= "Loaị weight muốn sử dụng: transformer hoặc seq2seq", default= "transformer")
parser.add_argument("-o", "--output", required= False, help="Dường dẫn tới thư mục cha chứa thư mục đầu ra của các file text ocr", default=".")
options = vars(parser.parse_args())

if options["weights"]=="seq2seq":
    print("Load weight seq2seq.pth")
    config = Cfg.load_config_from_name('vgg_seq2seq')
    path_model = os.path.join(os.getcwd(), 'model', 'seq2seq.pth')
    # load pretrained weight
    config['weights'] = path_model
else:
    print("Load weight transformerocr.pth")
    config = Cfg.load_config_from_name('vgg_transformer')
    path_model = os.path.join(os.getcwd(), 'model', 'transformerocr.pth')
# load pretrained weight
    config['weights'] = path_model
# set device to use cpu

config['cnn']['pretrained'] = False
config['predictor']['beamsearch'] = False
config['device'] = 'cpu'

detector = Predictor(config)

path_input = options["dir_images"]
output = options["output"]
if not os.path.exists(output):
    raise Exception("Đường dẫn đầu ra không chính xác")
path_outputs = os.path.join(output, "output_ocr")
read_me = os.path.join(output, "READ_ME_OCR.txt")
readme = open(read_me, "w", encoding="utf8")
readme.write("Chạy trên python 3.7 và cài môi trường bằng cách pip install -r requirements.txt\n"
             "usage: ocr.py [-h] -d DIR_IMAGES [-w WEIGHTS] [-o OUTPUT]\n"
             "optional arguments:\n"
             "-h, --help\n"
             "show this help message and exit\n"
             "-d DIR_IMAGES, --dir_images DIR_IMAGES\n"
             "Đường dẫn tới thư mục cha chứa các thư mục có ảnh cần OCR\n"
             "-w WEIGHTS, --weights WEIGHTS\n"
             "Loaị weight muốn sử dụng: transformer hoặc seq2seq\n"
             "-o OUTPUT, --output OUTPUT\n"
             "Dường dẫn tới thư mục cha chứa thư mục đầu ra của các file text ocr\n"
             "Các trường dữ liệu sẽ được lưu theo tên ảnh nên có thể tùy chọn cách đặt tên\n"
             "Như trong dữ liệu test là:\n"
             "fullname(họ và tên)|dateofbirth(ngày,tháng,năm sinh)|placeofbirth(nơi sinh)|gender(giới tính)|"
             "ethnicgroup(dân tộc)|school(học sinh trường)|examterm(khóa thi)|examboard(hội đồng thi)|"
             "typeofgraduation(tốt nghiệp loại)|typeoftraining(hình thức đào tạo)|date(ngày và nơi cấp bằng)|"
             "serialno(số hiệu)|regno(số vào sổ cấp bằng)"
             )

if not os.path.exists(path_outputs):
    os.mkdir(path_outputs)

# f = open("output_predict.txt", "w", encoding="utf8")
# print(timeit.default_timer() - st)
# st1 = timeit.default_timer()
try:
    paths = os.listdir(path_input)
except:
    raise Exception("Đường dẫn đầu vào không chính xác")

for path in paths:
    st1 = timeit.default_timer()
    path_img = os.path.join(path_input, path)
    filenames = os.listdir(path_img)
    path_output = os.path.join(path_outputs, path + '.txt')
    f = open(path_output, "w", encoding="utf8")
    for filename in filenames:
        if not filename.lower().endswith(('.bmp', '.jpeg', '.jpg', '.png', '.tif', '.tiff')):
            continue
        image = os.path.join(path_img, filename)
        image = Image.open(image)
        # im = img.crop((5, 5, 20, 40))

        # use numpy to convert the pil_image into a numpy array
        img = np.array(image)
        # im = np.array(im)
        img = detect_text(img)


        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        # Nếu phân tách đen trắng

        # gray = cv2.threshold(gray, 0, 255,
        #   cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # Nếu làm mờ ảnh
        # gray = cv2.medianBlur(gray, 3)

        # gray = cv2.blur(gray,(5,5))

        # gray = cv2.GaussianBlur(gray,(5,5),0)

        # image filtering
        # kernel = np.ones((5,5),np.float32)/25
        # gray = cv2.filter2D(gray,-1,kernel)

        # gray = cv2.bilateralFilter(gray,9,75,75)

        img = gray
        img = Image.fromarray(img)
        # im=Image.fromarray(im)
        # plt.imshow(img)
        # predict
        result = detector.predict(img)
        filename = filename.split('.')[0]
        if result[0].isdigit() and result[1] == ' ':
            result = result[2:]
        # plt.imshow(img)
        if result.isdigit():
            im = image.crop((1, 1, 22, 33))
            im = np.array(im)
            im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
            im = Image.fromarray(im)
            # plt.imshow(im)
            result1 = detector.predict(im)
            if result1[0].isalpha():
                result1 = result1.upper()
                # print(result)
                # plt.imshow(img)
                #   plt.imshow(im)
                print(filename + ':' + result1[0] + ' ' + result + '|')
                f.write(filename + ':' + result1[0] + ' ' + result + '|')
            else:
                print(filename + ':' + result)
                f.write(filename + ':' + result + '|')
        else:
            print(filename + ':' + result)
            f.write(filename + ':' + result + '|')
        # plt.show()
    f.close()
    print('Time to OCR folder {} : {}'.format(path, timeit.default_timer()-st1))
print('Total time: ', timeit.default_timer() - st)
