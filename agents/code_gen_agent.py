import json
from multiprocessing import Queue
import os
import random

from openai import OpenAI

MODEL = 'gpt-4'

with open('keys_list.json','r') as f:
        keys_dict:dict = json.load(f)
    
key = random.choice(list(keys_dict.items()))

os.environ["OPENAI_API_KEY"] = key[1]

client = OpenAI()


class CodeGeneratorAgent():
    def __init__(self,cg_cc_agents_queue,user_prompt):
        self.cg_cc_agents_queue:Queue = cg_cc_agents_queue
        self.user_prompt = user_prompt
    
    def __call_open_ai(self,messages):
        completion = client.chat.completions.create(
            model = MODEL,
            messages = messages
        )
        
        return  completion.choices[0].message.content

    
    def __send_response_to_critic(self,message):
        print('cg trimite la cc')
        self.cg_cc_agents_queue.put(message)
    
    def generate_python_code(self,messages):        
        response_from_openai = self.__call_open_ai(messages)
        
        return response_from_openai
       
    def start(self):
        messages = [{"role":"user","content":self.user_prompt}]

        while True:
            response_from_openai = self.generate_python_code(messages) 

            self.__send_response_to_critic(response_from_openai)
            print('cg asteapta status de la cg')
            message = self.cg_cc_agents_queue.get()
            print('cg a trimit status de la cc')
            if message['status'] == 'OK':
                break
            else:
                messages.append([{"role":"assistant","content":message['code']}])
                messages.append([{"role":"user","content":message['status']}])
