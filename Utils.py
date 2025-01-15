import os
from pathlib import Path

class Utils:
    def delete_file(file_path):
        """
        Delete a file from the filesystem.
        
        Args:
            file_path (str): Path to the file to delete
        """
        try:
            os.remove(file_path)
        except OSError as e:
            print(f"Error deleting file {file_path}: {e}")


    def get_image_files(directory_path):
        """
        Recursively find all image files in a directory and its subdirectories.
        
        Args:
            directory_path (str): Path to the directory to search
            
        Returns:
            list: List of paths to image files
        """
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
        image_files = []
        
        # Convert directory path to Path object for better cross-platform compatibility
        directory = Path(directory_path)
        
        # Walk through all files and directories
        for root, _, files in os.walk(directory):
            for file in files:
                # Check if file has an image extension
                if file.lower().endswith(image_extensions):
                    # Get full path and append to list
                    full_path = Path(root) / file
                    image_files.append(str(full_path))
        
        return image_files