from sentence_transformers import SentenceTransformer
import os

class MovieEmbedder:
    def __init__(self,model_name='all_MiniLM-L6-v2',save_path="./models/all-MiniLM-L6-v2"):
        self.save_path = save_path

        if os.path.exists(self.save_path):
            self.model = SentenceTransformer(self.save_path)
        else:
            self.model = SentenceTransformer(model_name)
            self.model.save(self.save_path)
    
    def encode(self,text):
        # Returns a standard python list for easy JSON serialization
        return self.model.encode(text).tolist()#converting the numpy array of vectors to a python list for saving it to database .
