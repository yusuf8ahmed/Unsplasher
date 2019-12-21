import subprocess, os, random, ctypes
import requests, shutil, uuid, csv
import urllib.request as urllib

#CreateFolder
def createFolder(directory = r'C:\Users\Yusuf\Pictures\Uploader'):
    try:
        if os.path.exists(directory) == False:
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

createFolder()
#Randomized stuff
list = ['city', 'toronto', 'sky', 'night', 'citynight', 'nature', 'animal', 'graffiti', 'top', "new-york", "tokyo", "downtown", "new"]
random.shuffle(list)
search = random.choice(list)
ppage = random.randint(1, 40)
pic_num = random.randint(1, ppage)
#Get image form unsplash
url2 = f"""https://api.unsplash.com/search/collections?query={search}&page=1&per_page={ppage}&client_id=20ffee15fdc5f17ed8490dbe62adc7489f94870fc3621abf3ec3a6af5c60cf01"""
r = requests.get(url2)
data = r.json()
#Global Uses
url = data["results"][pic_num]["cover_photo"]['urls']["full"]
mpath = r"C:\Users\Yusuf\Pictures\Uploader"
photo_id = str(uuid.uuid4())[:8] + ".png"
#getting image form url to project folder
response = requests.get(url, stream=True)
with open(photo_id, 'wb+') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response
#move to uploader
os.system(f"move {photo_id} {mpath}")
#Set to Background
ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{mpath}\{photo_id}", 0)
#csv