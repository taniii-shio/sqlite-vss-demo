import os
from dotenv import load_dotenv
from typing import List
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import create_extraction_chain
from langchain.prompts import PromptTemplate

import schemas.paper as paper_schema

load_dotenv()

def summarize(abstract: str):
    llm = AzureChatOpenAI(
    deployment_name=os.getenv("CHAT_DEPLOYMENT_NAME"),
    temperature=0,)

    schema = {
        "properties": {
            "purpose": {
                "type": "string",
                "description": "The purpose of the paper",
            },
            "method": {
                "type": "string",
                "description": "The method of the paper",
            },
            "novelty": {
                "type": "string",
                "description": "The novelty of the paper",
            },
        },
        "required": ["purpose", "method", "novelty"],
    }

    template = """
        From the following abstract, please tell us "purpose", "method", and "novelty" in about 3 sentences each. Also, please make sure that a junior high school student can understand it.
        Abstract: {abstract}
    """

    prompt = PromptTemplate(
        input_variables=["abstract"],
        template=template
    )

    chain = create_extraction_chain(schema=schema, llm=llm, prompt=prompt)
    result = chain.predict(abstract=abstract)

    return result
