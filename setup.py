{
  "name": "minecraft-launcher-pro",
  "version": "1.0.0",
  "description": "Professional Minecraft launcher with Microsoft authentication, instances, mods, and modern UI",
  "author": "LauncherPro Team",
  "license": "MIT",
  "main": "run.py",
  "scripts": {
    "start": "python run.py",
    "dev": "python -m launcher.main --debug",
    "test": "pytest tests/"
  },
  "dependencies": {
    "requests": ">=2.25.1",
    "pillow": ">=8.0.0"
  },
  "devDependencies": {
    "pytest": ">=6.0.0",
    "pytest-cov": ">=2.10.0"
  },
  "keywords": ["minecraft", "launcher", "game", "microsoft", "authentication"],
  "classifiers": [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Games/Entertainment"
  ],
  "python_requires": ">=3.8"
}