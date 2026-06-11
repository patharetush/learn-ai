from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnableBranch

#1. LLM Setup (simple initialization)
model = ChatOpenAI(
    model="gpt-4.1-nano",
    temperature=0
)

# ---- Define Independent Runnables/Chains for parallel execution ----
#2. Chain A : Generate concise sentence about a topic
sentence_prompt = ChatPromptTemplate.from_template(
    "Generate a very short, concise statement about {topic}"
)

sentence_chain = sentence_prompt | model | StrOutputParser()

#3. Chain B:  Generate a few keywords related to the same topic
keywords_prompt = ChatPromptTemplate.from_template(
    "List 3-5 comma seperated keywords related to: {topic}. Do not add any extra text or intros"
)

keywords_chain = keywords_prompt | model | StrOutputParser()

# --- Combine chain in parallel ---
parallel_generation = RunnableParallel(
    sentence=sentence_chain,
    keywords=keywords_chain
)

# --- Define Conditional Logic (RunnableBranch) ---

#5. Custom RunnableLambda for the conditional check
def is_sentence_short(data:dict) -> bool:
    """ Returns true if the generated sentence is <= 50 characters, False otherwise"""

    sentence = data.get("sentence", "")
    print(f"\n--- DEBUG: Sentence Length check ----")
    print(f"Sentence: '{sentence}' ({len(sentence)}) chars")
    is_short = len(sentence) <= 50
    print(f"Is senetence is short? {is_short}")
    return is_short

sentence_lenth_checker = RunnableLambda(is_sentence_short)

#6. Branch 1: Elaborate if the sentence is short
elaborate_prompt = ChatPromptTemplate.from_messages([
    ("system", "Elaborate on the following sentence using these keywords, adding ,more details"),
    ("user","Sentence: {sentence}\nKeywords: {keywords}\nElaboration:")
])

elaborate_chain = elaborate_prompt | model | StrOutputParser()

#7. Branch 2: Summarize if the senetence is long
summarize_prompt = ChatPromptTemplate.from_messages([
    ("system", "Summarise the following sentence concisely, using these keywords to guide the summary."),
    ("user", "Senetence: {sentence}\nkeywords: {keywords}\nSummary:")
])

summarize_chain = summarize_prompt | model | StrOutputParser()

#.8 Runnable Branch: Direct flow based on the condition
conditional_branch = RunnableBranch(
    (sentence_lenth_checker, elaborate_chain),
    summarize_chain
)

# --- Assemble the full Complex Chain ---
final_complex_chain = parallel_generation | conditional_branch

print("---- Visualizing the complex chain as ASCII Graph ----")
final_complex_chain.get_graph().print_ascii()