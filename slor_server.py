import json
import pysolr
import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Entry
import urllib.request
import io
import numpy as np
import faiss

#import email library
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
class FeatureExtract_VGG16:
    def __init__(self):

        self.vgg16 = VGG16(weights='imagenet', include_top=False,pooling='avg',input_shape=(224,224,3))
    
    # function to extract features from images
    def extractFeat(self,fileName):
        img = image.load_img(fileName, target_size=(224, 224))
        img_array = image.img_to_array(img)
        # expand_dims for image
        img_array = np.expand_dims(img_array, axis=0)
        # preprocess the image
        img_array = preprocess_input(img_array)

        # extract features of the image using vgg16
        feat = self.vgg16.predict(img_array)
        # L2归一化
        feat = feat[0] / np.linalg.norm(feat[0])

        return feat
feature_extract_vgg16 = FeatureExtract_VGG16()
'''
Send an email with an embedded image and a plain text message for

'''
def sendEmail():
    global email_query

    email_address = email_query.get()
    msg = MIMEMultipart()

# Add the sender, recipient, subject, and body to the message
    msg['From'] = 'huahaoshang2000@gmail.com'
    msg['To'] = email_address
    msg['Subject'] = 'Your Image From NASA!'
    body = 'Here is your image from NASA!'
    msg.attach(MIMEText(body, 'plain'))

# Open the image file, read its contents, and add it as an attachment to the message
    if image_click == 0:
        with open('image1.jpeg', 'rb') as f:
            img_data = f.read()
            print(type(img_data))
    
    elif image_click == 1:
        img_data = load_image_from_url(similar_imgs[0][0]['link'][0])
        img_data = img_data.resize((300, 300), Image.LANCZOS)
        with io.BytesIO() as buffer:
            img_data.save(buffer, format='JPEG')
            img_data = buffer.getvalue()

    elif image_click == 2:
        img_data = load_image_from_url(similar_imgs[1][0]['link'][0])
        img_data = img_data.resize((300, 300), Image.LANCZOS)
        with io.BytesIO() as buffer:
            img_data.save(buffer, format='JPEG')
            img_data = buffer.getvalue()

    elif image_click == 3:
        img_data = load_image_from_url(similar_imgs[2][0]['link'][0])
        img_data = img_data.resize((300, 300), Image.LANCZOS)
        with io.BytesIO() as buffer:
            img_data.save(buffer, format='JPEG')
            img_data = buffer.getvalue()
    
    image = MIMEImage(img_data, name='image.jpg')

    msg.attach(image)

# Create a connection to the SMTP server and send the message
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('huahaoshang2000@gmail.com', 'waqwcwwpnifluskz')
    text = msg.as_string()
    # server.sendmail('huahaoshang2000@gmail.com', 'huahaoshang2000@outlook.com', text)
    server.sendmail('huahaoshang2000@gmail.com', email_address, text)
    server.quit()    
# Create a Solr connectio
solr = pysolr.Solr('http://localhost:8983/solr/NasaImageData', timeout=100)

# Load the data from the JSON file
def uploadFile(solr):
    json_directory = './JsonData'

# Iterate through all files in the directory
    for filename in os.listdir(json_directory):
        if filename.endswith('.json'):
        # Construct the full file path
            print(filename)
            file_path = os.path.join(json_directory, filename)
            print(file_path)
        with open(file_path, 'r') as f:
            data = json.load(f)

            # Upload the data to the Solr core
            solr.add(data)
            solr.commit()

def searchbyTitle(title):
    results = solr.search(q='title:'+title, 
        **{
        'rows': 100
        })
    results_list = []
    for result in results:
        item_dict = {}
        title = result['title']
        description = result['description']
        date_created = result['date_created']
        media_type = result['media_type']
        nasa_id = result['nasa_id']
        item_dict['title'] = title
        item_dict['description'] = description
        item_dict['date_created'] = date_created
        item_dict['media_type'] = media_type
        item_dict['nasa_id'] = nasa_id
        item_dict['link'] = result['link']
        results_list.append(item_dict)
    return results_list


def load_image_from_url_search(url):
    with urllib.request.urlopen(url) as response:
        image_data = response.read()
    with open('image1.jpeg', 'wb') as f:
        f.write(image_data)
    
    image = Image.open('image1.jpeg')
    return image

def load_image_from_url(url):
    with urllib.request.urlopen(url) as response:
        image_data = response.read()
    # with open('image.jpg', 'wb') as f:
    #     f.write(image_data)
    image_file = io.BytesIO(image_data)
    image = Image.open(image_file)
    return image

