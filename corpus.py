import pickle
import os

def create_corpus(raw: list, save_to: str):
    """Create corpus and save it"""
    try:
        file = '{}.pickle'.format(save_to)
        print(file)
        if os.path.isfile(file):
            corpus = reconstruct_corpus(file)
            corpus += raw

        else:
            corpus = raw

        corpus = list(set(corpus))

        with open(file=file, mode='bw') as f:
            pickle.dump(corpus, f)

        return True
    except Exception as e:
        print(e)
        return False

def reconstruct_corpus(file: str):
    """Reconstruct corpus as list type with pickle file"""
    try:
        with open(file, mode='br') as f:
            corpus = pickle.load(f)
        
        return corpus

    except Exception as e:
        print(e)
        return False