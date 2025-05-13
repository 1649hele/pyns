from setuptools import setup, find_packages

setup(
    name='pyms',
    version='0.0',
    author='何乐',
    author_email='hele199380@hotmail.com',
    description='',
    long_description='',
    long_description_content_type='',
    url='https://github.com/1649hele/pyms',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
    """
    deepl==1.22.0
    easygui==0.98.3
    graphviz==0.20.3
    librosa==0.11.0
    numpy==2.2.6
    opencv_python==4.11.0.86
    pdf2docx==0.5.8
    Pillow==11.2.1
    playwright==1.52.0
    PyAudio==0.2.14
    PyAutoGUI==0.9.54
    pydub==0.25.1
    pygame==2.6.1
    pygamephysics==0.0.1
    pystray==0.19.5
    pyttsx3==2.98
    Requests==2.32.3
    setuptools==80.9.0
    soundfile==0.13.1
    weasyprint==65.1
    """,
    ],
)

