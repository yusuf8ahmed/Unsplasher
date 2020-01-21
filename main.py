import subprocess, os, random, ctypes, schedule
import requests, shutil, uuid, csv, time
import urllib.request as urllib
from datetime import datetime, timedelta

# env\Scripts\activate.bat

FOLDER_PATH = os.path.join(os.path.expanduser('~/Pictures'), 'Uploader')
CSV_PATH = os.path.join(os.path.expanduser('~/Pictures'), 'Uploader')  + "\logs.csv"

#CreateFolder
def createFolder():
    try:
        if not os.path.exists(FOLDER_PATH):
            os.makedirs(FOLDER_PATH)
    except Exception as err:
        print(f'{err} in Error: Creating directory. {FOLDER_PATH}')

def createcsv():
    try:
        if not os.path.exists(FOLDER_PATH+ "\logs.csv"):
            open(FOLDER_PATH + "\logs.csv", 'a+') 
    except Exception as err:
        print(f'{err} in Error: Creating CSV file. {FOLDER_PATH}')

createFolder()
createcsv()

def Change_Background():
    try:
        from func import Change_Background, check_internet 
    except ImportError:
        

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
        photo_id = str(uuid.uuid4())[:8] + ".png"

        #Getting image from url()
        response = requests.get(url, stream=True)
        with open(photo_id, 'wb+') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        #move to uploader
        os.system(f"move {photo_id} {FOLDER_PATH}")

        #Set to Background
        #Change for Fucntion
        #ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{FOLDER_PATH}\{photo_id}", 0)

        #csv
        csv_path = mpath + "\logs.csv"
        with open( csv_path, 'a', newline='') as file:
            w = csv.writer(file)
            w.writerow([photo_id, search, ppage, pic_num, url2, url])

    except Exception as err:
        #csv
        with open( CSV_PATH , 'w', newline='') as file:
            w = csv.writer(file)
            w.writerow([err])
            
    print(f"{str(datetime.now())[11:19]}==>{str(datetime.now() + timedelta(seconds=60))[11:19]}")

print(f"{str(datetime.now())[11:19]}==>{str(datetime.now() + timedelta(seconds=60))[11:19]}")
schedule.every(1).minutes.do(Change_Background)
while True:
    schedule.run_pending()
    time.sleep(1)
