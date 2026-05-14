import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

st.set_page_config(page_title="AI Chat App", page_icon="🤖")

st.title("🤖 AI Chat Assistant")
st.markdown("Powered by `Qwen2.5-0.5B-Instruct` from Hugging Face")

# ── Load model (cached so it only loads once) ──────────────────────────
@st.cache_resource
def load_model():
    model_name = "Qwen/Qwen2.5-0.5B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    ).to(device)
    model.eval()
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    return tokenizer, model, device

with st.spinner("Loading model... (first time may take a minute)"):
    tokenizer, model, device = load_model()

# ── Sidebar controls ───────────────────────────────────────────────────
st.sidebar.header("⚙️ Generation Settings")
system_prompt = st.sidebar.text_area(
    "System Prompt",
    value="You are a helpful assistant. Give clear and concise answers.",
    height=80
)
max_new_tokens = st.sidebar.slider("Max New Tokens", 20, 400, 150, step=10)
temperature = st.sidebar.slider("Temperature", 0.1, 1.5, 0.7, step=0.1)
top_p = st.sidebar.slider("Top-p", 0.1, 1.0, 0.9, step=0.05)

# ── Chat history ───────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── User input ─────────────────────────────────────────────────────────
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    messages_for_model = [{"role": "system", "content": system_prompt}]
    for m in st.session_state.messages:
        messages_for_model.append({"role": m["role"], "content": m["content"]})

    input_text = tokenizer.apply_chat_template(
        messages_for_model, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(input_text, return_tensors="pt", padding=True).to(device)
    input_length = inputs["input_ids"].shape[1]

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=temperature > 0.01,
            temperature=temperature,
            top_p=top_p,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

    response = tokenizer.decode(output_ids[0][input_length:], skip_special_tokens=True).strip()

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)