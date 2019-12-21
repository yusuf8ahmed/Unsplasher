import subprocess, os, random, ctypes
import requests, shutil, uuid, csv
import urllib.request as urllib

#CreateFolder
def createFolder(directory = r'C:\Users\Yusuf\Pictures\Uploader'):
    try:
        if os.path.exists(directory) == False:
            os.makedirs(directory)
    except Exception as err:
        print(f'{err} in Error: Creating directory. {directory}')

def createcsv(directory = r'C:\Users\Yusuf\Pictures\Uploader'):
    try:
        if os.path.exists(directory + "\logs.csv") == False:
            open(directory + "\logs.csv", 'a+') 
    except Exception as err:
        print(f'{err} in Error: Creating directory. {directory}')

createFolder()
createcsv()

try:
    #Randomized stuff
    name = ['city', 'toronto', 'sky', 'night', 'citynight', 'nature', 'animal', 'graffiti', "new-york", "tokyo", "downtown", "mountain", "safari"]
    random.shuffle(name)
    search = random.choice(name)
    ppage = random.randint(1, 40)
    pic_num = random.randint(1, ppage)

    #Get image form unsplash
    url2 = f"""https://api.unsplash.com/search/collections?query={search}&page=1&per_page={ppage}&client_id=20ffee15fdc5f17ed8490dbe62adc7489f94870fc3621abf3ec3a6af5c60cf01"""
    r = requests.get(url2)
    data = r.json()

    #variables
    url = data["results"][pic_num]["cover_photo"]['urls']["full"]
    mpath = r"C:\Users\Yusuf\Pictures\Uploader"
    photo_id = str(uuid.uuid4())[:8] + ".png"

    #Getting image from url()
    response = requests.get(url, stream=True)
    with open(photo_id, 'wb+') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

    #move to uploader
    os.system(f"move {photo_id} {mpath}")

    #Set to Background
    ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{mpath}\{photo_id}", 0)

    #csv
    csv_path = mpath + "\logs.csv"
    with open( csv_path, 'a', newline='') as file:
        w = csv.writer(file)
        w.writerow([photo_id, search, ppage, pic_num, url2, url])
except Exception as err:
    #csv
    mpath = r"C:\Users\Yusuf\Pictures\Uploader"
    csv_path = mpath + "\logs.csv"
    with open( csv_path , 'w', newline='') as file:
        w = csv.writer(file)
        w.writerow([err])
