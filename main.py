import os
import base64
import streamlit as st
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from dotenv import load_dotenv
import nest_asyncio


nest_asyncio.apply()


def get_markdown(upload_pdfs):
    parser = LlamaParse(
        result_type="markdown",
        accurate_mode=True,
        # extract_charts=True
    )

    file_extractor = {".pdf": parser}

    temp_file_path = os.path.join(os.getcwd(), upload_pdfs.name)  # Adjust "/tmp" as needed
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(upload_pdfs.read())  # Write file content to temp file

    try:
        documents = SimpleDirectoryReader(input_files=[temp_file_path],
                                          file_extractor=file_extractor)

        result = documents.load_data()

        text = ''
        for doc in result:
            text += doc.text


    except Exception as e:
        print(f"Error processing PDF {upload_pdfs.name}: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    return text


def main():
    load_dotenv()

    st.set_page_config(page_title='Extract PDFs', page_icon='📚', layout='wide')
    st.title('Extract PDFs📚')

    st.sidebar.header('PDFs Extraction.')
    pdf_uploader = st.sidebar.file_uploader('Upload Your PDFs: ', type='pdf')
    if pdf_uploader:
        if st.sidebar.button('Extract'):
            with st.spinner('Loading Text....'):
                text = get_markdown(pdf_uploader)
            if text:
                st.markdown(text)
            else:
                st.error("Failed to extract text from the uploaded PDF.")


if __name__ == '__main__':
    main()