import os
from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import AzureChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def summarize(summary: str) -> str:
    llm = AzureChatOpenAI(
    deployment_name=os.getenv("CHAT_DEPLOYMENT_NAME"),
    temperature=0.5,)

    # テンプレートの準備
    template = """
    以下の論文のアブストラクトの、「目的」「方法」「新規性」を中学生でもわかるように一言で表し、大学生がわかるようになるべく詳細に400文字程度で要約してください。
    アブストラクト: {human_input}

    出力の形式は以下の通りです。
    目的:
    方法:
    新規性:"""

    # プロンプトテンプレートの準備
    prompt = PromptTemplate(
        input_variables=["human_input"],
        template=template
    )

    # LLMChainの準備
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        # verbose=True,
    )

    response = llm_chain.predict(human_input=summary)

    return response
