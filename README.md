# PyDew Valley

PyDew Valley is a project originally created by ClearCode in Python using pygame-ce.

This expanded version will be used by the [University of Zurich's Department of Psychology](https://www.psychologie.uzh.ch/en.html) in an experimental study in social psychology. 

This particular repository covers the versions of the game used for a third study that is independent of [the first](https://github.com/sloukit/pydew-valley-uzh) and [the second study](https://github.com/sloukit/pydew-valley-uzh-second-study)

For more information, please contact s.kittelberger[at]psychologie.uzh.ch.

## Setup Instructions

This project requires Python 3.12. (Python 3.13 may cause issues, and free-threaded Python is **<ins>not</ins>** supported.)\
PyPy is also unsupported.

1. **Clone this repository:**
    ```bash
    git clone https://github.com/sloukit/pydew-valley-uzh-second-study.git
    ```

2. **Create and activate a virtual environment:**

    **Linux/MacOS**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    **For Windows**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt # For running the game (runtime dependencies)
    pip install -r requirements-dev.txt # For local development
    pip install -r requirements-test.txt # For running tests
    ```

4. Run this project
    ```bash
    python main.py
    ```

## Local Development

See [CONTRIBUTING.md](./CONTRIBUTING.md) for more information on how contributions can be made.

### Linting and Formatting

We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting. Run `pip install -r requirements-dev.txt` to install it and other relevant dependencies.

> [!IMPORTANT]
> **Before opening a PR, please run the following command to ensure that your code is formatted and doesn't upset the Ruff linter:**
> 
> ```sh
> python formatlint.py
> ```
> 
> Or alternatively, run the following commands individually:
> 
> ```sh
> ruff format . && ruff check --select I --fix . #  format code and sort imports
> ruff check . # Run linting and perform fixes accordingly, or use '# noqa: <RULE>' followed by a comment justifying why the rule is ignored
> ```

## Use of AI
We do not use AI for visual and design tasks.

## Relevant Links

- Project's Discord Server, https://discord.gg/SuthU2qKaZ
- Pygame Community's Discord Server, https://discord.gg/pygame
- ClearCode's Discord Server, https://discord.gg/Z2C3vnrxef
- Sprout Lands Assets, https://cupnooble.itch.io/sprout-lands-asset-pack
- ClearCode's Video Tutorial, https://www.youtube.com/watch?v=T4IX36sP_0c
