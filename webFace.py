import streamlit as st
from geminiModelAssist import GModel

# set to wide mode
st.set_page_config(layout="wide")

def random_print(_from, text):
    st.markdown(f"**{_from}**")
    st.write(text)


def get_model_response(user_input):
    response = GModel.interact(str(user_input))

    res = response['response']
    response_obj = response['response_obj']
    
    st.write(response_obj)
    try:
        candidates = response_obj['candidates']
        st.write(candidates)
    except:
        st.write("No candidates found")
        pass

    random_print('Gemini-Pro-Experimental', res)

with st.sidebar:
    st.markdown("""### Login""")
    LoogedInUser = st.text_input("Prefered user Name", key="user_name")

st.title("📝 Gemini Email Assistant")

col1, col2 = st.columns([4, 7])


with col1:
    uploaded_file = st.file_uploader("Optional File Updload", type=("txt", "md"))

    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type}
        st.write(file_details)


with col2:
    if LoogedInUser == "":
        st.warning("Please enter a user name to continue")
    else:
        with st.form(key='interaction_form'):
            user_input = st.text_area(f"{LoogedInUser}:: ")

            fmCol1, fmCol2 = st.columns([1, 1])
            with fmCol1:
                conversation_uploaded_file = st.file_uploader("Upload Email Extract", type=("txt", "md"))

            with fmCol2:
                st.markdown("""### Instructions
                                Note that we currently only support text files.
                            """)
            
            # submit button
            submit_button = st.form_submit_button(label='Submit')
            if submit_button:
                get_model_response(user_input)


