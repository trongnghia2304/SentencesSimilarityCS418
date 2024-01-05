from sentence_transformers import SentenceTransformer, util
import os
import re

def split_sentences(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return sentences

def calculate_similarity_score(model, input_sentence, sentences_to_compare):
    input_embedding = model.encode(input_sentence, convert_to_tensor=True)
    similarity_scores = []
    for sentence in sentences_to_compare:
        sentence_embedding = model.encode(sentence, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(input_embedding, sentence_embedding)
        similarity_scores.append(similarity.item())
    return similarity_scores

def find_similar_sentences_in_files(input_text, directory_path, similarity_threshold=0.8):
    if not os.path.isdir(directory_path):
        print(f"The directory '{directory_path}' does not exist.")
        return

    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

    with open(input_text, 'r', encoding='utf-8') as file:
        input_text_content = file.read()
    input_sentences = split_sentences(input_text_content)

    similar_files = []

    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                file_text_content = file.read()
            sentences_to_compare = split_sentences(file_text_content)
            
            for input_sentence in input_sentences:
                similarity_scores = calculate_similarity_score(model, input_sentence, sentences_to_compare)
                max_similarity = max(similarity_scores)
                if max_similarity > similarity_threshold:
                    similar_files.append((filename, input_sentence.strip(), sentences_to_compare[similarity_scores.index(max_similarity)].strip(), max_similarity))

    return similar_files

# Replace 'input_text.txt' with the path to your uploaded input text file
input_text_file = './data/data/C001.txt'

# Replace 'folder_path' with the path to the uploaded directory containing your .txt files
folder_path = './data/data/folder1/'

similar_sentences = find_similar_sentences_in_files(input_text_file, folder_path)

if similar_sentences:
    print("Files with similar sentences:")
    for file, input_sentence, similar_sentence, similarity_score in similar_sentences:
        print(f"File: {file}")
        print(f"Input Sentence: {input_sentence}")
        print(f"Similar Sentence: {similar_sentence}")
        print(f"Similarity Score: {similarity_score}")
        print("------")
else:
    print("No similar sentences found.")