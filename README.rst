festim-gui
----------------------------------------

GUI for FESTIM

License
----------------------------------------

This library is OpenSource and follow the MIT License

Installation
----------------------------------------

Install the application/library

.. code-block:: console

    pip install festim-gui

Run the application

.. code-block:: console

    festim-gui

Simulation runs
----------------------------------------

The Run page uses ``FESTIM_GUI_PYTHON`` to execute generated scripts, falling
back to the interpreter running ``festim-gui``. The Docker image configures
this variable automatically. Outside Docker, install ``festim`` in the active
environment or set the variable to an interpreter that provides it.

Simulation working directories are created under the system temporary
directory (e.g. ``/tmp``).

Each run gets its own temporary directory containing the generated script, a
``run.log`` file, and any simulation outputs written by the script.

Development setup
----------------------------------------

We recommend using uv for setting up and managing a virtual environment for your development.

.. code-block:: console

    # Create venv and install all dependencies
    uv sync --all-extras --dev

    # Activate environment
    source .venv/bin/activate

    # Install commit analysis
    pre-commit install
    pre-commit install --hook-type commit-msg




For running tests and checks, you can run ``nox``.

.. code-block:: console

    # run all
    nox

    # lint
    nox -s lint

    # tests
    nox -s tests

Docker
----------------------------------------

Build the Docker image from the repository root:

.. code-block:: console

    docker build -t festim-gui .

Run the image and expose it on port ``8080``:

.. code-block:: console

    docker run -it --rm -p 8080:80 festim-gui

Then open ``http://localhost:8080/`` in your browser.

The Docker image includes ``festim``, so Run page executions work inside the
container without any extra local FESTIM installation.

Docker setup files are located under ``setup/``.

Professional Support
----------------------------------------

* `Training <https://www.kitware.com/courses/trame/>`_: Learn how to confidently use trame from the expert developers at Kitware.
* `Support <https://www.kitware.com/trame/support/>`_: Our experts can assist your team as you build your web application and establish in-house expertise.
* `Custom Development <https://www.kitware.com/trame/support/>`_: Leverage Kitware’s 25+ years of experience to quickly build your web application.
