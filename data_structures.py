from typing import List

class EvolutionUnit:
    def __init__(self, T, M, P, fitness=0.0, history=None):
        self.T = T  # Thinking style
        self.M = M  # Mutation prompt
        self.P = P  # Task prompt
        self.fitness = fitness  # Estimated fitness
        self.history = history if history is not None else []  # Historical prompts

    def __repr__(self):
        return (
                f"EvolutionUnit(\n"
                f"    T={self.T!r},\n"
                f"    M={self.M!r},\n"
                f"    P={self.P!r},\n"
                f"    fitness={self.fitness:.2f},\n"
            )

class Population:
    def __init__(self, size, age, problem_description, units=None, elites=None):
        self.size = size
        self.age = age
        self.problem_description = problem_description
        self.units = units if units is not None else []  # List of individuals
        self.elites = elites if elites is not None else []  # Best-performing individuals

    def __repr__(self):
        units_str = ',\n    '.join(repr(unit) for unit in self.units)
        return (
            f"Population(\n"
            f"    size={self.size},\n"
            f"    age={self.age},\n"
            f"    problem_description={self.problem_description!r},\n"
            f"    units=[\n    {units_str}\n    ]\n)"
        )