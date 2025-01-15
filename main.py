import Transformer
import Utils
from subprocess import call
from Utils import Utils
import argparse
import sys

def main(directory_path):
    # Get image files
    image_files = Utils.get_image_files(directory_path)
    if not image_files:
        print(f"No image files found in directory: {directory_path}")
        return
    
    # Process images
    maindict = Transformer.encode_images(image_files)
    for i in maindict:
        if maindict[i]['has_been_reviewed'] == False:
            duplicates, near_duplicates = Transformer.find_similar_images(i, maindict, 0.8)
            if len(duplicates) > 0:
                print("Original image: " + i)
                call(["viu", i])
                for k, duplicate in enumerate(duplicates):
                    print(f"Image {k}: {duplicate}")
                    call(["viu", duplicate])
                user_input = input("Which ones do you want to delete? For the original image, type -1. For others, start from 0 such as the first image is 0, second 1, etc. Enter numbers separated by commas [-1, 2, 3]: ")
                selected_indices = [int(x.strip()) for x in user_input.split(',')]
                print(f"selected indices: {selected_indices}")
                for j in selected_indices:
                    print(type(j))
                if -1 in selected_indices:
                    maindict[i]['to_be_deleted'] = True
                    maindict[i]['has_been_reviewed'] = True
                    for j in selected_indices:
                        maindict[duplicates[j]]['has_been_reviewed'] = True
                else:
                    for j in selected_indices:
                        maindict[duplicates[j]]['to_be_deleted'] = True
                        maindict[duplicates[j]]['has_been_reviewed'] = True
                    for j in duplicates:
                        maindict[j]['has_been_reviewed'] = True
            if len(near_duplicates) > 0:
                print("Original image: " + i)
                call(["viu", i])
                for k, near_duplicate in enumerate(near_duplicates):
                    print(f"Image {k}: {near_duplicates}")
                    call(["viu", near_duplicate])
                user_input = input("Which ones do you want to delete? For the original image, type -1. For others, start from 0 such as the first image is 0, second 1, etc. Enter numbers separated by commas [-1, 2, 3]: ")
                selected_indices = [int(x.strip()) for x in user_input.split(',')]
                if -1 in selected_indices:
                    maindict[i]['to_be_deleted'] = True
                    maindict[i]['has_been_reviewed'] = True
                    for j in selected_indices:
                        maindict[near_duplicates[j]]['has_been_reviewed'] = True
                else:
                    for j in selected_indices:
                        maindict[near_duplicates[j]]['to_be_deleted'] = True
                        maindict[near_duplicates[j]]['has_been_reviewed'] = True
                    for j in near_duplicates:
                        maindict[j]['has_been_reviewed'] = True
    deleted_files = set()
    for i in list(maindict.keys()):
        if maindict[i]['to_be_deleted']:
            deleted_files.add(i)
            Utils.delete_file(i)
            del maindict[i]
    print(f"Deleted: {deleted_files}\n")
    print(f"Kept: {list(maindict.keys())}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find and remove duplicate/similar images in a directory.')
    parser.add_argument('directory', type=str, help='Path to the directory containing images')
    
    args = parser.parse_args()
    
    try:
        main(args.directory)
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

                





