import streamlit as st
import requests
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

local_host = 'http://localhost:8000/'

session_state = st.session_state

def get_jwt_token(username, password):
    
    url = local_host + 'api/token/'
    data = {
        'username': username,
        'password': password
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        token = response.json()
        access_token = token['access']
        return access_token
    else:
        return None
    

def get_data(token):
    url = local_host + 'data/'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return token
    else:
        return None


if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    
    st.markdown("<h1 style='text-align: center; '>LOGIN</h1> <br>", unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        col1, col2 ,col3= st.columns(3)
        with col2:
            login_button = st.button("Login")

    if login_button:
        token = get_jwt_token(username, password)
        
        if token:
            data = get_data(token)
            
            if data:
                st.session_state['logged_in'] = True
                st.session_state['token'] = token
                st.session_state['username'] = username
                st.experimental_rerun()
            else:
                 st.write("You do not have permission to access the next page")

        else:
            st.error("Invalid username or password.")
            
st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://cdn1.vectorstock.com/i/1000x1000/13/40/todo-list-seamless-pattern-universal-background-vector-7561340.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )    

if 'logged_in' in st.session_state and st.session_state['logged_in']:
    token = st.session_state['token']  
    UserName = st.session_state['username']
    col1,col2 = st.columns([8,2])
    with col1:
        selected = option_menu(
            menu_title="",
            options=["Todo","History",],
            icons=["card-checklist","journal-text"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
        )
    
            
        if selected == "Todo":
            
            a,b = st.columns([3,7])
            with a:
                with st.form(key="form",clear_on_submit=True):
                # if 'session_state' not in st.session_state:
                #     st.session_state['session_state'] = {'task': ''}
                    task = st.text_input("Tasks",key='task')#,value=st.session_state['session_state']['task']
                    
                    # if 'session_state' in st.session_state:
                    #         st.session_state['session_state'] = {'task': task}
                    # else:
                    #     st.session_state['session_state'] = {'task': ''}
                    
                    add = st.form_submit_button("ADD")    
                
            with b:
                if task:
                    if add:
                        st.session_state['session_state'] = {'task': ''}
                        url = local_host + "todo/?type=create"
                        headers = {'Authorization': f'Bearer {token}'}
                        params={
                            "userName":UserName,
                            "task":task,
                            "discription":"",
                            "status":"Pending",
                        }        
                        response = requests.get(url,headers=headers,params=params)
                        if response.status_code == 200: 
                            pass
                        else:
                            st.error("You dont have permission to create the task")
                        
                params={
                            "userName":UserName,
                        }     
                
                url = local_host + "todo/?type=read"
                headers = {'Authorization': f'Bearer {token}'}
                response = requests.get(url,headers=headers,params=params)
                if response.status_code == 200:
                    data = response.json()
                    task = data['task']  
                    for i in range(len(task)):
                        tasks = st.checkbox(task[i],key=task[i])
                        if tasks:
                            with st.container():
                                with st.form(key="forms",clear_on_submit=True):
                                    description = st.text_area("Description")
                                    file=st.file_uploader("please choose a file")
                                    submit = st.form_submit_button("submit")
                                    if description:
                                        if submit :
                                                url = local_host + "todo/?type=uploadfile"
                                                headers = {'Authorization': f'Bearer {token}'}
                                                params = {
                                                    "userName":UserName,
                                                    "description":description,
                                                    "status":"Done",
                                                    "task":task[i],
                                                }
                                                files = {
                                                    'file': file
                                                }
                                                st.success("Submited successfully")
                                                response = requests.post(url,headers=headers,params=params,files=files)
                                                if response.status_code == 200:
                                                    st.success("WOW")
                                                else:
                                                    st.error("ERROR")     
                else:
                    st.error(f'Error: {response.status_code}')
                    
                              
        if selected == "History":
            params={
                    "userName":UserName,
                }     
            
            url = local_host + "todo/?type=history"
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(url,headers=headers,params=params)
            
                        
            if response.status_code == 200:
                data = response.json()
                tasks = data['tasks']
                files = data['files']
                description = data['description']
                st.header("Completed Tasks")
                for i in range(len(tasks)):
                    details = st.button(f'{i+1}.{tasks[i]}')
                    # Apply CSS styles to hide the button structure
                    button_style = """
                        <style>
                        .stButton>button {
                            background: none;
                            border: none;
                            padding: 0;
                            margin: 0;
                            font-size: inherit;
                            font-family: inherit;
                            cursor: pointer;
                            outline: inherit;
                        }
                        </style>
                    """

                    # Display the CSS styles
                    st.markdown(button_style, unsafe_allow_html=True)
                    if details:
                        st.write("Description:", description[i])                        
                        st.write("click the link to download the file:", files[i])         
            else:
                st.error("Failed to fetch data from the backend")

    with col2:
        a,b = st.columns([3,5])
        with b:
            image="/home/anjana/todo_project/pp2.png"
            st.image(image, caption= "Profile photo", width=160)
        



