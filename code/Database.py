import mysql.connector
import sqlite3

import hashlib

#Ceate a hash from current password
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()


#Hashed password comparison
def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

#Class dedicated to storing
class User_MYSQL_Database():


  cursor=None
  connection=None


  def __init__(self,host="127.0.0.1",
                    user="user",
                    password="Pass1234.",database="mydb"):
    self.host=host
    self.user =user
    self.password = password
    self.database = database
    #Connection to database
  def connect(self):

      self.connection = mysql.connector.connect(
        host=self.host,
        user=self.user,
        password=self.password,
        db=self.database
      )
      self.cursor = self.connection.cursor()


  def create_usertable(self,force=False):
      if force:
          self.cursor.execute('DROP TABLE IF  EXISTS  userstable')
          self.cursor.execute('CREATE TABLE IF NOT EXISTS userstable(username varchar(255) NOT NULL,password TEXT,level INT,PRIMARY KEY (username))')
          print("Redoing table: userstable")
      else:
          self.cursor.execute('CREATE TABLE IF NOT EXISTS userstable(username varchar(255) NOT NULL,password TEXT,level INT,PRIMARY KEY (username))')


  def add_userdata(self,username,password,level):
      self.cursor.execute('INSERT INTO userstable(username,password,level) VALUES (%s,%s,%s)',(username,password,level))
      self.connection.commit()

  def login_user(self,username,password):
      self.cursor.execute('SELECT * FROM userstable WHERE username =%s AND password = %s',(username,password))
      data = self.cursor.fetchall()
      return data


  def view_all_users(self):
      self.cursor.execute('SELECT * FROM userstable')
      data = self.cursor.fetchall()
      return data



#SQLite version of the database class
class User_SQLite_Database():

  cursor=None
  connection=None


  def __init__(self,database="data.db"):

    self.database = database

  def connect(self):
      self.connection = sqlite3.connect(self.database)
      self.cursor = self.connection.cursor()


  def create_usertable(self,force=False):
      if force:
          self.cursor.execute('DROP TABLE IF  EXISTS  userstable')
          self.cursor.execute('CREATE TABLE IF NOT EXISTS userstable(username varchar(255) NOT NULL,password TEXT,level INT,PRIMARY KEY (username))')
          print("Redoing table: userstable")
      else:
          self.cursor.execute('CREATE TABLE IF NOT EXISTS userstable(username varchar(255) NOT NULL,password TEXT,level INT,PRIMARY KEY (username))')


  def add_userdata(self,username,password,level):
      self.cursor.execute('INSERT INTO userstable(username,password,level) VALUES (?,?,?)',(username,password,level))
      self.connection.commit()

  def login_user(self,username,password):
      #Can we find the specified hashed password and username pair
      self.cursor.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
      data = self.cursor.fetchall()
      return data


  def view_all_users(self):
      self.cursor.execute('SELECT * FROM userstable')
      data = self.cursor.fetchall()
      return data

#User authentication logic
def UserAuth(userdb,st,choice,pd):
    if choice == "Login":
        st.subheader("Login Section")
        #Print LOGIN form
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            # if password == '12345':
            userdb.create_usertable(force=False)
            hashed_pswd = make_hashes(password)

            result = userdb.login_user(username, check_hashes(password, hashed_pswd))
            if result:
                print(result[0])

                st.success("Logged In as {} with privilege {}".format(username, result[0][2]))

                task = st.selectbox("Task", ["Add Post", "Analytics", "Profiles"])
                if task == "Add Post":
                    st.subheader("Add Your Post")

                elif task == "Analytics":
                    st.subheader("Analytics")
                elif task == "Profiles":
                    st.subheader("User Profiles")
                    #show all users
                    user_result = userdb.view_all_users()
                    #SQL result to dataframe
                    clean_db = pd.DataFrame(user_result, columns=["Username", "Password", "Level"])
                    st.dataframe(clean_db)
            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        new_level = st.text_input("Level")

        if st.button("Signup"):
            #Xreate table
            userdb.create_usertable()
            #Upload user data
            userdb.add_userdata(new_user, make_hashes(new_password), new_level)
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")
# userdb=User_SQLite_Database()
# userdb.connect()
