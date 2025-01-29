from setuptools import setup, find_packages

setup(
    name='pyms',
    version='0.0',
    author='何乐',
    author_email='hele199380@hotmail.com',
    description='',
    long_description='',
    long_description_content_type='',
    url='https://github.com/1649hele/pyns',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pygame',
        'pyqt5',
        'requests',
        'numpy',
        'sympy',
        'quaternion',
        'pyautogui',
        'opencv-python',
        'pillow',
        'pdfdocx',
        'pyaudio',
        'librosa',
        'weasyprint',
        'pyttsx3',
        'watchdog',
    ],
)

