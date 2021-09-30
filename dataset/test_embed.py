import json
import time
import nltk
import scavenger.embeddings as em

# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKCYAN = '\033[96m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'

# train_strings = [
#   'Here is a list of',
#   'Here are some examples',
# ]
# test_true_strings = [
#   'For example',
#   'Here are some different',
#   'Examples include',
#   "Here are some examples of",
#   "I have a list of",
#   "These are some different ways to",
#   "There are many, such as",
#   "These are my favorite news articles",
#   "The following are the best restaurants in",
#   "Top 10 places to visit",
#   "Some of the best singers of 2020",
#   "I like all kinds of dinosaurs, including",
#   "The greatest bands in the world",
#   "Top spots for taking pictures",
#   "You may encounter any of the following",
#   "All of these methods can be considered",
# ]
# test_false_strings = [
#   "Hello, I am Ethan",
#   "Hello, I am Jun",
#   "This is a news article",
#   "Dinosaurs are a diverse group of reptiles of the clade Dinosauria",
#   "She doesn’t study German on Monday",
#   "Does she live in Paris",
#   "He doesn’t teach math",
#   "Cats hate water",
#   "Every child likes an ice cream",
#   "My brother takes out the trash",
#   "The course starts next Sunday",
#   "She swims every morning",
#   "I don’t wash the dishes",
#   "We see them every week",
#   "I don’t like tea",
#   "When does the train usually leave",
#   "She always forgets her purse",
#   "You don’t have children",
#   "I and my sister don’t see each other anymore",
#   "They don’t go to school tomorrow",
#   "He loves to play basketball",
#   "He goes to school",
#   "The Earth is spherical",
#   "Julie talks very",
#   "My brother’s dog barks a",
#   "Does he play",
#   "The train leaves every morning at 18",
#   "Water freezes at",
#   "I love my new",
#   "We drink coffee every",
#   "My Dad never works on the",
#   "She doesn’t teach",
#   "I do love my new",
#   "Mary brushes her teeth twice a",
#   "He drives to",
#   "Mary enjoys",
#   "She likes",
#   "My mother never",
#   "You don’t listen to",
#   "I run four miles every",
#   "They speak English at",
#   "The train does not leave at 12",
#   "I have no money at the",
#   "Do they talk a",
#   "Tomorrow early morning first I go to morning",
#   "Does she drink",
#   "You run to the",
#   "You have some schoolwork to",
#   "She doesn’t use a",
#   "It snows a lot in winter in",
#   "We live in",
#   "You go to holiday every",
#   "Do you like",
#   "My daughter does the",
# ]
# test_strings = test_true_strings + test_false_strings

# query_vec = get_mean_embedding(train_strings)

# distances = []
# tstart = time.time()
# for c in test_strings:
#   candidate_vec = get_embedding(c)
#   dist = get_cosine_distance(query_vec, candidate_vec)
#   distances.append(dist)
# time_per_embedding = (time.time() - tstart) / len(test_strings)
# print(f"Embeddings took an average of {time_per_embedding}s ({len(test_strings)} samples)")

# print("Query sentences:")
# for d in train_strings:
#   print(bcolors.OKBLUE + d + bcolors.ENDC)
# print("")
# print("Candidate sentences, sorted by cosine distance: (Blue are true examples)")
# for dist, text in sorted(zip(distances, test_strings)):
#   if text in test_true_strings:
#     print(bcolors.OKBLUE + f"{dist:.4f}: {text}" + bcolors.ENDC)
#   else:
#     print(f"{dist:.4f}: {text}")





# train_strings = [
#   'Here is a list of',
#   'Here are some examples',
# ]

# nltk.download('punkt')
# # filepath = "/home/jun/repos/few-shot-pretraining/embeddings/ExamplesStrings/true/c4/49994.txt"
# # filepath = "/home/jun/repos/few-shot-pretraining/output_10k/pile/869.txt"
# filepath = "/home/jun/repos/few-shot-pretraining/output_full/pile/33232.txt"
# with open(filepath, "r") as f:
#     # p = "Good morning Dr. Adams. The patient is waiting for you in room number 3."
#     # text = f.read()
#     obj = json.load(f)
#     text = obj["text"]
#     lines = text.split("\n")
#     sentences = []
#     for line in lines:
#         if len(line) < 5:
#             continue
#         sentences += nltk.tokenize.sent_tokenize(line)
#     em.show_sorted_distances(train_strings, sentences)





import scavenger.criterion as cri
from scavenger.document import Document

criterion = cri.ExamplesEmbedMinimalCriterion()

filepath = "/home/jun/repos/few-shot-pretraining/output_full/pile/33232.txt"
with open(filepath, "r") as f:
    # p = "Good morning Dr. Adams. The patient is waiting for you in room number 3."
    # text = f.read()
    obj = json.load(f)
    # doc = Document(text=obj["text"])
    doc = Document(text="Here is a list of")
report = criterion.check(doc)
print(report)