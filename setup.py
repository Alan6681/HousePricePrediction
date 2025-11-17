
"""
The setup.py file is used for packaging and distributing Python projects.
It defines metadata and dependencies using setuptools.
"""

from setuptools import setup, find_packages

def get_requirements() -> list:
    """Reads the requirements.txt file and returns a list of dependencies."""
    requirements_lst = []
    try:
        with open("requirements.txt", "r") as file:
            # Read each line of requirements file
            lines = file.readlines()

            for line in lines:
                requirement = line.strip()

                if requirement and not requirement.startswith("-e"):
                    requirements_lst.append(requirement)
        
    except FileNotFoundError:
        print("requirements.txt file not found.")  

    return requirements_lst
    

setup(
    name="HousePricePredictionProject",
    version="0.0.1",
    author="Alanabo Amaegbe",
    author_email="alanaboamaegbe@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)
                