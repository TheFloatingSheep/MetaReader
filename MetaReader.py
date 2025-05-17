import requests
from PIL import Image
from PIL.ExifTags import TAGS
import os

url = input("Veuillez entrer l'URL de votre image : ")
print(f"L'URL de l'image est : {url}")
name_image = input("Saisissez un nom d'image (par exemple image.jpg) : ")
print(f"Le nom de l'image est : {name_image}")

def download_image(url, name_image):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(name_image, 'wb') as f:
                f.write(response.content)
            print(f"Image téléchargée avec succès sous le nom : {name_image}")
        else:
            print(f"Échec du téléchargement. Code HTTP : {response.status_code}")
    except Exception as e:
        print(f"Une erreur est survenue lors du téléchargement : {e}")

def get_exif(name_image):
    try:
        if not os.path.exists(name_image):
            print("Le fichier image n'existe pas.")
            return
        
        absolute_path = os.path.abspath(name_image)
        print(f"Le chemin absolu de l'image est {absolute_path}")
        
        image = Image.open(name_image)

        exif_data = image._getexif() #get exif data

        if exif_data is not None:
            print("Données EXIF de l'image :")
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)  # Recupere le nom du tag EXIF
                print(f"{tag_name}: {value}")
        else:
            print("Aucune donnée EXIF trouvée.")
    except Exception as e:
        print(f'Une erreur est survenue lors de l\'extraction des données EXIF : {e}')

# Telecharge l'image et extrait les données EXIF
download_image(url, name_image)
get_exif(name_image)
