from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from rasa_core.agent import Agent
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.train import online
from rasa_core.utils import EndpointConfig

#from rasa_core.channels.console import ConsoleInputChannel
#from rasa_core.interpreter import RegexInterpreter


logger = logging.getLogger(__name__)


def run_weather_online(interpreter,
                          domain_file="room_domain.yml",
                          training_data_file='data/stories.md'):
    action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")						  
    
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(max_history=2), KerasPolicy()],
                  interpreter=interpreter,
                  action_endpoint=action_endpoint)
				  
    data = agent.load_data(training_data_file)
    
    '''agent.train(data,
                       batch_size=50,
                       epochs=200,
                       max_training_samples=300)
				   
    online.run_online_learning(agent)'''
	
    agent.train(data,max_training_samples=300)

    return agent


if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    nlu_interpreter = RasaNLUInterpreter('./models/current/nlu')
    run_weather_online(nlu_interpreter)
