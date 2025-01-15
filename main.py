import Transformer
import Utils


def main(directory_path):
    maindict = Transformer.encode_images(Utils.get_image_files(directory_path))
    for i in maindict:
        if maindict[i]['has_been_reviewed'] == False:
            duplicates, near_duplicates = Transformer.find_similar_images(i, maindict, 0.8)
            if len(duplicates) > 0:
                print("Original image: " + i)
                print(f"Duplicates: {duplicates}")
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
                print(f"Similar images: {near_duplicates}")
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
    print(maindict)
    for i in list(maindict.keys()):
        if maindict[i]['to_be_deleted']:
            Utils.delete_file(i)
            del maindict[i]

    return True


main('deneme')

                





