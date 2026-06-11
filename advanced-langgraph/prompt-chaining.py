"""
Task: Content Generation pipeline with Quality Control

Input:
 - Topic
 - Quality Requirements

Steps:
 - Generate an initial draft of the content based on the topic.
 - Fact check the generated content against reliable sources.
 - Improve the content based on the fact-checking results, ensuring it meets the specified quality requirements.
 - Format the final content according to the desired style and structure.
"""

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class ContentState(TypedDict):
    topic: str
    requirements: str
    draft: str
    fact_check_results: str
    improved_content: str
    final_content: str

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Define Node
def generate_draft(state: ContentState) -> ContentState:
    """Generate an initial draft of the content based on the topic."""
    prompt = f"""
        Write a 200-word article on the following topic: {state['topic']}.
        Requirements: {state['requirements']}.
        Ensure the content is engaging and informative.
    """
    draft = llm.invoke(prompt).content
    print("======Step #1 Draft Generated:", draft)
    print("-" * 50)
    print(draft[:150] + "...\n")
    
    state['draft'] = draft # type: ignore

    return state

def fact_check(state: ContentState) -> ContentState:
    """Fact check the generated content against reliable sources."""
    prompt = f"""
        Fact check the following content for accuracy and reliability:
        {state['draft']}
        Indentify:
        1. Any factual inaccuracies.
        2. The reliability of the sources used.
        3. Statements that require citations.

        Provide a summary of any inaccuracies or issues found.
    """
    fact_check_results = llm.invoke(prompt).content
    print("====== Step #2 Fact Check Results:", fact_check_results)
    print("-" * 50)
    
    state['fact_check_results'] = fact_check_results # type: ignore

    return state

def improve_content(state: ContentState) -> ContentState:
    """Improve the content based on the fact-checking results, ensuring it meets the specified quality requirements."""
    prompt = f"""
        Based on the following fact check results, improve the content to address any inaccuracies or issues:
        Fact Check Results: {state['fact_check_results']}
        Original Draft: {state['draft']}
        Requirements: {state['requirements']}
        
        Ensure the improved content is accurate, reliable, and meets the specified quality requirements.
    """
    improved_content = llm.invoke(prompt).content
    print("====== Step #3 Improved Content:", improved_content)
    print("-" * 50)
    
    state['improved_content'] = improved_content # type: ignore

    return state

def format_content(state: ContentState) -> ContentState:
    """Format the content with html tags and structure it according to the desired style."""
    prompt = f"""
        Format the following blog post content with appropriate HTML tags and structure it according to the desired style:
        {state['improved_content']}
        
        Add:
        - An engaging title wrapped in <h1> tags.
        - Subheadings wrapped in <h2> tags where appropriate.
        - Paragraphs wrapped in <p> tags.
        - media descriptions wrapped in <div class="media"> tags.

        Output the formatted content as HTML.
    """
    final_content = llm.invoke(prompt).content
    print("====== Step #4 Final Content:", final_content)
    print("-" * 50)
    
    state['final_content'] = final_content # type: ignore

    return state

builder = StateGraph(ContentState)
builder.add_node(generate_draft)
builder.add_node(fact_check)
builder.add_node(improve_content)
builder.add_node(format_content)

builder.add_edge(START, "generate_draft")
builder.add_edge("generate_draft", "fact_check")
builder.add_edge("fact_check", "improve_content")
builder.add_edge("improve_content", "format_content")
builder.add_edge("format_content", END)

graph = builder.compile()

result = graph.invoke({
    "topic": "The Benefits of Regular Exercise",
    "requirements": "The content should be informative, engaging, and supported by scientific evidence. Avoid using technical jargon and ensure it is accessible to a general audience."
}) # type: ignore

print("====== Final Output:", result['final_content'])