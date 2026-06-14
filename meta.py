from PIL import Image
from pypdf import PdfReader, PdfWriter
from docx import Document
from mutagen import File
from mutagen.mp4 import MP4
import streamlit as st
import io
import tempfile
import os

st.title("🔒 Privacy Cleaner - Metadata Remover")

# FILE TYPE SELECTION 
file_type = st.selectbox(
    "Choose the type of file you want to clean:",
    ["-- Select File Type --","Image", "PDF", "Word (.docx)", "MP3", "MP4"]
)


#IMAGE

if file_type == "Image":
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["jpg", "jpeg", "png"]
    )
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )
        # Display metadata
        if hasattr(image, "getexif"):
            exif_data = image.getexif()
            if exif_data:
                st.write("### Metadata Found")
                st.write(dict(exif_data))
            else:
                st.write("No metadata found in this image.")
        # Remove metadata
        data = list(image.getdata())
        new_image = Image.new(image.mode, image.size)
        new_image.putdata(data)
        st.image(
            new_image,
            caption="Image without Metadata",
            use_container_width=True
        )
        st.success("Metadata removed successfully!")
        # Output format
        output_format = st.selectbox(
            "Choose output format:",
            ["PNG", "JPEG", "JPG"]
        )
        save_format = (
            "JPEG" if output_format == "JPG"
            else output_format
        )
        buffer = io.BytesIO()
        new_image.save(buffer, format=save_format)
        buffer.seek(0)
        st.download_button(
            label="📥 Download Clean Image",
            data=buffer,
            file_name=f"clean_image.{output_format.lower()}",
            mime=f"image/{output_format.lower()}"
        )


#PDF
elif file_type == "PDF":
    uploaded_pdf = st.file_uploader(
        "Choose a PDF file...",
        type=["pdf"]
    )
    if uploaded_pdf is not None:
        reader = PdfReader(uploaded_pdf)
        if reader.metadata:
            st.write("### PDF Metadata Found")
            st.write(reader.metadata)
        else:
            st.write("No metadata found in this PDF.")
        writer = PdfWriter()
        # Copy all pages
        for page in reader.pages:
            writer.add_page(page)
        # Remove metadata
        writer.add_metadata({})
        pdf_buffer = io.BytesIO()
        writer.write(pdf_buffer)
        pdf_buffer.seek(0)
        st.success("PDF metadata removed successfully!")
        st.download_button(
            label="📥 Download Clean PDF",
            data=pdf_buffer,
            file_name="clean_document.pdf",
            mime="application/pdf"
        )


# WORD DOCX
elif file_type == "Word (.docx)":
    uploaded_docx = st.file_uploader(
        "Choose a Word document...",
        type=["docx"]
    )
    if uploaded_docx is not None:
        # Open the uploaded document
        doc = Document(uploaded_docx)
        props = doc.core_properties
        # Display existing metadata
        st.write("### Metadata Found")
        metadata = {
            "Author": props.author,
            "Title": props.title,
            "Subject": props.subject,
            "Category": props.category,
            "Comments": props.comments,
            "Keywords": props.keywords,
            "Last Modified By": props.last_modified_by,
            "Language": props.language,
            "Identifier": props.identifier,
            "Content Status": props.content_status
        }
        st.write(metadata)
        # ---------------- Remove Metadata ---------------- #
        # Clear only the safe text fields
        props.author = ""
        props.title = ""
        props.subject = ""
        props.category = ""
        props.comments = ""
        props.keywords = ""
        props.last_modified_by = ""
        props.language = ""
        props.identifier = ""
        props.content_status = ""
        # Save cleaned document into memory
        doc_buffer = io.BytesIO()
        doc.save(doc_buffer)
        doc_buffer.seek(0)
        st.success("Word document metadata removed successfully!")
        # Download button
        st.download_button(
            label="📥 Download Clean Document",
            data=doc_buffer,
            file_name="clean_document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )


# MP3
elif file_type == "MP3":
    uploaded_audio = st.file_uploader(
        "Choose an audio file...",
        type=["mp3", "wav"]
    )
    if uploaded_audio is not None:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(uploaded_audio.name)[1]
        ) as temp_file:
            temp_file.write(uploaded_audio.read())
            temp_path = temp_file.name
        audio = File(temp_path)
        if audio is not None:
            st.write("### Metadata Found")
            st.write(dict(audio.tags) if audio.tags else "No metadata found.")
            # Remove metadata
            audio.delete()
            audio.save()
            st.success("Audio metadata removed successfully!")
            with open(temp_path, "rb") as f:
                audio_bytes = f.read()
            extension = uploaded_audio.name.split(".")[-1]
            st.download_button(
                label="📥 Download Clean Audio",
                data=audio_bytes,
                file_name=f"clean_audio.{extension}",
                mime="audio/mpeg"
            )
        os.remove(temp_path)


#MP4
elif file_type == "MP4":
    uploaded_video = st.file_uploader(
        "Choose an MP4 video...",
        type=["mp4"]
    )
    if uploaded_video is not None:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp4"
        ) as temp_file:
            temp_file.write(uploaded_video.read())
            temp_path = temp_file.name
        try:
            video = MP4(temp_path)
            st.write("### Metadata Found")
            st.write(dict(video.tags) if video.tags else "No metadata found.")
            # Remove metadata
            video.delete()
            video.save()
            st.success("Video metadata removed successfully!")
            with open(temp_path, "rb") as f:
                video_bytes = f.read()
            st.download_button(
                label="📥 Download Clean Video",
                data=video_bytes,
                file_name="clean_video.mp4",
                mime="video/mp4"
            )
        except Exception as e:
            st.error(f"Error processing file: {e}")
        finally:
            os.remove(temp_path)