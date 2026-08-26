from PIL import Image
import glob

files = glob.glob("visualizations/*.png")

for file in files:
    try:
        with Image.open(file) as img:
            print(f"{file} -> OK | Size: {img.size} | Format: {img.format}")
    except Exception as e:
        print(f"{file} -> INVALID | {e}")