import streamlit as st
import time
import os
import json
import numpy as np
from numpy.linalg import norm
import ollama
from PyPDF2 import PdfReader

def parse_file(filename):
    reader = PdfReader(filename)
    paragraphs = []
    buffer = []
    for page in reader.pages:
        text = page.extract_text()
        for line in text.splitlines():
            line = line.strip()
            if line:
                buffer.append(line)
            elif len(buffer):
                paragraphs.append(" ".join(buffer))
                buffer = []
    if len(buffer):
        paragraphs.append(" ".join(buffer))
    return paragraphs

def save_embeddings(filename, embeddings):
    # create dir if it doesn't exist
    if not os.path.exists("embeddings"):
        os.makedirs("embeddings")
    # dump embeddings to json
    with open(f"embeddings/{filename}.json", "w") as f:
        json.dump(embeddings, f)


def load_embeddings(filename):
    # check if file exists
    if not os.path.exists(f"embeddings/{filename}.json"):
        return False
    # load embeddings from json
    with open(f"embeddings/{filename}.json", "r") as f:
        return json.load(f)

def get_embeddings(filename, modelname, chunks):
    # check if embeddings are already saved
    if (embeddings := load_embeddings(filename)) is not False:
        return embeddings
    # get embeddings from ollama
    embeddings = [
        ollama.embeddings(model=modelname, prompt=chunk)["embedding"]
        for chunk in chunks
    ]
    # save embeddings
    save_embeddings(filename, embeddings)
    return embeddings



def find_most_similar(needle, haystack):
    needle_norm = norm(needle)
    similarity_scores = [
        np.dot(needle, item) / (needle_norm * norm(item)) for item in haystack
    ]
    return sorted(zip(similarity_scores, range(len(haystack))), reverse=True)




def main():
    st.title("Reading Assistant")
    st.write("Ask me anything about the programming PDF!")

    filename = "programming.pdf"
    paragraphs = parse_file(filename)
    embeddings = get_embeddings(filename, "nomic-embed-text", paragraphs)

    prompt = st.text_area("Enter your question", height=100)

    if st.button("Get Answer"):
        prompt_embedding = ollama.embeddings(model="nomic-embed-text", prompt=prompt)["embedding"]
        most_similar_chunks = find_most_similar(prompt_embedding, embeddings)[:5]

        context = "\n".join(paragraphs[item[1]] for item in most_similar_chunks[:10])

        response = ollama.chat(
            model="llama3.2",                       #llama3-chatqa               
            messages=[
                {"role": "system", "content": "You are a helpful reading assistant who answers questions based on snippets of text provided in context. Answer only using the context provided, being short but not too short. If you're unsure, just say that you don't know, also if the context is not present just reply document doesn't contain neccesary information Context: " + context},
                {"role": "user", "content": prompt},
            ],
        )
        st.write("Answer:")
        st.write(response["message"]["content"])

if __name__ == "__main__":
    main()
