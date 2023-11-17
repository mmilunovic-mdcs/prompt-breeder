# Prompt Breeder Genetic Algorithm 🧬🤖

This project implements a genetic algorithm inspired by the concepts presented in the research paper ["Prompt-Based Evolution of Large Language Models"](https://arxiv.org/pdf/2309.16797.pdf).
The algorithm evolves a population of prompt strategies to interact effectively with Large Language Models (LLMs), aiming to improve the quality of prompts over successive generations.

## Installation Instructions 🛠️

To set up this project, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repository/prompt-breeder.git
   cd prompt-breeder
   ```

2. **Install Dependencies:**
   - Ensure you have Python 3.x installed.
   - Install required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

3. **Set Up OpenAI API Key:**
- Obtain an API key from [OpenAI](https://beta.openai.com/signup/).
- Set the API key as an environment variable:
   ```bash
   export OPENAI_API_KEY='your-api-key'
   ```
- For Windows, set the environment variable in the System Properties.

## Usage Instructions 🚀

To run the genetic algorithm:

1. **Run the script using Python, optionally passing command-line arguments:**
   ```bash
   python main.py --num_thinking_styles 2 --num_mutation_prompts 2 --problem_statement "Your problem statement here"
   ```
- You can use command-line arguments to override configurations. For details, use:
   ```bash
   python main.py --help
   ```
2. **Monitor Output:**
- The script will log the progress of the algorithm, including fitness evaluations and mutations applied to the prompts.

3. **Review Results:**
- Check the output for the evolution of prompts and the performance of the population across generations.


## Future Enhancements and To-Do List 📝

- [ ] Implement crossover mechanisms for prompt evolution.
- [ ] Introduce additional mutation strategies for diverse prompt exploration.
- [ ] Add functionality to visualize the evolution of prompts over time.
- [ ] Improve fitness evaluation.
- [ ] Explore different LLMs and compare performance.
