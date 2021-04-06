from setuptools import setup


def read_me(path):
    with open(path, "r", encoding="utf-8") as fp:
        return fp.read()


setup(
    name="T-flask",
    python_requires=">=3.7",
    version="1.0.0",
    author="SystemLight",
    author_email="1466335092@qq.com",
    maintainer="SystemLight",
    maintainer_email="1466335092@qq.com",
    url="https://github.com/SystemLight/T-flask",
    license="MIT",
    description="Flask project development template ",
    long_description=read_me("README.md"),
    long_description_content_type='text/markdown',
    download_url="https://codeload.github.com/SystemLight/T-flask/zip/refs/heads/master",
    install_requires="",
    platforms=["Windows", "Linux"],
    keywords=["flask", "template"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
    ],
    py_modules=[],
    scripts=[],
    entry_points={}
)
