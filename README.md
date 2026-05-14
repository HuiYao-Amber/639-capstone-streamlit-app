# AI Chat Assistant — Capstone Project

## Project Description
This is an interactive AI chat application built with Streamlit.
It uses the `Qwen2.5-0.5B-Instruct` large language model from Hugging Face
to answer user questions in a conversational interface.

## Files Included
| File | Description |
|------|-------------|
| `app.py` | Main Streamlit application |
| `requirements.txt` | Python dependencies |
| `README.md` | This file |

## How to Use
1. Install dependencies:
 pip install -r requirements.txt
2. Run the app:
 streamlit run app.py
3. Open your browser at `http://localhost:8501`
4. Type your message in the chat box at the bottom
5. Adjust generation settings in the left sidebar:
   - **System Prompt**: defines the assistant's behavior
   - **Max New Tokens**: controls response length
   - **Temperature**: controls creativity (higher = more creative)
   - **Top-p**: controls diversity of word choices

## Demo Video
[Click here to watch the demo](YOUR_VIDEO_LINK_HERE)

## Model Used
- **Model**: Qwen/Qwen2.5-0.5B-Instruct
- **Source**: Hugging Face
- **Task**: Conversational text generation
