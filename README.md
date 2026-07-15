# search-engine-from-scratch
Search engine implementation from scratch using Python


## Running the project
Before installing the project locally, make sure you have **Python 3.13+** and [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

To install the project, follow these steps:

1. Create a new virtual environment:

   ```
   uv venv venv --python 3.13
   ```

1. Activate the Python environment:

   ```
   source venv/bin/activate
   ```

1. Install the project dependencies:

   ```
   uv sync
   ```

1. Install the project locally:

   ```
   uv pip install -e .
   ```

### Running the search engine
Add instructions to run the search engine


### Using the venv in VS CODE

If you are modifying the project using VS CODE then create the file `.vscode/settings.json` with the following lines:

   ```
  {
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true
  }
   ```