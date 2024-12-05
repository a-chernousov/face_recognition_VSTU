"""
face_recognizer  Copyright (C) 2023  Your Name
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.

Contact Information:
- Email: your.email@example.com
- Paper Mail: Your Address, City, Country
"""

from deepface import DeepFace
import json


def face_recogn():
    try:
        img_path = "faceBPItest/img_3.png"
        db_path = "faceBPI"

        DeepFace.build_model("Facenet")

        result = DeepFace.find(img_path=img_path, db_path=db_path)
        return result
    except Exception as err:
        return err

def face_verify(img_1, img_2):
    try:
        result_dict = DeepFace.verify(img1_path=img_1, img2_path=img_2, model_name='Facenet512')

        with open('result.json', 'w') as file:
            json.dump(result_dict, file, indent=4, ensure_ascii=False)

        return result_dict
    except Exception as _ex:
        return _ex

def main():
    print(face_recogn())

if __name__ == "__main__":
    main()