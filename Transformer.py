from sentence_transformers import SentenceTransformer, util
from PIL import Image
import logging
import time

def encode_images(image_paths, batch_size=128):
    """
    Encode a list of images using CLIP model and return a dictionary of encodings with metadata.
    
    Args:
        image_paths (list): List of paths to image files
        batch_size (int): Batch size for encoding (default: 128)
    
    Returns:
        dict: Dictionary mapping image paths to their encodings and metadata:
            {
                path: {
                    'encoding': tensor,
                    'has_been_reviewed': bool
                }
            }
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger(__name__)

    # Load the OpenAI CLIP Model
    start_time = time.time()
    logger.info('Starting CLIP Model loading...')
    model = SentenceTransformer('clip-ViT-B-32')
    logger.info(f'CLIP Model loaded in {time.time() - start_time:.2f} seconds')

    # Load and encode images
    logger.info('Starting image loading and encoding...')
    batch_start = time.time()
    
    # Create list of PIL images
    images = [Image.open(filepath) for filepath in image_paths]
    
    # Encode images
    encodings = model.encode(
        images, 
        batch_size=batch_size, 
        convert_to_tensor=True, 
        show_progress_bar=True
    )
    
    logger.info(f'Image encoding completed in {time.time() - batch_start:.2f} seconds')
    logger.info(f'Average time per image: {(time.time() - batch_start) / len(image_paths):.2f} seconds')

    # Create dictionary mapping file paths to encodings and metadata
    encoded_images = {
        path: {
            'encoding': encoding,
            'has_been_reviewed': False,
            'to_be_deleted': False
        } for path, encoding in zip(image_paths, encodings)
    }
    
    return encoded_images

def find_similar_images(reference_image_path, encoded_images, similarity_threshold=0.8):
    """
    Find images similar to a reference image from a dictionary of encoded images.
    
    Args:
        reference_image_path (str): Path to the reference image to compare against
        encoded_images (dict): Dictionary of image paths and their encodings with metadata
        similarity_threshold (float): Minimum similarity score (0-1) for images to be considered similar
        
    Returns:
        tuple: Lists of (duplicates, near_duplicates) where:
            - duplicates: List of paths for images with similarity score = 1
            - near_duplicates: List of paths for images with similarity score >= threshold but < 1
    """
    logger = logging.getLogger(__name__)
    
    if reference_image_path not in encoded_images:
        raise ValueError(f"Reference image {reference_image_path} not found in encoded images")
    
    if not 0 <= similarity_threshold <= 1:
        raise ValueError("Similarity threshold must be between 0 and 1")
    
    reference_encoding = encoded_images[reference_image_path]['encoding']
    
    # Calculate similarity scores between reference image and all other images
    similarities = []
    for path, data in encoded_images.items():
        if path != reference_image_path:  # Skip comparing with itself
            score = util.pytorch_cos_sim(reference_encoding, data['encoding']).item()
            if score >= similarity_threshold:  # Only keep scores above threshold
                similarities.append((score, path))
    
    # Sort by similarity score in descending order
    similarities.sort(reverse=True)
    
    # Split into duplicates (score = 1) and near-duplicates (threshold <= score < 1)
    duplicates = [path for score, path in similarities if score >= 0.9999]  # Using 0.9999 for floating point comparison
    near_duplicates = [path for score, path in similarities if similarity_threshold <= score < 0.9999]
    
    return duplicates, near_duplicates
