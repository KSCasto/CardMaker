from PIL import Image  # install by > python3 -m pip install --upgrade Pillow  # ref. https://pillow.readthedocs.io/en/latest/installation.html#basic-installation
import zipfile, os, time, logging
from dotenv import load_dotenv
import multiprocessing as mp
from functools import partial

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


def process_image(f, inputPath, dpi):
    if f == ".gitkeep":
        return None
    #This is for when we download an image that doesn't need the edges cropped
    if "no-crop" in f:
        return Image.open(f"{inputPath}/{f}").resize((int(dpi*2.5), int(dpi*3.5)))
    elif "passport" in f.lower():
        return Image.open(f"{inputPath}/{f}").resize((int(dpi*2), int(dpi*2)))
    #This is the regular way
    else:
        img = Image.open(f"{inputPath}/{f}").resize((int(dpi*2.72), int(dpi*3.7)))
        return img.crop((int(dpi*0.11), int(dpi*0.1), int(dpi*2.61), int(dpi*3.6)))

def prepareImages(inputPath, dpi):
    imageNames = os.listdir(inputPath)
    
    # Create a multiprocessing pool
    with mp.Pool() as pool:
        # Use partial to fix inputPath and dpi arguments
        # Map process_image function to all image names in parallel
        images = pool.map(partial(process_image, inputPath=inputPath, dpi=dpi), imageNames)
    
    # Filter out None results (from .gitkeep files)
    return [img for img in images if img is not None]

def preparePDF(dpi,offset,images):
    i=0
    pages=[]
    while (len(images)!=0):
        rowGutter = int(dpi/4)
        colGutter = int(dpi/8)
        colWidth = int(dpi*2.5)
        rowHeight = int(dpi*3.5)
        newImage = Image.new('RGB', (int(dpi*8.5),int(dpi*11)), color="#fff") #8.5x11 paper with a white background
        for rowNum in range(0,3):
            for colNum in range(0,3):
                try:
                    cardImage=images.pop()
                    #Place the image offset by the row/col number and gutters to that point
                    #If thick paper is used, the gutter from the bottom will be used for the top instead
                    #Printing on thick paper normally often cuts off the top, so this is the workaround
                    newImage.paste(cardImage,(rowGutter*(colNum+1)+colWidth*(colNum),offset+colGutter*(rowNum+1)+rowHeight*(rowNum)))
                except:
                    pass
        pages.append(newImage)
        # newImage.save(f'new{i}.png')
        i+=1
    return pages

def makePDF(deckName,inputPath,outputPath):
    offset = 75
    dpi = 300
    startTime = time.time()
    images = prepareImages(inputPath,dpi)
    logging.info(f"Images prepared in {(time.time()-startTime) * 1000:.2f} milliseconds")
    startTime = time.time()
    pdf = preparePDF(dpi,offset,images)
    logging.info(f"PDF prepared in {(time.time()-startTime) * 1000:.2f} milliseconds")

    pdf_path = outputPath+'/'+deckName+".pdf"
    print(pdf_path)
        
    pdf[0].save(
        pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=pdf[1:]
    )
    return pdf_path

def cleanup_files(target_file_path):
    try:
        for filename in os.listdir(target_file_path):
            file_path = os.path.join(target_file_path, filename)
            if os.path.isfile(file_path) and filename != ".gitkeep":
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        print("All files deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def remove_zip(zip_file_path):
    try:
        os.remove(zip_file_path)
        print(f"File '{zip_file_path}' successfully deleted.")
    except FileNotFoundError:
        print(f"File '{zip_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def unzip_archive(zip_file_path, extract_to_path):
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_path)
        print(f"Successfully unzipped {zip_file_path} to {extract_to_path}")
    except Exception as e:
        print(f"Error unzipping the archive: {e}")
