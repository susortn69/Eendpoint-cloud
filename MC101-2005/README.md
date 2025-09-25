# Pre-requisites
## Conda
Venv => You can not choose the python version.
We use poetry for package management. Poetry builds up its package upon a virtual environment. We can use either of Venv or Conda. Conda give us the ability to choose the python version regardless of our default python. 
## Poetry
Before using poetry, ensure you have activated the intended python version either by using that or by using conda.
### Poetry commands
`poetry init`: Inits a poetry for the project
`poetry install`: Installs the poetry based on the initialized setup with `poetry init` command and updates the `poetry.lock` file.
`poetry update`: Updates the env if any package is added but not installed as well as updating the new compatible versions. 
`poetry add PACKAGE_NAME`: Adds a package
`poetry remove PACKAGE_NAME`: Removes a package
`poetry export -f requirements.txt --output requirements.txt --without-hashes`: Exports all packages with their versions into the requirements.txt file.

# Project: A Voting system

We are going to simulate a small voting system in which users can vote to their candidates after authentication.
This session is only about authentication.
