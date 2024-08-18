# import langchain
# https://towardsdatascience.com/getting-started-with-langchain-a-beginners-guide-to-building-llm-powered-applications-95fc8898732c

from langchain.llms import OpenAI
# pip install tiktoken
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain import PromptTemplate, FewShotPromptTemplate
from langchain.chains import RetrievalQA
from langchain import ConversationChain
# pip install youtube-transcript-api
# pip install pytube
from langchain.document_loaders import YoutubeLoader
# pip install faiss-cpu
from langchain.vectorstores import FAISS
# pip install wikipedia
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

# The LLM takes a prompt as an input and outputs a completion
llm = OpenAI(model_name="text-davinci-003")
# print(llm("Alice has a parrot. What animal is Alice's pet?"))

############################################################################
# Send prompts to a LLM and chain LLMs
# Create two separate prompt-llm pairs, and chain them to generate a catchphrase
############################################################################
# Set up a few shot prompt template for word antonyms
# Sample input and output
examples = [
    {"word": "happy", "antonym": "sad"},
    {"word": "tall", "antonym": "short"},
]
# Text template for dealing with input
example_template = "Word: {word}\tAntonym: {antonym}"
# Initial template to define inputs and the template
example_prompt = PromptTemplate(
    input_variables=["word", "antonym"],
    template=example_template,
)
# Finally definition of the prompt template
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Give the antonym of every input",
    suffix="Word: {input}\nAntonym:",
    input_variables=["input"],
    example_separator="\n",
)

# First chain that calls the initial OpenAI model using the prompt template for antonyms
chain = LLMChain(
    llm = llm, 
    prompt = few_shot_prompt
)
# print(chain.run("colorful socks"))

# Create a second prompt template
second_prompt = PromptTemplate(
    input_variables=["company_name"],
    template="Write a catchphrase for the following company: {company_name}",
)
# And a second chain to generate company catch phrases
chain_two = LLMChain(
    llm=llm,
    prompt=second_prompt
)
# print(chain_two.run("mysterious lunch boxes"))

# Combine the first and the second chains
overall_chain = SimpleSequentialChain(chains=[chain, chain_two], verbose=False)

# Take the antonym (output) of the first chain and use it as input to generate the catchphrase
catchphrase = overall_chain.run("colorful socks")
print(catchphrase)


############################################################################
# Create a knowledge from a youtube video
# Load a youtube video and ask natural language questions
############################################################################
# Create a knowledge store from a youtube video
loader = YoutubeLoader.from_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
documents = loader.load()
# The embeddings model takes a text as an input and outputs a list of floats
embeddings = OpenAIEmbeddings()

# Create the vectorestore to use as the index
db = FAISS.from_documents(documents, embeddings)
retriever = db.as_retriever()

qa = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=retriever, 
    return_source_documents=True
)

# And finally interact with the store
query = "What am I never going to do?"
result = qa({"query": query})
print(result['result'])

############################################################################
# Create persisting memory for the LLM
# Send a series of prompts for which the model will remember the conversation
############################################################################
conversation = ConversationChain(llm=llm, verbose=True)
conversation.predict(input="Alice has a parrot.")
conversation.predict(input="Bob has two cats.")
conversation.predict(input="How many pets do Alice and Bob have?")
conversation.predict(input="Good job")

############################################################################
# Create persisting memory for the LLM
# Create an agent that can lookup information in wikipedia and perform math
############################################################################
tools = load_tools(["wikipedia", "llm-math"], llm=llm)
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
agent.run("When was Barack Obama born? How old was he in 2022?")