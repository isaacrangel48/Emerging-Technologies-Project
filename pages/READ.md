# Randomness Lab

Randomness Lab is an interactive Streamlit website that demonstrates how randomness affects artificial intelligence and machine learning.

The project includes experiments involving:

- Temperature in language-model generation
- Random seeds and reproducibility
- Random weight initialization in a neural network
- Random number generation

The language-model experiments use Qwen 3.5 through Ollama.


How to Run the Application
1. Clone the Repository

Open PowerShell and run:

git clone https://github.com/isaacrangel48/Emerging-Technologies-Project.git

1. Clone the Repository

Open PowerShell and run:

git clone https://github.com/isaacrangel48/Emerging-Technologies-Project.git

Move into the project folder:

cd Emerging-Technologies-Project
2. Create a Virtual Environment
python -m venv venv


3. Activate the Virtual Environment on Windows
.\venv\Scripts\Activate.ps1

After activation, the PowerShell prompt should begin with:

(venv)
4. Install the Required Python Packages
pip install streamlit ollama scikit-learn pandas
5. Install Ollama

Ollama must be installed locally before running the language-model experiments.

After installing Ollama, download the Qwen 3.5 model:

ollama pull qwen3.5

You can confirm that the model is installed with:

ollama list

The list should include Qwen 3.5.

6. Run the Application

Start the Streamlit website with:

streamlit run Intro.py

Once Streamlit starts, the application should automatically open in a web browser.