from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline
from questiongenerator.questiongenerator import QuestionGenerator

class flashcards:
    def __init__(self, use_summary):
        self.use_summary = use_summary

    # def pre_process(self):
        #   pass

    def get_summary(self, input_text:str, sum_model_no:int)-> str:
        """Generates summary with minimum size of 50% of input
            Args:
                input_text (str): maximum length 1024 tokens
                sum_model_no (int): 0- DistilBart
                                    1- Bart_base
                input_size (int): lenght of the input text
            Returns:
                str: summary of the input
        """
        model_list = ['sshleifer/distilbart-cnn-12-6', 'facebook/bart-large-cnn']#List of models to choose from
        tokenizer = AutoTokenizer.from_pretrained(model_list[sum_model_no])
        model = AutoModelForSeq2SeqLM.from_pretrained(model_list[sum_model_no])
        inputs = tokenizer([input_text], max_length=1024, truncation=True, return_tensors="pt")
        summary_ids = model.generate(inputs["input_ids"], num_beams = 2, min_length = 222, max_new_tokens = 333) #Set min_length max_new_tokens
        return(tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0])

    def generate_qa(self, text: str)-> 'list':
        """Generate question answer pairs
            Args:
                text (str): paragraph on which flashcards have to be generated
                qa_model_no (int): 0- Base
                                    1- Small
            Returns:
                list: list containg dictionary with question and an answer
        """
        qg = QuestionGenerator()

        article = text
        qa_list = qg.generate(
        article,
        num_questions=10,
        answer_style='multiple_choice')

        return qa_list


    def remove_whitespaces(self, text:str) -> str:
        '''
        Use the replace method to replace all whitespaces with an empty string
        '''

        return text.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")


    def overlap_score(self, text1:str, text2:str) -> int:
        '''
        Calculates overlap score using bigrams
        
        '''
        
        # Convert the texts to lowercase for case-insensitivity
        text1 = text1.lower()
        text1 = self.remove_whitespaces(text1)
        text2 = text2.lower()
        text2 = self.remove_whitespaces(text2)

        # Generate the list of bigrams for each text
        bigrams1 = [text1[i:i+2] for i in range(len(text1) - 1)]
        # print(bigrams1)
        bigrams2 = [text2[i:i+2] for i in range(len(text2) - 1)]
        # print(bigrams2)

        # Calculate the number of identical bigrams
        identical_bigrams = len(set(bigrams1) & set(bigrams2))

        # Calculate the total number of bigrams
        # total_bigrams = len(bigrams1) + len(bigrams2)
        total_bigrams = len(set(bigrams1 + bigrams2))
        # print(text1,text2)
        # Return the overlap score
        return (identical_bigrams / total_bigrams)
    
    def generate_cards(self, text):
        qa = pipeline("question-answering")
        qa_pair_filtered = {}
        summary = self.get_summary(text, 0)
        print("Summary: ", summary)

        output = self.generate_qa(summary)
        i = 0
        print("Before Filtering: ")
        for qapair in output:
          print(i)
          print("question: ", qapair['question'])
          for ans in qapair['answer']:
              if ans['correct'] == True:
                 print("T5 Model Answer: ", ans['answer'])
                 answer = qa(question=qapair['question'], context=summary)
                 print(f"DistilBERT Answer: '{answer['answer']}'")
                 overlap_score_var = self.overlap_score(ans['answer'], answer['answer'])
                 print("Overlap Score: ", overlap_score_var)
                 if overlap_score_var > 0.60:
                     qa_pair_filtered[qapair['question']] = answer['answer']
          i = i + 1
        print("After Filtering: ")
        k = 0
        qapair = {}
        for key in qa_pair_filtered.keys():
          answers = qa_pair_filtered[key]
          print("question: ", key)
          print("answer: ", answers)
          qapair[key] = answers
          k = k + 1

        print()
        print("Number of questions before filtering: ", i)
        print("Number of questions after filtering: ", k)
        return qapair

