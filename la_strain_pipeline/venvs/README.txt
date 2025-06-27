Dependencies and requirements for venvs are listed here.

Suffixed "-env" files contains the conda list --explicit output. Lists conda packages that make up the environment. 
To create an exact copy of this environment, use:

conda create --name myenv --file spec.txt

Suffixed "-requirement" files contain the pip freeze output. Lists packages installed using pip. Does not include non-Python dependencies covered by conda. 
To recreate, use:

pip install -r requirements.txt
