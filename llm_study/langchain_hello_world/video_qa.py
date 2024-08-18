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
# Create a knowledge from a youtube video
# Load a youtube video and ask natural language questions
############################################################################
# Create a knowledge store from a youtube video
loader = YoutubeLoader.from_youtube_url("https://www.youtube.com/watch?v=Q9m_6TVJysI&t=13s&ab_channel=JordanBPeterson")
    
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
query = "What are the 12 best investments discussed in the video?"
result = qa({"query": query})
print(result['result'])

