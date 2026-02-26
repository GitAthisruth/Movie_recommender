from sentence_transformers import SentenceTransformer
import os
from src.logger import get_logger

logger = get_logger(__name__)

class MovieEmbedder:
    def __init__(self, model_name='all-MiniLM-L6-v2', save_path="./models/all-MiniLM-L6-v2"):
        logger.info("Initializing MovieEmbedder")

        self.save_path = save_path
        self.model_name = model_name

        try:
            # Check if saved model exists
            if os.path.exists(self.save_path):
                logger.info(f"Loading existing model from: {self.save_path}")
                self.model = SentenceTransformer(self.save_path)
                logger.info("Model loaded successfully from local path")
            else:
                logger.info(f"Local model not found. Downloading model: {model_name}")
                self.model = SentenceTransformer(model_name)

                # Create directory if not exists
                os.makedirs(os.path.dirname(self.save_path), exist_ok=True)

                logger.info(f"Saving model to: {self.save_path}")
                self.model.save(self.save_path)
                logger.info("Model downloaded and saved successfully")

        except Exception as e:
            logger.exception("Error during model initialization")
            raise
    
    def encode(self, text):
        try:
            # Only log when batch input
            if isinstance(text, list):
                logger.info(f"Encoding batch of {len(text)} texts")

            embeddings = self.model.encode(text)

            return embeddings.tolist()

        except Exception:
            logger.exception("Error during text encoding")
            raise