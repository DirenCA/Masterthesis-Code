from exiftool import ExifToolHelper

#we will use this function to extract all the metadata from the picture(url) that is inserted into it
def extract_metadata (url):
    with ExifToolHelper() as et:
        for d in et.get_metadata(f"{url}"):
            for k, v in d.items():
                print(f"Dict: {k} = {v}")