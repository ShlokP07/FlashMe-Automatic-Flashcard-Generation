import streamlit as st
from model import flashcards
import sqlite3
import hashlib

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


    #------------ Streamlit App ------------
    def main(self):

        st.set_page_config(page_title="FlashMe", page_icon=":zap:") #layout="wide"
        if 'login_button' not in st.session_state:
            st.session_state.login_button = False
        if 'result' not in st.session_state:
            st.session_state.result = False
        if 'button' not in st.session_state:
            st.session_state.button = False
        if 'output' not in st.session_state:
            st.session_state.output = False
        menu = ["Login","SignUp"]
        choice = st.selectbox("Menu",menu)

        if choice == "Login":
            st.subheader("Login Section")
            st.write(st.session_state)
            username = st.text_input("User Name")
            password = st.text_input("Password",type='password')
            login_button = st.button("Login")

            if login_button or st.session_state.login_button:
                self.create_usertable()
                st.session_state.login_button = True
                hashed_pswd = self.make_hashes(password)
                result = self.login_user(username,self.check_hashes(password, hashed_pswd))

                if (len(result) > 0) or st.session_state.result:
                    st.session_state.result = True
                    st.success("Logged In as {}".format(username))
                    st.subheader("Generate cards")
                    user_input = st.text_area('Enter text to Process')
                    button = st.button('Generate QA pairs')
                    if button or st.session_state.button:
                        st.session_state.button = True
                        st.spinner('Generating Flashcards📚...')
                        print("The button has been clicked")
                        if st.session_state.output == False:
                            Cards = flashcards(True)
                            output = Cards.generate_cards(user_input)
                            st.session_state.output = output
                            st.write("Output: ", st.session_state.output)
                        else:
                            st.write("Output: ", st.session_state.output)
                else:
                        st.warning("Incorrect Username/Password")


                    # uploaded_file = st.file_uploader("Choose a file")
                    # if uploaded_file is not None:
                    # 	st.write("filename:", uploaded_file.name)
                    # 	stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                    # 	string_data = stringio.read()
                    # 	st.text(f'Your message{string_data}')



        elif choice == "SignUp":
            st.subheader("Create New Account")
            new_user = st.text_input("Username")
            new_password = st.text_input("Password",type='password')

            if st.button("Signup"):
                self.create_usertable()
                self.add_userdata(new_user,self.make_hashes(new_password))
                st.success("You have successfully created a valid Account")
                st.info("Go to Login Menu to login")


stream = Streaml()
stream.main()
