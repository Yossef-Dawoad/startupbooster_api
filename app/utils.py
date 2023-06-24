import re, os, dotenv
from typing import List
from langchain import PromptTemplate, LLMChain, HuggingFaceHub

dotenv.load_dotenv()

def process_generatedkeywords(text: str) -> List[str]:
    """
    Transforms a text containing a list of items separated by commas, newlines, semicolons, or dashes into a list of strings.

    The function removes any numbers followed by a dot or a dash at the beginning of each item, as well as any dashes followed by a space. It also strips any leading or trailing whitespace and converts the items to lowercase.

    Args:
        text (str): The text containing the list of items.

    Returns:
        List[str]: The transformed list of strings.

    Examples:
        >>> process_generatedkeywords("1. Car Shop\\n2. New Car Shop\\n3. Used Car Shop")
        ['car shop', 'new car shop', 'used car shop']

        >>> process_generatedkeywords("- Car Service; - Car Repair; - Car Air Conditioning")
        ['car service', 'car repair', 'car air conditioning']

        >>> process_generatedkeywords("10. Car Accessories, 11-Car Tires, 12 Car Parts")
        ['car accessories', 'car tires', 'car parts']

    Notes:
        * The regular expression  the beginning of each item in the list that include numbers that are not preceded by a dot or a dash.
    """

    patt = re.compile(r"^(\d+\.|\d+-)?\s*|- ")
    lst = re.split(r"[,\n;-]\s*", text)
    new_list = [
        patt.sub("", item).strip().lower()
        for item in lst
        if item
    ]
    return new_list

def generate_keywords(promptq: str) -> List[str]:
    # Load your API key from an environment variable or secret management service
   
    repo_id = "tiiuae/falcon-7b-instruct"
    template = """
You are a helpfull assistant. you gives helpful, summarized, and polite answers to the user's questions.

question: {question}
"""
    prompt = PromptTemplate(template=template, input_variables=["question"])
    print(prompt.template)

    llm = HuggingFaceHub(
        repo_id=repo_id,
        huggingfacehub_api_token=os.getenv("huggingfacehub_api_token"),
        model_kwargs={"temperature":0.6, "max_new_tokens":512}
    )
    response = llm(f"just generate 10 related branding keywords for {promptq}")

    # Extract output text.
    keywords_: List[str] = process_generatedkeywords(response)
    return {"Keywords": keywords_}





