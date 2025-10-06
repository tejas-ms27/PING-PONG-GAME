import gradio as gr
from your_model import load_model, generate_response

# Load your model once
model = load_model()

def respond(prompt):
    return generate_response(model, prompt)

demo = gr.Interface(
    fn=respond,
    inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here…"),
    outputs="text",
    title="Ping-Pong Game LLM"
)

if __name__ == "__main__":
    demo.launch()
