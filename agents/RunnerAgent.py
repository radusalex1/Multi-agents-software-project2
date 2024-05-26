from multiprocessing import Queue


class CodeRunnerAgent():
    def __init__(self,cr_cc_agents_queue):
        self.cr_cc_agents_queue:Queue = cr_cc_agents_queue

    def __send_code_to_critic_agent(self,code,status):
        self.cr_cc_agents_queue.put({'code':code,'status':status})
    
    
    def start(self):
        code = self.cr_cc_agents_queue.get()
        print('cr a primit cod',code)
        try:
            print('cr ruleaza cod')
            exec(code)
            print('cr ruleaza cod oke si trimite status la critic')
            self.__send_code_to_critic_agent(code,"OK")
        except Exception as e:
            print("erorare si trimite cr la cc cod",code,e)
            self.__send_code_to_critic_agent(code,str(e))