from langchain_core.output_parsers import PydanticOutputParser
from src.models.question_schemas import MCQQuestion, FillBlankQuestion
from src.prompt.templates import mcq_prompt_template, fill_blank_prmopt_template
from src.llm.groq_client import get_groq_llm
from src.config.settings import settings
from src.common.logger import get_logger
from src.common.custom_exception import CustomException



class QuestionGenerator:
    def __init__(self):
        self.llm=get_groq_llm()
        self.logger=get_logger(self.__class__.__name__)

    def _retry_and_parse(self,prompt,parser,topic,difficulty):
         for attempt in range(settings.MAX_RETRIES):
              try:
                  self.logger.info(f"Genrating question for topic {topic} with difficulty {difficulty}")
                  response=self.llm.invoke(prompt.format(topic=topic,difficulty=difficulty))
                  self.logger.info(response)
                  parsed=parser.parse(response.content)
                  self.logger.info("Successfully parsed the logger")
                  return parsed
              except Exception as e:
                  self.logger.error(f"Error coming {e}")
                  if attempt==settings.MAX_RETRIES-1:
                      raise CustomException(f"Error generated after {settings.MAX_RETRIES} attempts",e)

    def generate_mcq(self,topic:str,difficulty:str='medium')->MCQQuestion:
        try:
            parser=PydanticOutputParser(pydantic_object=MCQQuestion)
            question=self._retry_and_parse(mcq_prompt_template,parser,topic,difficulty)
            if len(question.options)!=4 or question.correct_answer not in question.options:
                raise ValueError("Invalid MCQ structure")
            self.logger.info("Generated a valid MCQ question")
            return question
        except Exception as e:
            self.logger.error(f"Failed to generate MCQ : {str(e)}")
            raise CustomException("MCQ Genration failed",e)
        
    
    def generate_fill_blank(self,topic:str,difficulty:str='medium')->FillBlankQuestion:
        try:
            parser=PydanticOutputParser(pydantic_object=FillBlankQuestion)
            question =self._retry_and_parse(fill_blank_prmopt_template,parser,topic,difficulty)
            if "___" not in question.question:
                 raise ValueError("Fill in the blank should contain '___'")
            self.logger.info("Generated a valid Fill in the balank question")
            return question
        except Exception as e:
            self.logger.error(f"Failed to generate fillup : {str(e)}")
            raise CustomException("Fillup Genration failed",e)    

