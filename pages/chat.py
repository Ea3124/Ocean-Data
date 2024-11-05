import streamlit as st
import time
import requests

def response_generator(assistant_response):
    """Assistant response streaming generator."""
    for word in assistant_response.split():
        yield word + " "
        time.sleep(0.05)

def send_setup_request(category, species):
    setup_data = {
        "category": category,
        "species": species
    }
    try:
        response = requests.post("http://10.125.70.48:5000/setup", json=setup_data)
        response.raise_for_status()  # Raise an error for bad responses
        st.session_state.setup_completed = True  # Set setup completion status
    except requests.exceptions.RequestException:
        st.error("설정 요청 중 오류가 발생했습니다.")  # Show error message
        st.session_state.setup_completed = False  # Ensure setup is not completed

def display_chat_history():
    """Display chat history from session state."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input():
    """Handle user input and send to the server."""
    if prompt := st.chat_input("무엇이 궁금하신가요?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Send prompt to the Flask server
        try:
            response = requests.post(
                "http://10.125.70.48:5000/ask",
                json={"question": prompt}  # Send question in JSON format
            )
            response.raise_for_status()  # Raise an error for bad responses
            assistant_response = response.json().get("answer", "돌아온 답변이 없습니다. 다시 질문해주세요.")  # Get the response
        except requests.exceptions.RequestException:
            assistant_response = "에러가 발생했습니다. 다시 질문해주세요."  # Set error message

        # Display assistant response in a streaming manner
        with st.chat_message("assistant"):
            response_container = st.empty()
            full_response = ""
            for word in response_generator(assistant_response):
                full_response += word  # Accumulate each word
                response_container.markdown(full_response)  # Update the current state

        # Update session state with completed assistant response
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

def select_category_and_species():
    """Select category and species from the user."""
    categories = {
        "어류": "fish",
        "패류": "shellfish",
        "해조류": "seaweed",
        "기타": "etc"
    }
    
    # Category selection
    category = st.selectbox("어종을 선택하세요:", list(categories.keys()))
    st.session_state.category = categories[category]

    # Species selection based on the chosen category
    if st.session_state.category == "fish":
        species_list = ["넙치", "조피볼락", "뱀장어", "무지개송어", "강도다리", "숭어", "향어", "돔류", "메기", "황복", "비단잉어"]
    elif st.session_state.category == "shellfish":
        species_list = ["참굴", "전복", "가리비"]
    elif st.session_state.category == "seaweed":
        species_list = ["곰피", "모자반", "청각", "넓미역", "미역", "김"]
    else:
        species_list = ["해삼양식", "큰징거미새우", "멍게", "흰다리새우"]

    # Species selection
    species = st.selectbox("종을 선택하세요:", species_list)
    st.session_state.species = species

    # Confirm button to send setup request
    if st.button("확인"):
        # Send category and species to the Flask server
        send_setup_request(st.session_state.category, st.session_state.species)
        st.rerun()

def show():
    st.title("Simple Chat")

    # Initialize chat history and setup status
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "setup_completed" not in st.session_state:
        st.session_state.setup_completed = False

    # Display chat messages from history on app rerun
    display_chat_history()

    # Category and species selection
    if not st.session_state.setup_completed:
        select_category_and_species()
    else:
        # Accept user input only if setup is completed
        handle_user_input()
