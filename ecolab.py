from agents import rabbit, fox
import environment
import numpy as np

def agent_solve(env):
    new_agents = []  # List of new agents created for this iteration

    if env.mode == 'sync':
        # Update old_pos in each agent's message dictionary 
        # so that it contains position from previous iteration
        for agent in env.agents:
            agent.messages['old_pos'] = agent.pos

        #Apply rules
        for agent in env.agents:
            eaten = agent.eat(env)

            # If the agent hasn't eaten, migrate
            if not eaten:
                agent.migrate(env)

            # Apply the death rule - from starvation or old age
            agent.die(env)
                
            # If the agent did not die, apply the breed rule
            if not agent.dead:
                new = agent.breed(env)
                if new is not None:
                    new_agents.append(new)
                    
        # Add new agents to list
        env.agents.extend(new_agents)
                
        # Clean up the dead
        # First, how many have been eaten? 
        # We need to do it here since rabbits can be eaten twice
        # This could be simplified if we stop using last_pos in the eat functions -- something we are doing to emulate the MATLAB results
        num_rabbit_eaten = 0
        for agent in env.agents:
            if isinstance(agent,rabbit) and agent.has_been_eaten and not agent.dead:
                num_rabbit_eaten = num_rabbit_eaten + 1
        # Remove eaten and dead from the list of agents
        env.agents = ([a for a in env.agents if not a.dead and
                      not a.has_been_eaten])

        # The Dead are automatically accounted for in the .die() functions
        # Only need to decrement total number of eaten rabbits
        rabbit.num_rabbits = rabbit.num_rabbits - num_rabbit_eaten

    if env.mode == 'async':
        # Apply rules
        for agent in env.agents:
            eaten = agent.eat(env)

            # If the agent hasn't eaten, migrate
            if not eaten:
                agent.migrate(env)

            # Apply the death rule - from starvation or old age
            agent.die(env)
                
            # If the agent did not die, apply the breed rule
            if not agent.dead:
                new = agent.breed(env)
                if new is not None:
                    new_agents.append(new)
                    
        # Add new agents to list
        env.agents.extend(new_agents)
        
        # Clean up the dead
        env.agents = ([a for a in env.agents if not a.dead and
                      not a.has_been_eaten])


def ecolab(size, nr, nf, steps,mode='sync'):
    """ecolab - Python version of the original MATLAB code by Dawn Walker.
    Python version by Mike Croucher.

    Parameters
    ----------

    size : integer
        The length of one side of the square of the environment in which the
        agents live.

    nr: integer
        Initial Number of rabbits

    nf: integer
        Initial number of foxes

    steps: integer
        Number of simulation steps

    mode: string (default='sync')
        Simulation mode, either 'sync' or 'async'
        'sync' - Agents use information on previous iteration on which to 
        base their decisions. This gives the same results as MATLAB. 
        Some unphysical events can occur such as a dead rabbit giving birth

        'async' - Agents always use the most up to date information on which
        to base their decsisons. 

    """
    env = environment.environment(size, mode)
    env.create_agents(nr, nf, 'joined')

    history = np.zeros((2, steps))

    for n_it in range(steps):
        history[0, n_it] = rabbit.num_rabbits
        history[1, n_it] = fox.num_foxes

        agent_solve(env)

    return(env.agents,env,history)