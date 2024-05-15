import os
from typing import Dict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

from examples import *


# Function to convert dictionary to string for easier processing
def dict_to_string(dictionary):
    return '; '.join([f'{key}: {value}' for key, value in dictionary.items()])


def get_model(model: str):
    """
    Initialize and return the appropriate language model based on the specified model name.

    Args:
    model (str): The name of the model to initialize. Supported values: "gpt-3.5", "gpt-4".

    Returns:
    ChatOpenAI: The initialized ChatOpenAI model instance.
    """

    # Load environment variables from .env file
    load_dotenv(dotenv_path=".env")

    # Retrieve OpenAI API key from environment variables
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # Initialize the language model based on the specified model name
    if model == "gpt-3.5":
        llm = ChatOpenAI(model="gpt-3.5-turbo-1106")
    elif model == "gpt-4":
        llm = ChatOpenAI(model="gpt-4-turbo-preview")
    else:
        # Raise ValueError for unsupported model names
        raise ValueError("Unsupported model name. Supported values: 'gpt-3.5', 'gpt-4'")
    
    # Return the initialized model
    return llm


def generate_plan(model, lesson_subject: str, lesson_duration: int, student_data: Dict[str, str]) -> str:
    """
    Generate a detailed English lesson plan based on the provided subject, duration, and student data.

    Args:
    model: The language model to use for generating the plan.
    lesson_subject (str): The subject of the English lesson.
    lesson_duration (int): The duration of the lesson.
    student_data (Dict[str, str]): Specific details about the student and their learning context.

    Returns:
    str: A detailed English lesson plan.
    """

    # Examples of inputs and outputs for few-shot learning
    examples = [
        {
            "input": input_present_simple,
            "output": plan_present_simple
        },
        {
            "input": input_eng_for_travel,
            "output": plan_eng_for_travel}
    ]

    # Chat prompt template from the examples
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}")
        ]
    )

    # Few-shot chat message prompt template
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples
    )

    # Final chat prompt template
    final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                ## Overview
                You are a top-tier algorithm designed for creating a comprehensive English lesson plan
                on the lesson subject, taking into consideration all user data.

                ## Task 1. (Generate plan)
                I will provide you with the lesson subject, lesson duration, and specific details about the student and their learning context.
                Your task is to make a detailed plan with an individual approach, taking into account all the data about the student.
                Take into account the student's level of English proficiency and ensure that the lesson is neither too easy nor too difficult.  

                ## Plan Structure
                The plan should include a clear introduction, engaging activities in the main body, a concise conclusion, and relevant homework assignments.
                Ensure the plan is clear, organized, and adaptable, fostering interactive learning experiences between
                the student and the tutor. Use markdown format to structure your plan.

                #### Lesson duration
                The lesson plan must be structured to fit the given time duration precisely, with each section clearly scheduled.

                #### Homework
                Ensure there is no content after the homework section.\
                """),
            few_shot_prompt,
            ("human",
             """Generate {lesson_duration} minutes detailed lesson plan.
             Here is lesson subject: {lesson_subject};
             Here is student data: {student_data}"""),
        ]
    )

    # Convert student data dictionary to string
    student_data_str = dict_to_string(student_data)

    # Chain prompts and llm
    chain = final_prompt | model

    # Invoke the chain with provided inputs
    plan = chain.invoke(
        {"lesson_subject": lesson_subject, "lesson_duration": lesson_duration, "student_data": student_data_str})

    return plan.content
    

def generate_practical_exercises(model, lesson_subject: str, student_data: Dict[str, str]) -> str:
    """
    Generates practical exercises for an English class based on the lesson subject and student data.

    Args:
    model: The chat model to generate exercises.
    lesson_subject (str): The subject of the English lesson.
    student_data (Dict[str, str]): Data about the student.

    Returns:
        str: Practical exercises generated for the English class.
    """
    
    # Examples of inputs and outputs for few-shot learning
    examples = [
        {
            "input": input_past_simple,
            "output": exercises_past_simple
        },
        {
            "input": input_vocabulary,
            "output": exercises_vocabulary}
    ]

    # Chat prompt template from the examples
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}")
        ]
    )

    # Few-shot chat message prompt template
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples
    )

    # Final chat prompt template
    final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                ## Overview
                You are a top-tier algorithm designed for generating practical tasks that will be used during an English lesson.

                ## 1. Task (Generate tasks)
                I will provide you with the lesson subject and specific details about the student and their learning context.
                Your task is to make practical tasks which tutor can use during the lesson.\
                """),
            few_shot_prompt,
            ("human",
             """Generate practical exercises for an English class focused on the lesson subject and data about student.
             Here is lesson subject: {lesson_subject};
             Here is student data: {student_data}"""),
        ]
    )

    # Convert student data dictionary to string
    student_data_str = dict_to_string(student_data)

    # Chain prompts and chat model
    chain = final_prompt | model

    # Invoke the chain with provided inputs
    exercises = chain.invoke({"lesson_subject": lesson_subject, "student_data": student_data_str})

    return exercises.content
