import streamlit as st
import llama_cpp

# Initialize the GPT4All model
llama = llama_cpp.Llama(model_path="C:/Users/gsdav/AppData/Local/nomic.ai/GPT4All/Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf")

def ask_llm(question):
     """Asks the llama model a question.

  Args:
    question: The question to ask.

  Returns:
    The answer to the question.
  """
     response = llama(question)
     return response["choices"][0]["text"]

def main():
    st.title("LLM Chat Interface")

    # User question input
    user_question = st.text_input("Ask a question:", "")

    # Container for the response
    response_container = st.empty()

    # Button to submit the question
    if st.button("Submit"):
        # Get the response from the LLM
        response = ask_llm(user_question)
        # Display the response
        response_container.text_area("Response:", value=response, height=300, disabled=True)

    # Button to clear the question
    if st.button("Clear Question"):
        # This will clear the question input and the response display
        st.experimental_rerun()

if __name__ == "__main__":
    main()
