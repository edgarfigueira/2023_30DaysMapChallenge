import shutil
import os


def create_folders_with_files(base_path, num_folders):
    for i in range(1, num_folders + 1):
        folder_name = str(i).zfill(len(str(num_folders)))  # Ensure leading zeros for sorting
        folder_path = os.path.join(base_path, folder_name)

        # Check if folder already exists and remove it if it does
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

        os.makedirs(folder_path)  # Create the main folder

        # Create sub-folders
        subfolders = ['data', 'results', 'processing']
        for subfolder in subfolders:
            subfolder_path = os.path.join(folder_path, subfolder)
            os.makedirs(subfolder_path)

        # Create sources.txt
        sources_path = os.path.join(folder_path, "sources.txt")
        with open(sources_path, "w") as sources_file:
            sources_file.write("This is the sources file.")

        # Create readme.txt
        readme_path = os.path.join(folder_path, "readme.txt")
        with open(readme_path, "w") as readme_file:
            readme_file.write("This is the readme file.")


base_path = "C:\\Users\\Edgar\\Desktop\\30daysMapChallenge"  # Replace with your desired parent folder path
num_folders = 10  # Change this to the number of folders you want to create

create_folders_with_files(base_path, num_folders)



