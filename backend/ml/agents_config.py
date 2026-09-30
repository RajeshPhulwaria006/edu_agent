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
            template="""
            You are {name}, an academic performance advisor.
            {description}

            Based only on the student's performance data below, provide personalized recommendations.

            Student Performance:
            {input}

            Return exactly 4-5 concise bullet points.
            Focus on:
            1. Weak areas that need improvement
            2. Specific actions to improve them
            3. Study or practice priorities
            4. How to strengthen existing strong areas
            5. One practical next step

            Use plain text only. No Markdown, bullets, headings, emojis, or special formatting.
            Do not make assumptions or recommend anything unsupported by the data.
            """
        )
        chain = prompt_template | self.model | parser
        output = chain.invoke({'input': input, 'name': self.name, 'description': self.description})
        return output

    def analyze(self, input: dict):
        parser = StrOutputParser()
        prompt_template = PromptTemplate(
            input_variables=["input", "name", "description"],
            template="""
                You are {name}, an academic performance analyst.
                {description}

                Analyze the student's performance from the provided data.

                Student data:
                {input}

                Write exactly short notes covering:
                1. Overall performance
                2. Strongest areas
                3. Weakest areas
                4. Areas needing improvement
                5. One actionable recommendation

                Use plain text only. No Markdown, bullets, headings, emojis, or formatting.
                Use only the given data and avoid assumptions or fabricated details.
            """
        )

        chain = prompt_template | self.model | parser
        output = chain.invoke({'input': input, 'name': self.name, 'description': self.description})
        return output
