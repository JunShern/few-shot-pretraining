import numpy as np
import requests
import zipfile
from pathlib import Path
from scipy import spatial
from spacy.language import Language
from tqdm import tqdm

WORD_VEC_DATA_SRC = "https://dl.fbaipublicfiles.com/fasttext/vectors-english/crawl-300d-2M.vec.zip"
CACHE_DIR = "./cache"
NLP_CACHE = "./cache/nlp/"

if Path(NLP_CACHE).exists():
    print("Loading model from cache", NLP_CACHE)
    nlp = Language()
    nlp.from_disk(NLP_CACHE)
else:
    word_vec_data_cache = Path(CACHE_DIR) / Path(WORD_VEC_DATA_SRC).stem
    word_vec_data_cache.parent.mkdir(parents=True, exist_ok=True)
    word_vec_data_zipped = Path("/tmp/") / Path(WORD_VEC_DATA_SRC).name
    word_vec_data_zipped.parent.mkdir(parents=True, exist_ok=True)
    # Download if not cached
    if not word_vec_data_cache.exists():
        print(f"{word_vec_data_cache} does not exist.\nDownloading from {WORD_VEC_DATA_SRC}")
        r = requests.get(WORD_VEC_DATA_SRC, stream=True)
        with open(word_vec_data_zipped, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in tqdm(r.iter_content(chunk_size=1024), total=(total_length/1024) + 1): 
                if chunk:
                    f.write(chunk)
                    f.flush()
        # Unzip
        with zipfile.ZipFile(word_vec_data_zipped, 'r') as zip_ref:
            zip_ref.extractall(word_vec_data_cache.parent)
    else:
        print(f"Using cached word vectors at {word_vec_data_cache}")

    # Use Spacy to load Vectors
    nlp = Language()
    print('[*] Loading Vectors with Spacy...')
    with open(word_vec_data_cache, "rb") as f:
        header = f.readline()
        nr_row, nr_dim = header.split()
        nlp.vocab.reset_vectors(width=int(nr_dim))
        for line in tqdm(f, total=2000000):
            line = line.rstrip().decode("utf8")
            pieces = line.rsplit(" ", int(nr_dim))
            word = pieces[0]
            vector = np.asarray([float(v) for v in pieces[1:]], dtype="f")
            nlp.vocab.set_vector(word, vector)
    Path(NLP_CACHE).mkdir(parents=True, exist_ok=True)
    nlp.to_disk(NLP_CACHE)

def get_embedding(string: str) -> np.array:
    vec = nlp(string).vector
    return vec / np.linalg.norm(vec)

def get_mean_embedding(strings: "list[str]") -> np.array:
    # Embed each dataset example into a vector
    embedding_vecs = []
    for s in strings:
        embedding_vecs.append(get_embedding(s))
    embedding_vecs = np.array(embedding_vecs)
    # print('Dataset Embedding Matrix Shape:', dataset_vecs.shape)
    avg_vec = embedding_vecs.mean(0)
    norm_avg_vec = avg_vec / np.linalg.norm(avg_vec)
    # print('Unit-Normalized Average Embedding for Dataset Examples:', norm_avg_vec)
    return norm_avg_vec

def get_cosine_distance(vec1, vec2):
    return spatial.distance.cosine(vec1, vec2)

def show_sorted_distances(train_strings, candidate_strings, test_true_strings=[]):
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    query_vec = get_mean_embedding(train_strings)
    test_strings = test_true_strings + candidate_strings
    distances = []
    # tstart = time.time()
    for c in test_strings:
        candidate_vec = get_embedding(c)
        dist = get_cosine_distance(query_vec, candidate_vec)
        distances.append(dist)
    # time_per_embedding = (time.time() - tstart) / len(test_strings)
    # print(f"Embeddings took an average of {time_per_embedding}s ({len(test_strings)} samples)")
    print("Query sentences:")
    for d in train_strings:
        print(bcolors.OKBLUE + d + bcolors.ENDC)
    print("")
    print("Candidate sentences, sorted by cosine distance: (Blue are true examples)")
    for dist, text in sorted(zip(distances, test_strings)):
        if text in test_true_strings:
            print(bcolors.OKBLUE + f"{dist:.4f}: {text}" + bcolors.ENDC)
        else:
            print(f"{dist:.4f}: {text}")
