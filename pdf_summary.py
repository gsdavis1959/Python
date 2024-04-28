import streamlit as st
import pdfplumber
import spacy
from collections import Counter
import re
import nltk
from nltk.corpus import stopwords
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.llms import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

openai_key = "xxxx"
llm = OpenAI(openai_api_key=openai_key, max_tokens=-1)

num_topics = 10
words_per_topic = 20

# Load the English language model
nlp = spacy.load("en_core_web_sm")
nltk.download('stopwords')
stop_words = set(stopwords.words(['english','spanish']))

def clean_text(text):
    # Remove numbers and special characters
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Remove extra whitespace and newlines
    cleaned_text = ' '.join(cleaned_text.split())
    # Remove stopwords
    cleaned_text = ' '.join([word for word in cleaned_text.split() if word.lower() not in stop_words])
    return cleaned_text

def get_topic_lists_from_pdf(text, num_topics=num_topics):

    # Clean the text

    cleaned_text = clean_text(text)

    
    doc = nlp(cleaned_text)
    

# Get the most common 10 topics
    # Extract noun phrases as topics
    noun_phrases = [chunk.doc for chunk in doc.noun_chunks]
    # Get word vectors for each word in the text
    word_vectors = [token.vector for token in doc if token.has_vector]
    
    # Perform clustering or similarity search here to identify topics
    # For example, you can use KMeans clustering or cosine similarity
    
    # For demonstration, let's just return the top 10 most common words
    words = [token.text for token in doc]
    most_common_topics = Counter(words).most_common(num_topics)
    # Extract entities and count their occurrences
    topics = [ent.text for ent in doc.ents]
    topic_counts = Counter(topics)
    # Return the most common topics
    return topic_counts.most_common(num_topics)


def topics_from_pdf(llm, file, num_topics, words_per_topic):
    """
    Generates descriptive prompts for LLM based on topic words extracted from a
    PDF document.

    This function takes the output of `get_topic_lists_from_pdf` function,
    which consists of a list of topic-related words for each topic, and
    generates an output string in bulleted nested list format.

    Parameters:
        llm (LLM): An instance of the Large Language Model (LLM) for generating
        responses.
        file (str): The path to the PDF file for extracting topic-related words.
        num_topics (int): The number of topics to consider.
        words_per_topic (int): The number of words per topic to include.

    Returns:
        str: A response generated by the language model based on the provided
        topic words.
    """

    # Extract topics and convert them to string
    list_of_topicwords = get_topic_lists_from_pdf(file, num_topics)
    string_lda = ""
    for list in list_of_topicwords:
        string_lda += str(list) + "\n"

    # Create the template
    template_string = '''Describe the topic of each of the {num_topics}
        double-quote delimited lists in a simple sentence and also write down
        three possible different subthemes. The lists are the result of an
        algorithm for topic discovery.
        Do not provide an introduction or a conclusion, only describe the
        topics. Do not mention the word "topic" when describing the topics.
        Use the following template for the response.

        1: <<<(sentence describing the topic)>>>
        - <<<(Phrase describing the first subtheme)>>>
        - <<<(Phrase describing the second subtheme)>>>
        - <<<(Phrase describing the third subtheme)>>>

        2: <<<(sentence describing the topic)>>>
        - <<<(Phrase describing the first subtheme)>>>
        - <<<(Phrase describing the second subtheme)>>>
        - <<<(Phrase describing the third subtheme)>>>

        ...

        n: <<<(sentence describing the topic)>>>
        - <<<(Phrase describing the first subtheme)>>>
        - <<<(Phrase describing the second subtheme)>>>
        - <<<(Phrase describing the third subtheme)>>>

        Lists: """{string_lda}""" '''

    # LLM call
    prompt_template = ChatPromptTemplate.from_template(template_string)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    response = chain.run({
        "string_lda" : string_lda,
        "num_topics" : num_topics
        })

    return response

def read_pdf(file):
    # Using pdfplumber to open and read the PDF
    with pdfplumber.open(file) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    # Join text from all pages
    text = "\n".join(filter(None, pages))
    return text



st.title('PDF Topic Extractor')

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Read the text from the PDF
    file = read_pdf(uploaded_file)
    # Generate topics from the text
    topics = get_topic_lists_from_pdf(file)
    # Show the extracted topics
    st.write("Extracted Topics:")
    for topic, freq in topics:
        st.write(f"{topic} (occurrences: {freq})")



st.subheader("Chat with LLM")

submit_button = st.button("Submit")
clear_button = st.button("Clear Response")
response_container = st.empty()

if submit_button:

        response = topics_from_pdf(llm, file, num_topics, words_per_topic)
        
        response_container.text_area("Response", value=response, height=300, disabled=True)
    
if clear_button:
        st.experimental_rerun()
