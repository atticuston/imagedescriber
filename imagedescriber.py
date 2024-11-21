#Copyright © 2024 Atticus

#This code is free to use, modify, and distribute by anyone. There are no restrictions on its usage, and you are welcome to do whatever you like with it. However, please acknowledge the original author, Atticus, when using or redistributing this code.

#No warranty is provided, and the author (me :D) is not liable for any damages that may arise from the use of this code, this is simply a project i did for fun.

import requests
import base64
import os
import re
import tkinter as tk
from tkinter import filedialog, Text
from PIL import Image
import io

def img_2_base(img_path, quality=25, max_size=(128, 128)): #feel free to change the max size however it will make it way longer if u upload crystal clear 4k images
    with Image.open(img_path) as img:
        if img.mode != 'RGB':
            img = img.convert('RGB')

        img.thumbnail(max_size)
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=quality) # I FUCKING DESPISE JPEG BUT IT'S EITHER THIS OR WEBP SO FUCK IT
        buffer.seek(0)

        #print(base64.b64encode(buffer.read()).decode("utf-8")) # debugging for best quality & image size
        return base64.b64encode(buffer.read()).decode("utf-8")


def filter_resp(raw_content):
    removecontent = r'"content":"(.*?)"'
    matchfilter = re.findall(removecontent, raw_content)
    cleanup = [word.strip().replace(' ', '') for word in matchfilter]
    filtered_shit = ' '.join(cleanup)
    return filtered_shit

class ImageChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Describer by atticus duh")
        self.img_path = None
        self.uhhh_gui()

    def uhhh_gui(self):
        self.select_btn = tk.Button(self.root, text="Select Image", command=self.tk_img_select)
        self.select_btn.pack(pady=10)
        self.img_path_l = tk.Label(self.root, text="No image selected. (choose something already)")
        self.img_path_l.pack()
        self.send_btn = tk.Button(self.root, text="Send (may take a while)", command=self.send_cq, state=tk.DISABLED)
        self.send_btn.pack(pady=10)
        self.resp_txt = Text(self.root, height=10, width=50, wrap="word")
        self.resp_txt.pack(pady=10)

    def tk_img_select(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image shiii", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )

        if file_path:
            self.img_path = file_path
            self.img_path_l.config(text=f"Selected Image: {os.path.basename(file_path)}")
            self.send_btn.config(state=tk.NORMAL)

    def send_cq(self):
        global countnum # doesn't actually work and i'm too lazy to fix it
        countnum=0 # doesn't actually work and i'm too lazy to fix it
        if not self.img_path:
            return

        user_msg = "Describe the image honestly SERIOUSLY DESCRIBE IT AS SHORT AS POSSIBLE (If possible try to guess who it is in the image)."
        img_base = img_2_base(self.img_path, quality=25)  #i tested 25 is the optimal for good results and fast respondes under 25 it just becomes a bunch of slashes and empty data (a sign of failure to compress the image)
        payload = {
            "model": "llava",
            "messages": [
                {"role": "system", "content": user_msg, "goal": "SERIOUSLY DESCRIBE IT AS SHORT AS POSSIBLE", "images": [img_base]}
            ],
            "options": {
                "temperature": 0.1,  # Eh tweak this only if your pc is strong asf or weak asf
                "max_tokens": 25,   # Eh tweak this only if your pc is strong asf or weak asf
                "top_p": 0.1,      # Eh tweak this only if your pc is strong asf or weak asf
                "frequency_penalty": 0, # removes weird delay
                "presence_penalty": 0, # removes weird delay
                "n": 1# Eh tweak this only if your pc is strong asf or weak asf
            }
        }
        api_url = "http://localhost:11434/api/chat"

        resp = requests.post(api_url, json=payload)
        out_path = os.path.join(os.getcwd(), "rawres.json")
        with open(out_path, "w") as file:
            file.write(resp.text)

        filtered_shit = filter_resp(resp.text)
        countnum=countnum+1
        self.show_filter_resp({countnum} )
        self.show_filter_resp(filtered_shit)

    def show_filter_resp(self, content):
        self.resp_txt.insert(tk.END, content)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageChatApp(root)
    root.mainloop()
#damn you gotta be either worried or bored asf or both to look all the way down here
