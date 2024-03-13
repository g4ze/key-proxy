from setuptools import setup, find_packages

with open("req.txt") as f:
    requirements = f.read().splitlines()
setup(
    name="key-proxy",
    version="2.0.0",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.7",
    py_modules=["script", "src/key_proxy_gui", "src/starter", "src/typer"],
    entry_points="""
     [console_scripts]
     key-proxy=script:hello
     """,
)
