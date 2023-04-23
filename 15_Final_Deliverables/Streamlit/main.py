import streamlit as st
import requests
from PIL import Image
import pickle
import numpy as np
import string as st
from collections import defaultdict

try:

    with open("final_stopwords.txt", "r", encoding="UTF-8") as f:
        stopWords = [i.strip() for i in f]

    # loading all data

    paras_e = open('english.txt',
                   encoding="UTF8").read().split("\n")
    paras_h = open('hindi.txt',
                   encoding="UTF8").read().split("\n")
    paras_g = open('gujarati.txt',
                   encoding="UTF8").read().split("\n")
    paras_p = open('punjabi.txt',
                   encoding="UTF8").read().split("\n")
    paras_t = open('tamil.txt',
                   encoding="UTF8").read().split("\n")
    paras_b = open('bengali.txt',
                   encoding="UTF8").read().split("\n")

    suffixes = {
        1: ["ो", "े", "ू", "ु", "ी", "ि", "ा"],
        2: ["कर", "ाओ", "िए", "ाई", "ाए", "ने", "नी", "ना", "ते", "ीं", "ती", "ता", "ाँ", "ां", "ों", "ें"],
        3: ["ाकर", "ाइए", "ाईं", "ाया", "ेगी", "ेगा", "ोगी", "ोगे", "ाने", "ाना", "ाते", "ाती", "ाता", "तीं", "ाओं", "ाएं", "ुओं", "ुएं", "ुआं"],
        4: ["ाएगी", "ाएगा", "ाओगी", "ाओगे", "एंगी", "ेंगी", "एंगे", "ेंगे", "ूंगी", "ूंगा", "ातीं", "नाओं", "नाएं", "ताओं", "ताएं", "ियाँ", "ियों", "ियां"],
        5: ["ाएंगी", "ाएंगे", "ाऊंगी", "ाऊंगा", "ाइयाँ", "ाइयों", "ाइयां"],
    }

    def stemming_hindi(text):
        for L in 5, 4, 3, 2, 1:
            if len(text) > L + 1:
                for suf in suffixes[L]:
                    if text.endswith(suf):
                        return text[:-L]
        return text

    def preprocess_text(string, stopWords):
        # Define a set of punctuation marks to remove
        punctuations = set(st.punctuation) | set(["०", "S", "―", "=", "॥", "”", "|", "“", "'", "।",
                                                  ";", ",", ":", "!", '"', "?", "[", "]", "......", ":-", ".", ":-", "{", "(", "}", ")"])

        # Remove punctuations and split the string into tokens
        tokens = string.translate(str.maketrans(
            "", "", "".join(punctuations))).split()

        # Apply stemming and remove stop words from the tokens
        tokens = [stemming_hindi(word)
                  for word in tokens if word not in stopWords]

        return tokens

    pos_lis = {}
    for idx, para in enumerate(paras_h):
        words = preprocess_text(para, stopWords)

        for word in words:
            if word in pos_lis.keys():
                if idx in pos_lis[word].keys():
                    pos_lis[word][idx] += 1
                else:
                    pos_lis[word][idx] = 1
            else:
                temp = {idx: 1}
                pos_lis[word] = temp.copy()

    # model BM25

    def bm25(query, paragraphs, pos_lisl, stop_words, l, b=0.75, k=2):
        q_tokens = preprocess_text(query, stop_words)
        lengths = [len(p.split()) for p in paragraphs]
        N = len(paragraphs)
        avg_len = sum(lengths) / N

        idf = {}
        for word in np.unique(q_tokens):
            if word in pos_lisl:
                df = len(pos_lisl[word])
            else:
                df = 0
            idf[word] = np.log((N - df + 0.5) / (df + 0.5))

        score = defaultdict(float)
        for idx, para in enumerate(paragraphs):
            para_tokens = para.split()
            for word in q_tokens:
                tf = para_tokens.count(word)
                if word in pos_lisl and idx in pos_lisl[word]:
                    tf = pos_lisl[word][idx]
                score[idx] += idf[word] * \
                    (tf * (k + 1)) / \
                    (k * (1 - b + b * lengths[idx] / avg_len) + tf)

        return sorted(score, key=score.get, reverse=True)[:l]

    from googletrans import Translator

    def get_translation(data, dest):
        translator = Translator()
        text = translator.translate(data, dest).text
        return text
    # search Function

    def search(query, pos_lis, lang, l=5):
        # print(query)
        # print(pos_lis)
        query = get_translation(query, "hi")
        # print(query)
        # print(query)
        tokens = preprocess_text(query, stopWords)

        query = " ".join(tokens)

        indxs = bm25(query, pos_lis, l)
        # print(indxs)
        if lang == 'e':
            return [f'{paras_e[idx]}' for idx in indxs], indxs
        elif lang == 'g':
            return [f'{paras_g[idx]}' for idx in indxs], indxs

        elif lang == 'h':
            return [f'{paras_h[idx]}' for idx in indxs], indxs
        elif lang == 'b':
            return [f'{paras_b[idx]}' for idx in indxs], indxs
        elif lang == 't':
            return [f'{paras_t[idx]}' for idx in indxs], indxs
        elif lang == 'p':
            return [f'{paras_p[idx]}' for idx in indxs], indxs

    # def print_shloka(shloka):
    #     n = len(shloka.split())
    #     shloka = shloka.split()
    #     idx1 = n//4
    #     idx2 = n//2
    #     idx3 = (3*n)//4

    #     print(" ".join(shloka[:idx1]))
    #     print(" ".join(shloka[idx1:idx2]))
    #     print(" ".join(shloka[idx2:idx3]))
    #     print(" ".join(shloka[idx3:]))

    # query = "praise shame evil lust"
    # result = search(query, pos_lis, "e")

    # print("The top 5 relevant documents for the query \" ",
    #       query, " \" in the asked language are : ")
    # for i in range(5):
    #     print("\nshloka ", i+1, " (index = ", result[1][i], " ) =>  \n")

    #     print_shloka(result[0][i])

    menu = ["Home", "English", "Hindi", "Gujarati", "Punjabi", "Bengali"]

    choice = st.sidebar.radio("Query Language Selection", menu)

    var1, var2, var3 = st.columns(3)
    with var1:
        st.write(' ')
    with var2:
        st.image("download.png")
    with var3:
        st.write(' ')

    if choice == "Home":
        with st.form(key='searchform'):
            search_term = st.text_input("Enter your search query:")
            submit_button = st.form_submit_button("Search")
        if submit_button:
            genre_dict = {"English": "e", "Hindi": "h", "Gujarati": "g",
                          "Bengali": "b", "Punjabi": "p", "Tamil": "t"}
            genre = st.radio("What's your preferred output language preference of retrieved documents?",
                             ("English", "Hindi", "Gujarati", "Bengali", "Punjabi", "Tamil"))

            out = search(search_term, pos_lis, genre_dict[genre])

            for i, doc in enumerate(len(out)):
                st.write(
                    '...........................................................')
                st.write(f"Document {i+1}:")
                st.write(doc)
                st.write(
                    '...........................................................')

    elif choice == "English":

        st.subheader("Please enter your query in English")
        with st.form(key='searchform'):
            search_term = st.text_input("Enter your search query:")
            submit_button = st.form_submit_button("Search")
        if submit_button:
            genre_dict = {"English": "e", "Hindi": "h", "Gujarati": "g",
                          "Bengali": "b", "Punjabi": "p", "Tamil": "t"}
            genre = st.radio("What's your preferred output language preference of retrieved documents?",
                             ("English", "Hindi", "Gujarati", "Bengali", "Punjabi", "Tamil"))

            out = search(search_term, pos_lis, genre_dict[genre])

            for i, doc in enumerate(len(out)):
                st.write(
                    '...........................................................')
                st.write(f"Document {i+1}:")
                st.write(doc)
                st.write(
                    '...........................................................')
    elif choice == "Bengali":

        st.subheader("Please enter your query in Bengali")
        with st.form(key='searchform'):
            search_term = st.text_input("Enter your search query:")
            submit_button = st.form_submit_button("Search")
        if submit_button:
            genre_dict = {"English": "e", "Hindi": "h", "Gujarati": "g",
                          "Bengali": "b", "Punjabi": "p", "Tamil": "t"}
            genre = st.radio("What's your preferred output language preference of retrieved documents?",
                             ("English", "Hindi", "Gujarati", "Bengali", "Punjabi", "Tamil"))

            out = search(search_term, pos_lis, genre_dict[genre])

            for i, doc in enumerate(len(out)):
                st.write(
                    '...........................................................')
                st.write(f"Document {i+1}:")
                st.write(doc)
                st.write(
                    '...........................................................')
    elif choice == "Hindi":

        st.subheader("Please enter your query in Hindi")
        with st.form(key='searchform'):
            search_term = st.text_input("Enter your search query:")
            submit_button = st.form_submit_button("Search")
        if submit_button:
            genre_dict = {"English": "e", "Hindi": "h", "Gujarati": "g",
                          "Bengali": "b", "Punjabi": "p", "Tamil": "t"}
            genre = st.radio("What's your preferred output language preference of retrieved documents?",
                             ("English", "Hindi", "Gujarati", "Bengali", "Punjabi", "Tamil"))

            out = search(search_term, pos_lis, genre_dict[genre])

            for i, doc in enumerate(len(out)):
                st.write(
                    '...........................................................')
                st.write(f"Document {i+1}:")
                st.write(doc)
                st.write(
                    '...........................................................')
    elif choice == "Gujarati":

        st.subheader("Please enter your query in Gujarati")
        with st.form(key='searchform'):
            search_term = st.text_input("Enter your search query:")
            submit_button = st.form_submit_button("Search")
        if submit_button:
            genre_dict = {"English": "e", "Hindi": "h", "Gujarati": "g",
                          "Bengali": "b", "Punjabi": "p", "Tamil": "t"}
            genre = st.radio("What's your preferred output language preference of retrieved documents?",
                             ("English", "Hindi", "Gujarati", "Bengali", "Punjabi", "Tamil"))

            out = search(search_term, pos_lis, genre_dict[genre])

            for i, doc in enumerate(len(out)):
                st.write(
                    '...........................................................')
                st.write(f"Document {i+1}:")
                st.write(doc)
                st.write(
                    '...........................................................')
    elif choice == "Tamil":

        st.subheader("Please enter your query in Tamil")
        with st.form(key='searchform'):
            search_term = st.text_input("Enter your search query:")
            submit_button = st.form_submit_button("Search")
        if submit_button:
            genre_dict = {"English": "e", "Hindi": "h", "Gujarati": "g",
                          "Bengali": "b", "Punjabi": "p", "Tamil": "t"}
            genre = st.radio("What's your preferred output language preference of retrieved documents?",
                             ("English", "Hindi", "Gujarati", "Bengali", "Punjabi", "Tamil"))

            out = search(search_term, pos_lis, genre_dict[genre])

            for i, doc in enumerate(len(out)):
                st.write(
                    '...........................................................')
                st.write(f"Document {i+1}:")
                st.write(doc)
                st.write(
                    '...........................................................')
    elif choice == "Punjabi":

        st.subheader("Please enter your query in Punjabi")
        with st.form(key='searchform'):
            search_term = st.text_input("Enter your search query:")
            submit_button = st.form_submit_button("Search")
        if submit_button:
            genre_dict = {"English": "e", "Hindi": "h", "Gujarati": "g",
                          "Bengali": "b", "Punjabi": "p", "Tamil": "t"}
            genre = st.radio("What's your preferred output language preference of retrieved documents?",
                             ("English", "Hindi", "Gujarati", "Bengali", "Punjabi", "Tamil"))

            out = search(search_term, pos_lis, genre_dict[genre])

            for i, doc in enumerate(len(out)):
                st.write(
                    '...........................................................')
                st.write(f"Document {i+1}:")
                st.write(doc)
                st.write(
                    '...........................................................')


except:
    pass
