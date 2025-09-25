#!/usr/bin/env python3
"""
Downloads real animal photos from web sources
"""

import requests
import os
from urllib.parse import urlparse
import mysql.connector

# Database connection parameters
config = {
    'host': 'vvfv20el7sb2enn3.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
    'user': 'gqxyxhxouyc8p0rp',
    'password': 'dlksjydtftbge4in',
    'database': 'ish64y4wkai1mdp7',
    'port': 3306
}

# Real animal photo URLs - from free sources or public domain
ANIMAL_PHOTOS = {
    # Reassigned photos to match animal descriptions better
    1: "https://th.bing.com/th/id/OIP.3YD8o-iQeSyNlAO-eS6pigHaE8?w=243&h=180&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3",  # Golden Retriever - Buddy
    2: "https://th.bing.com/th/id/OIP.Nnr1ADKFhDAfLw9SSvcW6AHaFF?w=273&h=187&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3",  # Siamese cat - Luna
    3: "https://th.bing.com/th/id/OIP.4FiMlTM6QS-w2eXg3Y1BAAHaEj?w=300&h=185&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3",  # German Shepherd - Max
    4: "https://th.bing.com/th/id/OIP.5_Hv1mq1uwfIMnAoiJlZGAHaE8?w=214&h=180&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3",  # Persian cat - Whiskers
    5: "https://th.bing.com/th/id/OIP.S_bJSleu8xwsEHZcMzLcMgHaFj?w=257&h=187&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3",  # Labrador Mix - Bella
    8: "https://images.unsplash.com/photo-1574158622682-e40e69881006?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",  # Tabby cat - Mittens
    12: "https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", # White Rabbit - Snowball
    13: "https://th.bing.com/th/id/OIP.txMGTq6DltF-eDaevXBjsgHaE8?w=286&h=191&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3", # Border Collie - Ranger
    16: "https://static.vecteezy.com/system/resources/previews/025/015/156/non_2x/a-cute-and-beautiful-orange-tabby-cat-with-curious-eyes-sits-on-the-floor-lovely-portrait-of-the-domestic-pet-isolated-on-white-background-adorable-feline-animal-image-by-ai-generated-photo.jpg", # Orange Tabby - Ginger
    20: "https://th.bing.com/th/id/OIP.onxW-rgMy1xj2LbNzajrSwHaE6?w=239&h=180&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3",  # Russian Blue - Smokey
    22: "https://th.bing.com/th/id/OIP.xp3vHXGhlDWVPhU5cLpnAgHaHa?w=151&h=180&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3",  # Tuxedo cat - Oreo
    6: "https://th.bing.com/th/id/OIP.nLJPUnCXkq40Y62L0xSFjgHaE8?w=370&h=202&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3",  # Black Shorthair - Shadow
    8: "https://th.bing.com/th/id/OIP.CnPGt4uD9g_olJzo5tY6CgHaIp?w=158&h=185&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3",  # Tabby cat - Mittens
    17: "https://th.bing.com/th/id/OIP.LcSUiEvCsTakFISIozP5RgHaFj?w=245&h=184&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3",  # Newfoundland dog - Bear
    11: "https://th.bing.com/th/id/OIP.cXsYFjx2q8SFLc4gZluM1AHaE6?w=232&h=180&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3",  # Beagle dog - Charlie
    21: "https://th.bing.com/th/id/OIP.DlPBawZANMAXMpVW4AUM9wHaFL?w=222&h=180&c=7&r=0&o=5&dpr=1.5&pid=1.7",  # Cocker Spaniel - Daisy
    15: "https://th.bing.com/th/id/OIP.pPYCDkESLvuibJ1l-9NjuQHaEK?w=252&h=180&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3",  # Rottweiler - Duke
    7: "https://th.bing.com/th/id/OIP.I3zbW6yrvcyJqo51FiLNjQHaHG?w=178&h=180&c=7&r=0&o=5&dpr=1.5&pid=1.7",  # Bulldog - Rocky
    25: "https://th.bing.com/th/id/OIP.Uypu4O8LGpqZY4caAo76qwHaGR?w=265&h=220&c=7&r=0&o=5&dpr=1.5&pid=1.7",  # Irish Setter - Rusty
    19: "https://th.bing.com/th/id/OIP.2jO32ymZJ68FvcgJ7UIIsQHaF0?w=230&h=180&c=7&r=0&o=5&dpr=1.5&pid=1.7",  # Australian Shepherd - Scout
    23: "https://th.bing.com/th/id/OIP.TOzJkfH5HNv_a725UK2udAHaE0?w=308&h=200&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3",  # Husky - Thor
    9: "https://th.bing.com/th/id/OIP.xHqZj-aF91JMymKcKjCWIwHaHa?w=193&h=193&c=7&r=0&o=5&dpr=1.5&pid=1.7",  # Great Dane - Zeus
    18: "https://th.bing.com/th/id/OIP.xIQhDPOOje3GDpMLP8nXgQHaE7?w=289&h=192&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3",  # American Guinea Pig - Coco
    24: "https://th.bing.com/th/id/OIP.7HnoxPjK4FULyzoMMGV6WAHaE8?w=248&h=180&c=7&r=0&o=5&dpr=1.5&pid=1.7",  # Lionhead rabbit - Honey
}

def download_image(url, filename):
    """Download an image from URL and save it"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Save the image
        with open(filename, 'wb') as f:
            f.write(response.content)

        print(f"[SUCCESS] Downloaded: {filename}")
        return True

    except Exception as e:
        print(f"[FAILED] Failed to download {url}: {str(e)}")
        return False

def get_animal_info():
    """Get animal information from database"""
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        cursor.execute("SELECT animal_id, name, species, breed FROM animals ORDER BY animal_id")
        animals = cursor.fetchall()

        animal_dict = {}
        for animal in animals:
            animal_id, name, species, breed = animal
            animal_dict[animal_id] = {
                'name': name,
                'species': species,
                'breed': breed,
                'filename': f"app/static/assets/animals/{animal_id:02d}_{name.lower().replace(' ', '_')}.jpg"
            }

        return animal_dict

    except Exception as e:
        print(f"Database error: {e}")
        return {}

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def main():
    print("Downloading Real Animal Photos")
    print("=" * 50)

    # Get animal information
    animals = get_animal_info()
    if not animals:
        print("Could not connect to database")
        return

    downloaded_count = 0

    # Download photos we have URLs for
    for animal_id, photo_url in ANIMAL_PHOTOS.items():
        if animal_id in animals:
            animal = animals[animal_id]
            filename = animal['filename']

            print(f"\nDownloading photo for {animal['name']} ({animal['breed']})...")

            if download_image(photo_url, filename):
                downloaded_count += 1
            else:
                print(f"Keeping placeholder image for {animal['name']}")

    print(f"\nSuccessfully downloaded {downloaded_count} real animal photos!")
    print(f"\nAnimals with real photos:")

    for animal_id in ANIMAL_PHOTOS.keys():
        if animal_id in animals:
            animal = animals[animal_id]
            print(f"  - {animal['name']} ({animal['species']}, {animal['breed']})")

    print(f"\nRemaining animals still use placeholder images:")
    for animal_id, animal in animals.items():
        if animal_id not in ANIMAL_PHOTOS:
            print(f"  - {animal['name']} ({animal['species']}, {animal['breed']})")

    print(f"\nYour website: http://localhost:5000")
    print(f"To add more real photos, find image URLs and add them to ANIMAL_PHOTOS in this script")

if __name__ == "__main__":
    main()