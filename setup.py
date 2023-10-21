import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# The requirements file
with open('requirements.txt') as f:
    required = f.read().splitlines()

# This call to setup() does all the work
setup(
    name="rtlsdr_nfs32002",
    version="0.3",
    description="Réimplémentation du protocole NF S 32002 utilisé par les balises sonores des feux piétons. Permet de détecter le signal d'une télécommande à partir d'un RTL SDR.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/balises-ouistici/rtlsdr_nfs32002",
    author="Jérémy Kalsron ; Samuel Braikeh <samuel.braikeh@yahoo.fr>",
    author_email="jeremy.kalsron@gmail.com",
    license="AGPL-3.0",
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=required,
    packages=["rtlsdr_nfs32002"],
    include_package_data=True,
)