def on_button_click():
    global img_num, label_img, results, photo,img,search_image_title

    img_num += 1
    if img_num >= len(results):
        img_num = 0  # Reset to the first image if no more images are available

    img = load_image_from_url_search(results[img_num]['link'][0])
    img = img.resize((300, 300), Image.LANCZOS)
    image_bytes = img.tobytes()
    with open('image.jpg', 'wb') as f:
        f.write(image_bytes)
    photo = ImageTk.PhotoImage(img)

    label_click = tk.Label(text=results[img_num]['description'])
    long_description = results[img_num]['description'][0]
    words = long_description.split()
    label.delete('1.0', 'end')
    for i, word in enumerate(words):
        label.insert('end', word + ' ')
        if (i+1) % 20 == 0:
            label.insert('end', '\n')
    
    label_img.place(x=0, y=100)
    label_img.config(image=photo)
    label_img.image = photo

    search_image_title.config(text=results[img_num]['title'][0])
    

def on_similar_button_click():
    global photo, img, similar_imgs, label_img1, label_img2, label_img3
    global similar_img_title1, similar_img_title2, similar_img_title3
    index_vgg = faiss.read_index('/Users/shanghuahao/Desktop/RiceU/COMP631/Project1/image_feature/voc_vgg.index')
    name_list_vgg = np.load('/Users/shanghuahao/Desktop/RiceU/COMP631/Project1/image_feature/name_list_vgg.npy')
    # bytes_io = io.BytesIO()
    # img.save(bytes_io, format='JPEG')
    # bytes_data = bytes_io.getvalue()
    feat_vec = feature_extract_vgg16.extractFeat('/Users/shanghuahao/Desktop/RiceU/COMP631/image1.jpeg')
    #expand the dimension of the feature vector
    feat_vec = np.expand_dims(feat_vec, axis=0)

    k = 4
    D, I = index_vgg.search(feat_vec, k)

    select_file_list = name_list_vgg[I[0]]
    image_titles = []
    for i,file_name in enumerate(select_file_list):
        if i == 0:
            continue
        image_titles.append(file_name)
    # 组装文件名
    similar_img_title1 = image_titles[0].replace('_',' ')
    similar_img_title2 = image_titles[1].replace('_',' ')
    similar_img_title3 = image_titles[2].replace('_',' ')

    print(similar_img_title1,'  ', similar_img_title2,'  ', similar_img_title3)
    result_1 = searchbyTitle(similar_img_title1)
    result_2 = searchbyTitle(similar_img_title2)
    result_3 = searchbyTitle(similar_img_title3)

    similar_imgs = [result_1, result_2, result_3]

    #create 3 images display on the window
    img1 = load_image_from_url(result_1[0]['link'][0])
    img1 = img1.resize((300, 300), Image.LANCZOS)
    photo1 = ImageTk.PhotoImage(img1)
    label_img1 = tk.Label(image=photo1)
    label_img1.place(x=0, y=500)
    label_img1.bind("<Button-1>", on_image1_click)
    label_img1.config(image=photo1)
    label_img1.image = photo1

    similar_img_title_1.config(text=result_1[0]['title'][0])



    img2 = load_image_from_url(result_2[0]['link'][0])
    img2 = img2.resize((300, 300), Image.LANCZOS)
    photo2 = ImageTk.PhotoImage(img2)
    label_img2 = tk.Label(image=photo2)
    label_img2.place(x=400, y=500)
    label_img2.bind("<Button-1>", on_image2_click)
    label_img2.config(image=photo2)
    label_img2.image = photo2

    similar_img_title_2.config(text=result_2[0]['title'][0])

    img3 = load_image_from_url(result_3[0]['link'][0])
    img3 = img3.resize((300, 300), Image.LANCZOS)
    photo3 = ImageTk.PhotoImage(img3)
    label_img3 = tk.Label(image=photo3)
    label_img3.place(x=800, y=500)
    label_img3.bind("<Button-1>", on_image3_click)
    label_img3.config(image=photo3)
    label_img3.image = photo3

    similar_img_title_3.config(text=result_3[0]['title'][0])
    



def search_button_click():
    global results, title_query

    title_query = search_query.get()
    results = searchbyTitle(title_query)
    on_button_click()

def on_image_click(event):
    global image_click, click_label
    print("Search clicked")
    image_click = 0
    click_label.config(text="Search Image Selected")

    long_description = results[img_num]['description'][0]
    words = long_description.split()
    label.delete('1.0', 'end')
    for i, word in enumerate(words):
        label.insert('end', word + ' ')
        if (i+1) % 20 == 0:
            label.insert('end', '\n')

def on_image1_click(event):
    global image_click, click_label, similar_img_title1, similar_img_title2, similar_img_title3
    print("Image 1 clicked")
    image_click = 1
    click_label.config(text="Similar Image 1 Selected")

    image1_search = searchbyTitle(similar_img_title1)
    long_description = image1_search[0]['description'][0]
    words = long_description.split()
    label.delete('1.0', 'end')
    for i, word in enumerate(words):
        label.insert('end', word + ' ')
        if (i+1) % 20 == 0:
            label.insert('end', '\n')

