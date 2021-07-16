from setuptools import find_packages, setup  # type: ignore

REQUIREMENTS = [
    "pygithub",
]

DEPLOY_DEPS = [
    # Used to zip up the code
    "wheel",
]

EXTRAS = {
    "deploy": DEPLOY_DEPS
}

setup(
    name="KeepActionsAlive",
    version="0.0.1",
    description="Re-enables Github Workflows disabled due to inactivity",
    author="Invenia Technical Computing",
    url="https://github.com/invenia/KeepActionsAlive",
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    include_package_data=True,
    extras_require=EXTRAS,
)
