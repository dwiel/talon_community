from setuptools import setup
from setuptools.command.install import install as _install
from os import system


# add post-install command
class install(_install):
    def run(self):
        _install.run(self)
        system("pre-commit install")


def main():
    setup(
        name="taloncommunity",
        version="0.1",
        install_requires=["pre-commit", "black", "flake8"],
        cmdclass={"install": install},
    )


if __name__ == "__main__":
    main()
