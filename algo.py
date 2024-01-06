from sentence_transformers import SentenceTransformer, util
from transformers import AutoModel
import os
import re

precalculated_embeddings = {}

def split_sentences(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return sentences

def calculate_similarity_scores(model, input_sentences, sentences_to_compare):
    global precalculated_embeddings
    
    input_sentences_tuple = tuple(input_sentences)
    
    if input_sentences_tuple in precalculated_embeddings:
        input_embeddings = precalculated_embeddings[input_sentences_tuple]
    else:
        input_embeddings = model.encode(input_sentences, convert_to_tensor=True)
        precalculated_embeddings[input_sentences_tuple] = input_embeddings
    
    sentence_embeddings = model.encode(sentences_to_compare, convert_to_tensor=True)
    similarity_scores = util.pytorch_cos_sim(input_embeddings, sentence_embeddings)
    
    return similarity_scores

def find_similar_sentences_in_files(list_input, list_compare, sentences_input, sentences_compare, similarity_threshold=0.8):
    model = SentenceTransformer('sentence-transformers_paraphrase-multilingual-mpnet-base-v2')

    similar_files = []
    for i in range(len(list_compare)):
        similarity_scores = calculate_similarity_scores(model, sentences_input, sentences_compare[i])
        max_similarities = similarity_scores.max(dim=1)

        for idx, max_similarity in enumerate(max_similarities.values):
            if max_similarity > similarity_threshold:
                similar_files.append((
                    idx,
                    i,
                    max_similarities.indices[idx]
                ))

    return similar_files

# def find_similar_sentences_in_files(input_text, directory_path, similarity_threshold=0.8):
#     if not os.path.isdir(directory_path):
#         print(f"The directory '{directory_path}' does not exist.")
#         return

#     model = SentenceTransformer('sentence-transformers_paraphrase-multilingual-mpnet-base-v2')

#     with open(input_text, 'r', encoding='utf-8') as file:
#         input_text_content = file.read()
#     input_sentences = split_sentences(input_text_content)

#     similar_files = []
#     file_idx = -1
#     for filename in os.listdir(directory_path):
#         file_idx = file_idx + 1
#         if filename.endswith('.txt'):
#             file_path = os.path.join(directory_path, filename)
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 file_text_content = file.read()
#             sentences_to_compare = split_sentences(file_text_content)

#             similarity_scores = calculate_similarity_scores(model, input_sentences, sentences_to_compare)
#             print(input_sentences)
#             print(sentences_to_compare)
#             max_similarities = similarity_scores.max(dim=1)

#             for idx, max_similarity in enumerate(max_similarities.values):
#                 if max_similarity > similarity_threshold:
#                     similar_files.append((
#                         idx,
#                         file_idx,
#                         max_similarities.indices[idx]

#                         # filename,
                        
#                         # input_sentences[idx].strip(),
#                         # sentences_to_compare[max_similarities.indices[idx]].strip(),
#                         # max_similarity.item()
#                     ))

#     return similar_files

def main(): 
    # Replace 'input_text.txt' with the path to your uploaded input text file
    input_text_file = './bbc.txt'

# Replace 'folder_path' with the path to the uploaded directory containing your .txt files
    folder_path = './data/data/folder1/'

    similar_sentences = find_similar_sentences_in_files(input_text_file, folder_path)

    if similar_sentences:
        print("Files with similar sentences:")
        for input_idx,file_idx,sentence_idx in similar_sentences:
            print(f"input_idx: {input_idx}")
            print(f"file_idx: {file_idx}")
            print(f"sentence_idx: {sentence_idx}")
    else:
        print("No similar sentences found.")

if __name__ == '__main__':
    main()