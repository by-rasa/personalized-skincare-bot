import gradio as gr
import requests
import json
from typing import List, Tuple

class RasaChatInterface:
    def __init__(self, rasa_url: str = "http://localhost:5005"):
        self.rasa_url = rasa_url
        self.webhook_url = f"{rasa_url}/webhooks/rest/webhook"
        self.sender_id = "gradio_user"
    
    def send_message(self, message: str) -> List[str]:
        """Send message to Rasa and return bot responses"""
        payload = {
            "sender": self.sender_id,
            "message": message
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                bot_responses = response.json()
                return [msg.get("text", "") for msg in bot_responses if msg.get("text")]
            else:
                return [f"Error: Server returned status code {response.status_code}"]
                
        except requests.exceptions.RequestException as e:
            return [f"Connection error: {str(e)}"]
    
    def chat_function(self, message: str, history: List[Tuple[str, str]]) -> Tuple[List[Tuple[str, str]], str]:
        """Process chat message and update history"""
        if not message.strip():
            return history, ""
        
        # Get bot responses
        bot_responses = self.send_message(message)

        # Add user message and bot responses to history
        history.append((message, "\n\n".join(bot_responses)))
        
        return history, ""

def create_skincare_ui():
    """Create and launch the Gradio interface"""
    
    # Initialize chat interface
    chat_interface = RasaChatInterface()
    
    # Custom CSS for skincare theme
    css = """
    .gradio-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .chat-container {
        padding: 4px;
        background: #ae63bd;
        border-radius: 2px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .message-user {
        background: #e3f2fd !important;
        border-radius: 18px 18px 5px 18px;
    }
    .message-bot {
        background: red !important;
        border-radius: 18px 18px 18px 5px;
    }
    """
    # background: #f3e5f5 !important;
    
    with gr.Blocks(css=css, title="Skincare Consultation Bot") as interface:
        
        gr.Markdown(
            """
            # 🌸 Personalized Skincare Consultation Bot
            
            Welcome to your AI-powered skincare advisor! I'll help you create a personalized 
            day and night skincare routine based on your skin type, age, and specific concerns.
            
            **To get started, simply say "Hi" or "I need skincare advice"**
            """,
            elem_classes=["chat-container"]
        )
        
        # Information panel
        with gr.Accordion("ℹ️ About This Bot", open=False):
            gr.Markdown(
                """
                This skincare consultation bot will:
                
                1. **Ask about your skin type** (oily, dry, combination, sensitive, normal)
                2. **Determine your age range** (teens, twenties, thirties, forties, 50+)
                3. **Identify your skin concerns** (acne, dark spots, wrinkles, dullness, etc.)
                4. **Generate personalized routines** for morning and evening
                
                The recommendations are based on dermatological best practices and 
                will be tailored specifically to your needs.
                
                **Note:** This is for informational purposes only. Always consult with 
                a dermatologist for serious skin concerns.
                """
            )
        
        # Chat interface
        chatbot = gr.Chatbot(
            value=[],
            height=400,
            elem_classes=["chat-container"],
            show_label=False
        )
        
        with gr.Row():
            msg_input = gr.Textbox(
                placeholder="Type your message here... (e.g., 'Hi' or 'I need skincare advice')",
                show_label=False,
                scale=4,
                container=False
            )
            send_btn = gr.Button("Send", variant="primary", scale=1)
        
        # Quick start buttons
        with gr.Row():
            gr.Markdown("**Quick Start:**")
        
        with gr.Row():
            start_btn = gr.Button("🌟 Start Consultation", variant="secondary")
            reset_btn = gr.Button("🔄 Reset Chat", variant="secondary")
        
        # Event handlers
        def send_message(message, history):
            return chat_interface.chat_function(message, history)
        
        def quick_start(history):
            return chat_interface.chat_function("I need skincare advice", history)
        
        def reset_chat():
            return [], ""
        
        # Wire up events
        msg_input.submit(
            send_message,
            inputs=[msg_input, chatbot],
            outputs=[chatbot, msg_input]
        )
        
        send_btn.click(
            send_message,
            inputs=[msg_input, chatbot],
            outputs=[chatbot, msg_input]
        )
        
        start_btn.click(
            quick_start,
            inputs=[chatbot],
            outputs=[chatbot, msg_input]
        )
        
        reset_btn.click(
            reset_chat,
            outputs=[chatbot, msg_input]
        )
        
        # Connection status
        with gr.Row():
            gr.Markdown(
                """
                <small>🔗 Connected to Rasa server at http://localhost:5005</small>
                """,
                elem_id="connection-status"
            )
    
    return interface

if __name__ == "__main__":
    # Install required packages
    print("Starting Skincare Consultation Bot UI...")
    print("Make sure your Rasa server is running on http://localhost:5005")
    print("And your action server is running on http://localhost:5055")
    
    # Create and launch the interface
    interface = create_skincare_ui()
    interface.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,       # Default Gradio port
        share=False,            # Set to True for public link
        debug=True
    )