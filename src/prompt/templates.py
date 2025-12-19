from langchain_core.prompts import PromptTemplate
mcq_prompt_template=PromptTemplate(
    template=(
        "Generate a {difficulty} multiple-choice question about {topic} \n\n"
        "Return only a JSON object with these exact fields:\n"
        "- 'question': A clear, specific question"
        "- 'options': An array of eactly 4 possible answers \n"
        "- 'correct_answer':One of the options that is the correct answer \n\n"
        "Example format:\n"
        '{{\n'
        '   "question":"What is the capital of France?",\n'  
        '   "options":["London","Berlin","Paris","Madrid"],\n'  
        '   "correct_answer":"Paris"\n'  
        '}}\n\n'
        "Your response:"
    ),
    input_variables=["topic","difficulty"]
)
fill_blank_prmopt_template=PromptTemplate(
    template=(
        "Generate a {difficulty} multiple-choice question about {topic} \n\n"
        "Return only a JSON object with these exact fields:\n"
        "- 'question': A sentence with '___' marking where the blank should be\n"
        "- 'answer':The correct word of phrase that belongs on the blank\n\n"
        "Example format:\n"
        '{{\n'
        '   "question"The capital of France is ___",\n'  
        '   "answer":"Paris",\n'   
        '}}\n\n'
        "Your response:"
    )
)