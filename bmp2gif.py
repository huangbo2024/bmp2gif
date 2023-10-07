from PIL import Image
import os

def bmp_to_gif(bmp_dir, output_gif):
    '''
    在我做项目时，一个小工作是把material studio导出的很多bmp图片连续拼接成gif，所以编写了此脚本自动拼接
    When I was working on the project, a small task was to continuously splice a lot of .bmp images exported by material studio into .gif, 
    so I wrote this script for automatic stitching.
    '''
  
    bmp_files = [f for f in os.listdir(bmp_dir) if f.endswith('.bmp') or f.endswith('.BMP')]

    bmp_files.sort()

    images = [Image.open(os.path.join(bmp_dir, f)) for f in bmp_files]

    images[0].save(output_gif, save_all=True, append_images=images[1:], loop=0, duration=200)

bmp_dir = 'your_path'  # 请将此路径替换为您的bmp文件的目录
output_gif = '3.gif'
bmp_to_gif(bmp_dir, output_gif)
