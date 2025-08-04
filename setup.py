from setuptools import setup, find_packages

setup(
    name="caricom_survey",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-api-python-client",
        "oauth2client",
        "python-dotenv",
        "pandas"
    ],
    entry_points={
        "console_scripts": [
            "caricom-survey=main:main"
        ]
    },
    include_package_data=True,
    description="Automated survey distribution tool for CARICOM central banks",
    author="Brian Langrin",
    author_email="brianlangrin@gmail.com"
)