def on_image2_click(event):
    global image_click, click_label
    print("Image 2 clicked")
    image_click = 2
    click_label.config(text="Similar Image 2 Selected")

    image2_search = searchbyTitle(similar_img_title2)
    long_description = image2_search[0]['description'][0]
    words = long_description.split()
    label.delete('1.0', 'end')
    for i, word in enumerate(words):
        label.insert('end', word + ' ')
        if (i+1) % 20 == 0:
            label.insert('end', '\n')
    
def on_image3_click(event):
    global image_click, click_label
    print("Image 3 clicked")
    image_click = 3
    click_label.config(text="Similar Image 3 Selected")

    image3_search = searchbyTitle(similar_img_title3)
    long_description = image3_search[0]['description'][0]
    words = long_description.split()
    label.delete('1.0', 'end')
    for i, word in enumerate(words):
        label.insert('end', word + ' ')
        if (i+1) % 20 == 0:
            label.insert('end', '\n')

def main():
    global img_num, label_img,title_label, results, search_query, label, email_query, photo,img
    
    global click_label

    global similar_imgs, image_click, label_img1, label_img2, label_img3, click_label, search_image_title 
    global similar_img_title_1, similar_img_title_2, similar_img_title_3, similar_img_title1, similar_img_title2, similar_img_title3

    # uploadFile(solr)
    
    title_query = 'galaxy'
    results = searchbyTitle(title_query)
    
    img_num = 0
    init_image_path = '/Users/shanghuahao/Desktop/RiceU/COMP631/Project1/UI_image/Nasa.jpeg'
    img = Image.open(init_image_path)
    img = img.resize((300, 300), Image.LANCZOS)
    # sendEmail()
    img_num1 = 1
    img1 = load_image_from_url(results[img_num1]['link'][0])
    
    root = tk.Tk()
    root.geometry("1200x1000")
    root.title("NASA Image Search")
    root.configure(background='white')


    #search bar###########
    search_query = tk.StringVar()
    entry = Entry(root, textvariable=search_query)
    entry.place(x=10, y=50)
    entry.configure(background='white')

    search_button = tk.Button(root, text="Search", command=search_button_click)
    search_button.place(x=200, y=50)
    
    button = tk.Button(root, text="Next Image", command=on_button_click)
    button.place(x=300, y=50)

    title_label = tk.Label(root, text="Start Searching!")
    title_label.place(x=10, y=10)

    button_similar = tk.Button(root, text="Similar Images", command=on_similar_button_click)
    button_similar.place(x=10, y=430)

    listbox = tk.Listbox(root, height=20, width=15)
    listbox.place(x=330, y=100)
    items = ["Search Examples:","Earth","Cluster","Galaxy","Jupyter","Mars","SpaceX","Rocket","Apollo","Nubela","Supernova"]
    for item in items:
        listbox.insert(tk.END, item)
    #####################


    #Email section########
    email_label = tk.Label(root, text="Your Email")
    email_label.place(x=500, y=10)
    email_query = tk.StringVar()
    email_entry = Entry(root, textvariable=email_query)
    email_entry.place(x=500, y=50)
    email_entry.configure(background='white')
    email_button = tk.Button(root, text="Send Email", command=sendEmail)
    email_button.place(x=700, y=50)
    ######################

    label = tk.Text(root, height=20, width=80)
    label.place(x=500, y=100)
    
    #Main Search Image######
    photo = ImageTk.PhotoImage(img)
    label_img = tk.Label(root, image=photo)
    label_img.place(x=0, y=100)
    label_img.bind("<Button-1>", on_image_click)
    # label_img.pack()

    # photo1 = ImageTk.PhotoImage(img1)
    # label_img1 = tk.Label(root, image=photo1)
    # #change the image position
    # label_img1.place(x=1000, y=100)
    # label_img1.pack()

    click_label = tk.Label(root, text="No Image Selected")
    click_label.place(x=200, y=10) 

    search_image_title = tk.Label(root, text="NASA Image")
    search_image_title.place(x=0, y=80)
    
    click_label = tk.Label(root, text="No Image Selected")
    click_label.place(x=200, y=10)
    
    similar_img_title_1 = tk.Label(root, text="")
    similar_img_title_1.place(x=0, y=480)

    similar_img_title_2 = tk.Label(root, text="")
    similar_img_title_2.place(x=400, y=480)

    similar_img_title_3 = tk.Label(root, text="")
    similar_img_title_3.place(x=800, y=480)

    root.mainloop()

if __name__ == "__main__":
    main()