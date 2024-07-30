import streamlit as st
from time import sleep

from prompt_eng.speech_quality_report import get_speech_quality_report


# TODO: See where this should leave
default_bedrock_config = {
    "maxTokenCount": 8192,
    "stopSequences": [],
    "temperature": 0,
    "topP": 1
}

def get_variable_from_file(uploaded_file, variable_name="text"):
    file_content = uploaded_file.read().decode("utf-8")

    global_variables = {}
    local_variables = {}

    try:
        exec(file_content, global_variables, local_variables)
        return local_variables.get(variable_name)
    except Exception as e:
        print(f"Error executing code: {e}")
        return None


def main():

    st.markdown(
    """
    <style>
        h1 {
            color: #3498db; /* Change this color to your desired font color */
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("Speech Quality Evaluator")
    st.write("#")

    tab_text, tab_file = st.tabs(["Text", "File"])

    with tab_text:
        # User input using text_area
        user_input = st.text_area("Enter paragraph to be evaluated:", height=250)
        
        if st.button(label="Evaluate", key="eval_text"):
            with st.container(border=True):
                with st.spinner("Evaluating quality of text, be patient..."):

                    info_label = st.empty()
                    output = st.empty()
                    processed_output = get_speech_quality_report(user_input, default_bedrock_config)

            # Display the output
            info_label.info("QUALITY REPORT")
            output.markdown(processed_output[1])  # TODO: show also the other

    with tab_file:
        # User input for file path
        uploaded_file = st.file_uploader("Enter File Path:")

        if uploaded_file is not None:
            if st.button(label="Evaluate", key="eval_file"):
                with st.container(border=True):
                    with st.spinner("Evaluating quality of text, be patient..."):
                
                        info_label = st.empty()
                        output = st.empty()

                        user_input = get_variable_from_file(uploaded_file)
                        processed_output = get_speech_quality_report(user_input, default_bedrock_config)

                # Display the output
                info_label.info("QUALITY REPORT")
                output.markdown(processed_output[1])  # TODO: show also the other

if __name__ == "__main__":
    main()