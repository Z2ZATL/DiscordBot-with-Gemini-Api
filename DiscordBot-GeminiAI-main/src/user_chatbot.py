import discord
import os
import json
import tracemalloc
import google.generativeai as genai
from asyncio import Semaphore
from src.response import send_message
from dotenv import load_dotenv

load_dotenv()
tracemalloc.start()

users_chatbot = {}

async def set_chatbot(user_id, api_key=None, model=None, temperature: float=None, harassment=None, hate_speech=None, sexually_explicit=None, dangerous_content=None):
    if user_id not in users_chatbot:
        users_chatbot[user_id] = UserChatbot(user_id)
    chatbot = users_chatbot[user_id]
    if api_key:
        chatbot.set_api_key(api_key)

    if model:
        chatbot.set_model(model)
    
    if temperature:
        chatbot.set_temperature(temperature)
    
    if harassment:
        chatbot.set_harassment(harassment)
    
    if hate_speech:
        chatbot.set_hate_speech(hate_speech)

    if sexually_explicit:
        chatbot.set_sexually_explicit(sexually_explicit)
    
    if dangerous_content:
        chatbot.set_dangerous_content(dangerous_content)

def get_users_chatbot():
    return users_chatbot
    
class UserChatbot():
    def __init__(self, user_id):
        self.sem_send_message = Semaphore(1)
        self.api_key = None
        self.chatbot = None
        self.thread = None
        self.model = None
        self.g_model = None
        self.user_id = user_id
        self.generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]
    
    def set_api_key(self, api_key):
        self.api_key = api_key
    
    def get_api_key(self):
        return self.api_key
    
    def del_api_key(self):
        self.api_key=None

    def set_thread(self, thread: discord.threads.Thread):
        self.thread = thread
    
    def get_thread(self) -> discord.threads.Thread:
        return self.thread
    
    def set_model(self, model: str):
        self.model = model
    
    def get_model(self) -> bool:
        return self.model
    
    def get_chatbot(self):
        return self.chatbot
    
    def set_temperature(self, temperature):
        self.generation_config["temperature"] = temperature
    
    def set_harassment(self, harassment):
        self.safety_settings[0]["threshold"] = harassment

    def set_hate_speech(self, hate_speech):
        self.safety_settings[1]["threshold"] = hate_speech

    def set_sexually_explicit(self, sexually_explicit):
        self.safety_settings[2]["threshold"] = sexually_explicit

    def set_dangerous_content(self, dangerous_content):
        self.safety_settings[3]["threshold"] = dangerous_content

    async def initialize_chatbot(self, interaction: discord.Interaction):
        if self.api_key == None and os.getenv("GOOGLE_API_KEY"):
            self.api_key = os.getenv("GOOGLE_API_KEY")
        elif self.api_key == None:
            await interaction.followup.send("> **ERROR：Please upload your api key.**")
            return False

        genai.configure(api_key=self.api_key)
        self.g_model = genai.GenerativeModel(model_name=self.model,
                                      generation_config=self.generation_config,
                                      safety_settings=self.safety_settings)
        self.chatbot = self.g_model.start_chat(history=[])
        return True

    async def send_message(self, message: str):
        if not self.sem_send_message.locked():
            async with self.sem_send_message:
                async with self.thread.typing():
                    if self.model == "gemini-pro" or "gemini-1.0-pro":
                        await send_message(self.chatbot, message, self.thread)                 
        else:
            await self.thread.send("> **ERROE：Please wait for the previous command to complete.**")

    async def reset_conversation(self):
        self.chatbot = self.g_model.start_chat(history=[])