from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from pathlib import Path
from time import sleep
from PIL import Image
import requests
import random
import time
import io

def scroll_down():
    sleep(2)
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    sleep(2)

def download_image(url, name, download_path):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = Path(download_path, name)
        with open(file_path, "wb") as f:
            image.save(f, "JPEG")         
    except Exception as e:
        print(f"Can't save image {name}")
        print('FAILED: ', e)

def get_images_url():
    return browser.execute_script(
        'let images_url = []; \
        let board = document.getElementsByClassName("vbI XiG")[0] \
                            .getElementsByTagName("img"); \
        for (let i = 0; i < board.length; i++) \
            {images_url.push(board[i].getAttribute("src"));} \
        return images_url;')

time_start = time.time()
browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
url = 'https://www.pinterest.com/ngntrgduc/girl/'
browser.get(url)
browser.maximize_window()
sleep(random.random() * 1 + 1)

images_url_file = open("images_url.txt", "w")
run = True
file_name = 1
download_folder = Path('Downloaded')
if not download_folder.exists():
    download_folder.mkdir()

while run:
    images_url = get_images_url()
    images_url = [image.replace('/236x/', '/564x/') for image in images_url 
                  if len(image) == 71]
    for image in images_url:
        images_url_file.write(f'{image}\n')    
        download_image(image, f'{file_name}.jpg', download_folder)    
        file_name += 1
    scroll_down()    

    images_url_after_scroll = get_images_url()
    images_url_after_scroll = [image.replace('/236x/', '/564x/') 
                               for image in images_url_after_scroll
                               if len(image) == 71]
    if len(images_url_after_scroll) == 0:
        run = False
        continue

    for image in images_url_after_scroll:
        images_url_file.write(f'{image}\n')
        download_image(image, f'{file_name}.jpg', download_folder)
        file_name += 1
    scroll_down()

images_url_file.close()
print(f'Done, took {time.time() - time_start} seconds.')
browser.quit()
