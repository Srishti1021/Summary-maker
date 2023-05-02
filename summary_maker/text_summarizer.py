import spacy 

def text_summarizer(text, lines=3):
    text = " ".join([word for word in text.split()])
    nlp = spacy.load("en_core_web_sm")
    print("inside text summarizer function")
    doc = nlp(text=text)
    word_dict = {}
    sentences = []
    sentence_score = 0
    for word in doc:
        word=word.text.lower()
        if word in word_dict:
            word_dict[word] +=1
        else:
            word_dict[word] = 1
    for i, sentence in enumerate(doc.sents):
        for word in sentence:
            word = word.text.lower()
            sentence_score += word_dict[word]
        sentences.append((i, sentence.text.replace("\n", " "), sentence_score/len(sentence)))
    sorted_sentence = sorted(sentences, key = lambda x : -x[2])
    top_three = sorted(sorted_sentence[:lines], key=lambda x : x[0])
    summary_text = ""
    for sentence in top_three:
        summary_text +=sentence[1] + " "
    return summary_text

if __name__ == "_main_":
    out = text_summarizer('''
    Dash is a Python framework built on top of React, a JavaScript library.
    But Dash also works for R, and most recently supports Julia, and while still described a Python framework, 
    Python isn't used for the other languages, 
    "describing Dash as a Python framework misses a key feature of its design: 
    the Python side (the back end/server) of Dash was built to be lightweight and stateless 
    [allowing] multiple back-end languages to coexist on an equal footing". 
    It is possible to integrate D3.js charts as Dash components. 
    Dash provides the default CSS (and HTML and JavaScript, and you can add your own), 
    but for custom styling Dash applications CSS can be added, or Dash Enterprise used.''',3)
    print("==>", out)

    #with open('content.txt') as file:
     #   text = file.read()
      #  print(text_summarizer(text,1))