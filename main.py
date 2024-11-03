import tkinter as tk
from tkinter import scrolledtext
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Define the prompt template
template = """ 
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

# Initialize the model and prompt
model = OllamaLLM(model="llama3.1")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Define the function to handle conversation
def handle_conversation():
    context = ""
    
    # Retrieve user input and provide the AI response
    def on_send():
        nonlocal context
        user_input = entry.get()
        if user_input.lower() == "exit":
            root.destroy()
            return
        
        result = chain.invoke({"context": context, "question": user_input})
        context += f"\nUser: {user_input}\nAI: {result}"
        
        # Update the chat display
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"You: {user_input}\n")
        chat_display.insert(tk.END, f"Bot: {result}\n")
        chat_display.config(state=tk.DISABLED)
        chat_display.yview(tk.END)
        
        entry.delete(0, tk.END)

    # Create the main window
    root = tk.Tk()
    root.title("AI ChatBot")

    # Create and configure the chat display area
    chat_display = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD)
    chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Create and configure the entry widget for user input
    entry = tk.Entry(root, width=80)
    entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
    
    # Create and configure the send button
    send_button = tk.Button(root, text="Send", command=on_send)
    send_button.pack(side=tk.RIGHT, padx=10, pady=10)
    
    # Bind the Enter key to the send button
    root.bind('<Return>', lambda event: on_send())

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    handle_conversation()