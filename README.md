# Finding Similar Images using a Neural Network

A Python tool that identifies and helps you delete duplicate and similar images, using OpenAI's CLIP (Contrastive Language-Image Pre-Training) neural network. It uses the model to generate image embeddings and compares them using cosine similarity.

## Demo

https://github.com/user-attachments/assets/622d0702-8f6a-483f-9c83-a5b30ab218c5

## Description

This tool helps you:

- Find exact duplicates and visually similar images in a directory
- Preview images using terminal-based image viewer (viu)
- Interactively choose which images to keep or delete
- Support common image formats (jpg, jpeg, png, gif, bmp, tiff, webp)

The similarity detection is powered by OpenAI's CLIP model (ViT-B-32) through the sentence-transformers library, providing visual similarity matching beyond just pixel-perfect duplicates.

## Key Features

- **Smart Similarity Detection**: Uses CLIP (ViT-B-32) model to detect both exact duplicates (similarity score ≥ 0.9999) and visually similar images (customizable threshold)
- **Interactive Review Process**:
  - Visual preview of each image group using terminal-based 'viu' viewer
  - User-friendly selection interface for choosing which images to keep/delete
- **Robust File Handling**:
  - Recursive directory scanning
  - Support for multiple image formats (jpg, jpeg, png, gif, bmp, tiff, webp)
  - Cross-platform compatibility using Path objects

## Limitations

- Needs sufficient memory to load the CLIP model and process image batches
- Initial CLIP model loading time may be significant
- Terminal-based image preview has limited resolution

## Installation

You have to have [CLIP](https://github.com/openai/CLIP), [sentence-transformers](https://pypi.org/project/sentence-transformers/), [PyTorch](https://pytorch.org/), and [viu](https://github.com/atanunq/viu) installed to get this working. BEFORE STARTING THIS INSTALLATION, go ahead to their respective pages and install them.

1. Clone the repository:

   ```bash
   git clone https://github.com/erenmenges/image-dedup-with-CLIP.git
   cd image-dedup-with-CLIP
   ```

2. Install required Python packages:

   ```bash
   pip install sentence-transformers Pillow
   ```

3. If you haven't, install the 'viu' terminal image viewer:
   - On Ubuntu/Debian:

     ```bash
     sudo apt install viu
     ```

   - On macOS:

     ```bash
     brew install viu
     ```

   - Other systems: Visit [viu repository](https://github.com/atanunq/viu)

## Usage

1. Basic Usage:

   ```bash
   python main.py /path/to/image/directory
   ```

2. Interactive Process:
   - The tool will scan the directory and process images in batches
   - For each group of similar images:
     - Original image is displayed first
     - Followed by potential duplicates
     - Enter numbers to select images to delete:
       - `-1` to delete the original image
       - `0,1,2` to delete specific duplicates (comma-separated)

3. Review Results:
   - Program shows list of deleted files
   - Shows list of kept files
   - Automatically skips previously reviewed images

Note: The default similarity threshold is 0.8 (80%). Images with similarity score ≥ 0.9999 are considered exact duplicates.
