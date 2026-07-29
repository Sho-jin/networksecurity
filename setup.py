from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path: str) -> List[str]:
    """Read requirements from a file and return them as a list."""
    requirement_lst: List[str] = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            for line in lines:
                requirement = line.strip()

                if requirement and  requirement !='-e .':
                    requirement_lst.append(requirement)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")

    return requirement_lst

setup (
    name = "Network Security Project",
    version = "0.0.1",
    author = "Shobhit Jindal",
    author_email="sjindal3_be23@thapar.edu",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),

)

