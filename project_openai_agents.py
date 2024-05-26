from multiprocessing import Process, Queue

from agents.RunnerAgent import CodeRunnerAgent
from agents.code_gen_agent import CodeGeneratorAgent
from agents.critic_agent import CriticAgent


def start_code_generator_agent(cg_cc_agents_queue,user_prompt):
    cg = CodeGeneratorAgent(cg_cc_agents_queue,user_prompt)
    cg.start()
    
def start_critic_agent(cg_cc_agents_queue,cr_cc_agents_quere):
    ca = CriticAgent(cg_cc_agents_queue,cr_cc_agents_quere)
    ca.start()
    
def start_code_runner_agent(cr_cc_agents_quere):
    cr = CodeRunnerAgent(cr_cc_agents_quere)
    cr.start()

if __name__ == "__main__":
    
    user_prompt = "Write me ONLY python code to print Hello World!"
    
    cg_cc_agents_queue = Queue()
    cr_cc_agents_quere = Queue()
    
    code_generator_process = Process(target=start_code_generator_agent,args=(cg_cc_agents_queue,user_prompt,))
    code_runner_agent = Process(target=start_code_runner_agent,args = (cr_cc_agents_quere,))
    critic_agent = Process(target=start_critic_agent,args=(cg_cc_agents_queue,cr_cc_agents_quere,))
    
    code_generator_process.start()
    code_runner_agent.start()
    critic_agent.start()
    
    code_generator_process.join()
    code_generator_process.join()
    critic_agent.join()
    
    print("Program terminated")