from langchain_community.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Create a LlamaCpp instance
llm = LlamaCpp(model_path="C:/Users/gsdav/AppData/Local/nomic.ai/GPT4All/Meta-Llama-3-8B-Instruct.Q4_0.gguf")

# Create a PromptTemplate
template = """Question: {question} Answer: Let's work this out in a step by step way to be sure we have the right answer."""
prompt = PromptTemplate(template=template, input_variables=["question"])

# Create an LLMChain
llm_chain = llm | prompt

# Ask a question
question = "Who is Bjarne Stroustrup and how is he related to programming?"

# Get the answer
answer = llm_chain.invoke(question)

# Print the answer
print(answer)