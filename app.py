import os
import shutil
import streamlit as st
from PIL import Image
from lyzr import ChatBot

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["apikey"]

# Set Streamlit page configuration
st.set_page_config(
    page_title="Lyzr",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png",
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Poem Generator📖 🖋️ ")
st.markdown("### Built using Lyzr SDK🚀")
st.markdown("Craft captivating poems effortlessly using Lyzr's intuitive Poem Generator. Unleash your creativity and refine your writing with ease")

# Function to remove existing files
def remove_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"Error while removing existing files: {e}")

# Set the local directory
data_directory = "data"

# Create the data directory if it doesn't exist
os.makedirs(data_directory, exist_ok=True)

# Remove existing files in the data directory
remove_existing_files(data_directory)

# Function to implement RAG Lyzr Chatbot
def rag_implementation(file_path):
    # Initialize the RAG Lyzr ChatBot
    rag = ChatBot.docx_chat(
        input_files=[file_path],
        llm_params={"model": "gpt-3.5-turbo"},
    )

    return rag

# Function to get Lyzr response
def resume_response(file_path):
    rag = rag_implementation(file_path)
    prompt = f"""To generate a poem for the uploaded document, please follow the instructions below:
                     - Topic Exploration: Explore the topic provided by the user. What are the key elements or themes you can draw upon to create a compelling poem?
                     - Brainstorming: Generate ideas and imagery related to the topic. How can you evoke emotions and capture the essence of the subject matter?
                     - Structuring the Poem: Decide on a structure for the poem. Will it follow a traditional format or a more experimental style? How will you organize the verses to convey your message effectively?
                     - Poetic Devices: Incorporate poetic devices such as metaphors, similes, and personification to enrich the poem's language and imagery. How can you use literary techniques to convey deeper meaning?
                     - Crafting the Flow: Consider the rhythm, meter, and rhyme scheme of the poem. How can you create a harmonious and engaging flow that captivates the reader?
                     - Emotional Tone: Determine the emotional tone and mood you want to convey through the poem. How can you use language and imagery to evoke the desired feelings in the reader?
                     - Refinement: Review the poem for coherence, clarity, and artistic expression. Are there any areas that need refinement or enhancement? How can you polish the poem to perfection?
                     - Poem: With the above information generate a really good poem.
                     - These Topic Exploration , Brainstorming , Structuring the Poem , Crafting the Flow Emotional and Tone Refinement details can be just one sentences.
                     - Make sure the poem is generated. Follow all these steps carefully. """

    response = rag.chat(prompt)
    return response.response

# File upload widget
uploaded_file = st.file_uploader("Choose Word file", type=["docx"])

if uploaded_file is not None:
    # Save the uploaded Word file to the data directory
    file_path = os.path.join(data_directory, uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getvalue())
    
    # Display the path of the stored file
    st.success(f"File successfully saved")

    # Generate poem button
    if st.button("Generate Poem"):
        automatice_response = resume_response(file_path)
        st.markdown(f"{automatice_response}")

# Footer or any additional information
with st.expander("ℹ️ - About this App"):
    st.markdown(
        """Experience the seamless integration of Lyzr's ChatBot as you refine your documents with ease.For any inquiries or issues, please contact Lyzr."""
    )
    st.link_button("Lyzr", url="https://www.lyzr.ai/", use_container_width=True)
    st.link_button(
        "Book a Demo", url="https://www.lyzr.ai/book-demo/", use_container_width=True
    )
    st.link_button(
        "Discord", url="https://discord.gg/nm7zSyEFA2", use_container_width=True
    )
    st.link_button(
        "Slack",
        url="https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw",
        use_container_width=True,
    )

