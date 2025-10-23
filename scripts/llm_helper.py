import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
LLM_PROVIDER = "google"

def get_llm(temp: float = 0.2):
    if LLM_PROVIDER == "google":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            google_api_key=api_key,
            temperature=temp,
            max_output_tokens=1024,
            convert_system_message_to_human=True,
        )
    raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

def create_rag_chain(temp: float = 0.2):
    template = """
    You are an expert IAM assistant.
    Answer only from CONTEXT. If not in context, say "I don't have enough information from the provided context."
    Be concise (3–6 sentences).

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """
    prompt = PromptTemplate.from_template(template)
    llm = get_llm(temp=temp)
    return prompt | llm | StrOutputParser()

def generate_answer(chain, context: str, question: str) -> str:
    return chain.invoke({"context": context, "question": question})

if __name__ == '__main__':
    print("Running a simple test for the RAG chain...")

    test_chain = create_rag_chain(temp=0.0)  # more deterministic for tests
    test_context = """
    The Principle of Least Privilege (PoLP) is a security concept where a user
    is given the minimum levels of access needed to perform their job functions.
    This reduces the attack surface if an account is compromised.
    """
    test_question = "What is the principle of least privilege?"

    try:
        answer = generate_answer(test_chain, test_context, test_question)
        print(f"\nTest Question: {test_question}")
        print(f"\nGenerated Answer:\n{answer}")

        ans = answer.lower()
        assert ("least privilege" in ans) or ("minimum" in ans and "access" in ans)
        print("\nTest PASSED.")
    except Exception as e:
        print(f"\nTest FAILED: {e}")
