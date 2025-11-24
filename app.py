import os
import gradio as gr
from dotenv import load_dotenv
from groq import Groq

# ----------------- Load API key -----------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in .env")

# ----------------- Groq client -----------------
groq_client = Groq(api_key=GROQ_API_KEY)

GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
]


def generate_response(user_input: str, system_context: str, tone: str, model: str) -> str:
    """
    Generate chatbot reply using Groq LLM.
    """
    prompt = (
        f"System context: {system_context}\n"
        f"Tone: {tone}\n"
        f"User: {user_input}\n"
        f"Assistant:"
    )

    completion = groq_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return completion.choices[0].message.content


# ----------------- Avatar video (mock) -----------------
def generate_avatar_video(text: str) -> str:
    """
    Mock avatar video generator for college project.

    Instead of calling a paid avatar API, we simply return the path
    to a pre-recorded talking-head video stored locally.
    """
    video_path = "assets/avatar.mp4"  # make sure this file exists
    if not os.path.exists(video_path):
        # Fallback: if file is missing, return None
        # Gradio will just show an empty video box
        return None
    return video_path


# ----------------- Gradio callback -----------------
def chat(input_text, system_context, model, tone):
    """
    Gradio callback.

    NOTE: parameter order must match inputs list:
    (Your Input, System Context, Groq Model, Tone)
    """
    try:
        reply = generate_response(input_text, system_context, tone, model)
    except Exception as e:
        # Show Groq error in textbox
        return f"[Groq error: {e}]", None

    # Get mock avatar video path
    video = generate_avatar_video(reply)
    if video is None:
        return f"{reply}\n\n[Avatar video file not found at assets/avatar.mp4]", None

    return reply, video


# ----------------- Gradio UI -----------------
iface = gr.Interface(
    fn=chat,
    inputs=[
        gr.Textbox(label="Your Input", placeholder="Type your message here..."),
        gr.Textbox(
            label="System Context",
            value="You are a helpful, natural-sounding assistant.",
        ),
        gr.Dropdown(GROQ_MODELS, value=GROQ_MODELS[0], label="Groq Model"),
        gr.Dropdown(
            ["Neutral", "Friendly", "Formal", "Humorous", "Professional"],
            value="Neutral",
            label="Tone",
        ),
    ],
    outputs=[
        gr.Textbox(label="Chatbot Response"),
        gr.Video(label="Avatar Video", autoplay=True),
    ],
    title="Talking Avatar Chatbot (Groq + Avatar Video)",
    description="A conversational AI chatbot that replies with text and plays a speaking avatar video (pre-recorded) for academic demonstration.",
)

if __name__ == "__main__":
    iface.launch(share=True, debug=True)
