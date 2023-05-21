import streamlit as st
import sqlite3
import hashlib
from PIL import Image
from io import StringIO
from questiongenerator.questiongenerator import QuestionGenerator
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import re
from model import getqapairs

class Streaml:
    #------------ Hashing ------------

    def make_hashes(self, password):
        return hashlib.sha256(str.encode(password)).hexdigest()

    def check_hashes(self, password, hashed_text):
        if self.make_hashes(password) == hashed_text:
            return hashed_text
        return False

    #------------ DB Management ------------

    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    # DB  Functions
    def create_usertable(self):
        Streaml.c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

    def add_userdata(self,username,password):
        Streaml.c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
        Streaml.conn.commit()

    def login_user(self, username,password):
        Streaml.c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
        data = Streaml.c.fetchall()
        return data

    def view_all_users(self):
        Streaml.c.execute('SELECT * FROM userstable')
        data = Streaml.fetchall()
        return data

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
        qg = QuestionGenerator()

        article = text
        qa_list = qg.generate(
        article,
        num_questions=10,
        answer_style='multiple_choice')

        return qa_list
    def remove_whitespaces(self, text):
      '''
      Use the replace method to replace all whitespaces with an empty string
      '''

      return text.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")


    def overlap_score(self, text1, text2):
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
        output = self.generate_qa(summary)
        i = 0
        print("Before Filtering: ")
        for qapair in output:
          print(i)
          print("question: ", qapair['question'])
          for ans in qapair['answer']:
              if ans['correct'] == True:
                 answer = qa(question=qapair['question'], context=summary)
                 overlap_score_var = self.overlap_score(ans['answer'], answer['answer'])
                 if overlap_score_var > 0.60:
                     qa_pair_filtered[qapair['question']] = answer['answer']
          i = i + 1
        k = 0
        qapair = {}
        for key in qa_pair_filtered.keys():
          answers = qa_pair_filtered[key]
          qapair[key] = answers
          k = k + 1
        return qapair

    def generate_qa(self, text:str)-> 'list':
        qg = QuestionGenerator()

        article = text
        qa_list = qg.generate(
        article,
        num_questions=10,
        answer_style='multiple_choice')

        return qa_list
        # return qa_list
    #------------ Streamlit App ------------
    def main(self):
        if 'login_button' not in st.session_state:
            st.session_state.login_button = False
        if 'result' not in st.session_state:
            st.session_state.result = False
        if 'button' not in st.session_state:
            st.session_state.button = False
        if 'output' not in st.session_state:
            st.session_state.output = False
        if 'counter' not in st.session_state:
            st.session_state.counter = 0
        menu = ["Login","SignUp","Flashcard"]
        choice = st.selectbox("Menu",menu)
        
        with st.sidebar:   
            # Add the logo image to the sidebar
            image = Image.open("Assets\FlashMe_logo.png")
            st.image(image)
        

        if choice == "Login":
            st.subheader("Login Section")
            # st.write(st.session_state)
            username = st.text_input("User Name")
            password = st.text_input("Password",type='password')
            login_button = st.button("Login")

            if login_button or st.session_state.login_button:
                self.create_usertable()
                st.session_state.login_button = True
                hashed_pswd = self.make_hashes(password)
                result = self.login_user(username,self.check_hashes(password, hashed_pswd))

                if (len(result) > 0) or st.session_state.result:
                    st.success(f'Logged In as {username}. Please select the Flashcard page')
                    st.session_state.result = True

                else:
                        st.warning("Incorrect Username/Password")

        elif choice == "SignUp":
            st.subheader("Create New Account")
            new_user = st.text_input("Username")
            new_password = st.text_input("Password",type='password')

            if st.button("Signup"):
                self.create_usertable()
                self.add_userdata(new_user,self.make_hashes(new_password))
                st.success("You have successfully created a valid Account")
                st.info("Go to Login Menu to login")

        elif choice == "Flashcard":
            if st.session_state.result:
                    st.subheader("Generate cards")
                    user_input = st.text_area('Enter text to Process')
                    uploaded_file = st.file_uploader("Choose a file") #change this later
                    string_data = ""
                    if uploaded_file is not None:
                        st.write("filename:", uploaded_file.name)
                        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                        string_data = stringio.read()
                    button = st.button('Generate QA pairs')
                    if button or st.session_state.button:
                        st.session_state.button = True
                        st.spinner('Generating Flashcards📚...')
                        if st.session_state.output == False:
                            with st.spinner('Simplifying the content 📖....'):
                                if string_data!= "":
                                    output = getqapairs(string_data)
                                else:
                                    output = getqapairs(user_input)
                            st.session_state.output = output
                            max_value = len(output) - 1
                            my_bar = st.progress(st.session_state.counter/max_value)
                            my_bar.progress(st.session_state.counter/max_value)
                            q = st.session_state.output[st.session_state.counter][0]
                            q = re.sub(r'Front: ', '', q)
                            st.markdown('### ' + str(st.session_state.counter) + '. ' + q )

                            with st.expander("Show Answer"):
                                st.write(output[st.session_state.counter][1])

                            if st.button('Next Question'):
                                if st.session_state.counter < (len(st.session_state.output) - 2):
                                    st.session_state.counter += 1

                        else:
                            if st.session_state.counter == 0:
                                st.session_state.counter += 1
                            max_value = len(st.session_state.output) - 1
                            my_bar = st.progress(st.session_state.counter/max_value)
                            q = st.session_state.output[st.session_state.counter][0]
                            q = re.sub(r'Front: ', '', q)
                            st.markdown('### ' + str(st.session_state.counter) + '. ' + q )

                            with st.expander("Show Answer"):
                                st.write(st.session_state.output[st.session_state.counter][1])

                            if st.button('Next Question'):
                                my_bar.progress(st.session_state.counter/max_value)
                                if st.session_state.counter < (len(st.session_state.output) - 1):
                                    st.session_state.counter += 1
                                else:
                                    st.balloons()
            else:
                st.warning("Please Login first")


stream = Streaml()
stream.main()
