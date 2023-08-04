import os
import re

from dotenv import load_dotenv
from langchain import HuggingFaceHub, PromptTemplate

from ..prompts import keyword_templete

load_dotenv()

REPO_ID = "tiiuae/falcon-7b-instruct"
LLM = HuggingFaceHub(
    repo_id=REPO_ID,
    huggingfacehub_api_token=os.environ["HUGGINGFACEHUB_API_TOKEN"],
    model_kwargs={"temperature": 0.3, "max_new_tokens": 512},
)


def process_generatedkeywords(text: str) -> list[str]:
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

    patt = re.compile(r"^(\d+\.|\d+-)?\s*|- (?=\s|\n)")
    lst = re.split(r"[,\n;]\s*|-(?=\s|\n)", text)
    new_list = [patt.sub("", item).strip().lower() for item in lst if item]
    return list(set(new_list))


async def generate_keywords(promptq: str) -> dict[str, list]:
    """Generate 10 related branding keywords for a given business as a dictionary."""
    prompt = PromptTemplate.from_template(template=keyword_templete)
    chain = prompt | LLM
    response = chain.invoke({"question": promptq})
    # Extract output text.
    keywords_: list[str] = process_generatedkeywords(response)
    return {"kw": keywords_}


async def generate_business_snippet(promptq: str) -> str:
    _template = "Generate upbeat branding snippet for {question}"
    prompt = PromptTemplate.from_template(template=_template)
    chain = prompt | LLM
    response = chain.invoke({"question": promptq})
    return response
