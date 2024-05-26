import json
import os
import random

from openai import OpenAI
import openai

MODEL = 'gpt-4'

with open('keys_list.json','r') as f:
        keys_dict:dict = json.load(f)
    
key = random.choice(list(keys_dict.items()))

os.environ["OPENAI_API_KEY"] = key[1]

client = OpenAI()


class CriticAgent():
    def __init__(self,cg_cc_agents_queue,cr_cc_agents_queue):
        self.cg_cc_agents_queue = cg_cc_agents_queue
        self.cr_cc_agents_quere = cr_cc_agents_queue
    
    def __call_open_ai(self,messages):
        completion = openai.chat.completions.create(
            model = MODEL,
            messages = messages
        )
        
        return  completion.choices[0].message.content
    
    def __send_code_to_code_runner_agent(self,code):
        self.cr_cc_agents_quere.put(code)
        print('cc a trimis cod la runner')
    
    def __send_status_to_generator_agent(self,code='',status=''):
        print('cc trimite status si cod la cg')
        self.cg_cc_agents_queue.put({'code':code,'status':status})
    
    
    def __analyze_code(self,code,error=''):
        print('cc analizeaza cod')
        if error:
            prompt = "You are a python code expert, analyze this code {0} and consider this error too {1}, and decide if it is written correctly. Please write \"YES.\" or \"NO.\"".format(code,error)
        else:
            prompt = "You are a python code expert, analyze this code {0}, and decide if it is written correctly. Please write \"YES.\" or \"NO.\"".format(code)
            
        messages = [{"role":"user","content":prompt}]

        status = self.__call_open_ai(messages)
        if status == "YES.":
            return True,code
        
        if status == "NO.":
            return False,code
        
    def start(self):
        while True:
            #receive message from code generator agent
            print('cc trebuie sa primeasca cod')
            message_from_cg = self.cg_cc_agents_queue.get()
            print('cc a primit cod')
            print('cc trebuie sa analizeze cod')
            result_code_analysis,code_to_be_run = self.__analyze_code(message_from_cg)
            print('cc a analizat cod')
            print(result_code_analysis,code_to_be_run)
            
            if result_code_analysis == True:
                print('cc trimite cod la runner')
                self.__send_code_to_code_runner_agent(code_to_be_run)
                
                print('cc asteapta status de la runner')
                #receive status and code form code runner agent.
                message_from_cr = self.cr_cc_agents_quere.get()
                print('cc a primit status de la runner')
                if message_from_cr['status'] == 'OK':
                    print(message_from_cr)
                    self.__send_status_to_generator_agent({'code':"","status":'OK'})
                    break
                else:
                    print('cc analizeaza cod cu eroare')
                    print(message_from_cr)
                    result_code_analysis,code_to_be_run = self.__analyze_code(message_from_cr['code'],message_from_cr['status'])
                    print(result_code_analysis,code_to_be_run)
                    print('cc trebuie sa trimita status la cg')
                    self.__send_status_to_generator_agent(code=code_to_be_run,status=result_code_analysis)
            else:
                self.__send_status_to_generator_agent.put(code = code_to_be_run,status = 'Please correct this code.')
                