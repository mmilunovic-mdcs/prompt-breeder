import argparse
from typing import List
import os
import openai
from rich import print

from data_structures import EvolutionUnit, Population
from gsm8k_utils import gsm_extract_answer, read_jsonl, check_answer_in_response
from mutations import mutate
from prompts import MUTATION_PROMPTS, THINKING_STYLES

from rich.console import Console
from rich.traceback import install
from rich.logging import RichHandler
import logging
import random

# Setup rich logging
install()
console = Console()
logging.basicConfig(level="INFO", format="%(message)s", handlers=[RichHandler(console=console)])


def create_population(tp_set: List[str], mutator_set: List[str], problem_description: str) -> Population:
    """Creates a population based on the provided sets of thinking styles and mutation prompts."""
    units = [EvolutionUnit(T=t, M=m, P='', fitness=0, history=[]) 
             for t in tp_set for m in mutator_set]
    return Population(size=len(units), age=0, problem_description=problem_description, units=units)


def init_run(population: Population, gsm8k_examples: List[dict], num_evals: int) -> Population:

    # Generate initial task prompts
    for unit in population.units:
        prompt = f"{unit.T} {unit.M} INSTRUCTION: {population.problem_description} INSTRUCTION MUTANT = "
        response = openai.Completion.create(model="gpt-3.5-turbo-instruct", prompt=prompt, max_tokens=1000)
        unit.P = response.choices[0].text.strip()

    # Evaluate fitness of each unit
    evaluate_fitness(population, gsm8k_examples, num_evals)

    return population

def evaluate_fitness(population: Population, gsm8k_examples: List[dict], num_evals: int) -> Population:
    elite_fitness = -1
    current_elite = None

    examples = random.sample(gsm8k_examples, num_evals)

    for unit in population.units:
        unit.fitness = 0

        for example in examples:
            prompt = unit.P + " " + example['question']
            response = openai.Completion.create(model="gpt-3.5-turbo-instruct", prompt=prompt, max_tokens=1000)
            model_answer = response.choices[0].text.strip()
            correct_answer = gsm_extract_answer(example['answer'])

            # Logging the comparison
            # console.print(f"[bold magenta]Prompt Given:[/bold magenta] {prompt}", style="magenta")
            console.print(f"[bold cyan]LLM's Answer:[/bold cyan] {model_answer[-500:]}", style="cyan")
            console.print(f"[bold red]Actual Answer:[/bold red] {correct_answer}", style="red")

            if check_answer_in_response(model_answer, correct_answer):
                console.print("Correct!", style="green")
                unit.fitness += 1 / num_evals
            else:
                console.print("Incorrect!", style="red")

        if unit.fitness > elite_fitness:
            elite_fitness = unit.fitness
            current_elite = unit

    # Update the elite list
    if current_elite:
        population.elites.append(current_elite)

    return population

def run_for_n(n: int, population: Population, gsm8k_examples: List[dict], num_evals:int) -> Population:
    for generation in range(n):
        print(f"[bold green]Running Generation {generation}[/bold green]")

        # Apply mutations to the population
        mutate(population)

        # Evaluate fitness of each unit
        evaluate_fitness(population, gsm8k_examples, num_evals)

        max_fitness = max(unit.fitness for unit in population.units)
        print(f"[bold blue]Generation {generation} Summary:[/bold blue] Max Fitness: {max_fitness:.2f}")


    return population

# Main function to run the prompt breeder
def main(args):
    logger = logging.getLogger("Prompt Breeder")
    # Extract the command-line arguments
    num_thinking_styles = args.num_thinking_styles
    num_mutation_prompts = args.num_mutation_prompts
    problem_statement = args.problem_statement

    # Select the specified number of thinking styles and mutation prompts
    thinking_styles = random.sample(THINKING_STYLES, num_thinking_styles)
    mutation_prompts = random.sample(MUTATION_PROMPTS, num_mutation_prompts)

    # Create the initial population
    logger.info("Creating the initial population")
    population = create_population(mutation_prompts, thinking_styles, problem_statement)
    print(population)

    gsm8k_dataset = read_jsonl("./gsm8k_sampled.jsonl")
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # Initialize and evaluate fitness of the initial population
    init_run(population, gsm8k_dataset, args.num_evals)

    # Run the simulation for n generations
    logger.info("Running the simulation")
    final_population = run_for_n(args.simulations, population, gsm8k_dataset, args.num_evals)
    print(final_population)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Prompt Breeder Algorithm.")
    parser.add_argument('-ts', '--num_thinking_styles', type=int, default=2, help="Number of thinking styles to use.")
    parser.add_argument('-mp', '--num_mutation_prompts', type=int, default=2, help="Number of mutation prompts to use.")
    parser.add_argument('-p', '--problem_statement', type=str, default="Solve the math word problem, giving your answer as an arabic numeral.")
    parser.add_argument('-e', '--num_evals', type=int, default=10, help="Number of evaluations for each unit.")
    parser.add_argument('-n', '--simulations', type=int, default=5, help="Number of generations/simulations to run.")

    args = parser.parse_args()
    main(args)
