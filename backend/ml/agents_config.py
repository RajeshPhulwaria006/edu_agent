import os
from dotenv import load_dotenv
from fastapi import Depends
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

class Agent:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.model=ChatGroq(
            model="openai/gpt-oss-120b",
            temperature=0
        )

    def recommend(self, input: dict):
        parser = StrOutputParser()
        prompt_template = PromptTemplate(
            input_variables=["input", "name", "description"],
            template="""You are a {name}.
             {description}
             On the basis of overall student performance, recommend things to improvise in 4-5 lines
             student performance: 
                {input}
            """,
        )
        chain = prompt_template | self.model | parser
        output = chain.invoke({'input': input, 'name': self.name, 'description': self.description})
        return output

    def analyze(self, input: dict):
        parser = StrOutputParser()
        prompt_template = PromptTemplate(
            input_variables=["input", "name", "description"],
            template="""You are a {name}.
             {description}
             On the basis of overall student performance, analyze the performance and provide a detailed analysis in 4-5 lines (mention the weak areas and strong areas in string format not **markdown**)
             student's performance: 
                {input}
            """,
        )

        chain = prompt_template | self.model | parser
        output = chain.invoke({'input': input, 'name': self.name, 'description': self.description})
        return output
