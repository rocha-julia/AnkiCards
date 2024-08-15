import os
import csv
import tqdm

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC

from translate import Translator

def write_csv(card_frontside, card_backside, csv_file):

    if not os.path.isfile('./'+csv_file):
        with open(csv_file, 'w', newline='', encoding='UTF-8') as file:
            writer = csv.writer(file)
        
            writer.writerow([card_frontside, card_backside])
    else:
        # Write new cards into csv
        with open(csv_file, 'a', newline='',encoding='UTF-8') as file:
            writer = csv.writer(file)
            
            writer.writerow([card_frontside, card_backside])

# Assimil path
ASSIMIL_PATH    = 'C:/Users/Rocha/Documents/AssimilAlemao/'

lessons_list = input('Please, provide the lesson numbers separated by a comma >> ').split(',')

print('Generating cards...')
for lesson in tqdm.tqdm(lessons_list):

    # Transform lessons numbers into folder name
    lesson = 'L'+(3-len(lesson))*'0'+lesson+'-German ASSIMIL'

    # Grab folder path
    folder_path = ASSIMIL_PATH+lesson

    # List files in the folder
    list_of_files = os.listdir(folder_path)

    # Set translator
    translator = Translator(from_lang='de', to_lang='en')

    # Translate sentences and add them to csv file
    for file in list_of_files:
        if file[:3]!='T00':
            audiofile =  MP3(folder_path+'/'+file, ID3=EasyID3)
            phrase = audiofile.get('title', ['Unknown'])[0].split('-')[-1]
            translation = translator.translate(phrase)
            write_csv(translation, phrase, 'anki_cards_de.csv')

print('Process finished: Csv file is now up to date!')