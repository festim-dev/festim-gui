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

The Run page can execute the generated FESTIM script in the current Python
environment.

When running inside the provided Docker image, ``festim`` is installed as part
of the image build.

When running ``festim-gui`` outside the Docker container, the same assumption
still applies: the Python environment used to launch ``festim-gui`` must also
have ``festim`` installed, since the Run page executes the generated script in
that same environment.

Simulation working directories are created under ``FESTIM_GUI_TMP`` when that
environment variable is set. If it is not set, the application falls back to
``/tmp``.

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

To persist simulation run directories outside the container, set
``FESTIM_GUI_TMP`` and bind-mount it:

.. code-block:: console

    mkdir -p ./festim-runs
    docker run -it --rm \
        -p 8080:80 \
        -e FESTIM_GUI_TMP=/data/festim-runs \
        -v $(pwd)/festim-runs:/data/festim-runs \
        festim-gui

Docker setup files are located under ``setup/``.

Professional Support
----------------------------------------

* `Training <https://www.kitware.com/courses/trame/>`_: Learn how to confidently use trame from the expert developers at Kitware.
* `Support <https://www.kitware.com/trame/support/>`_: Our experts can assist your team as you build your web application and establish in-house expertise.
* `Custom Development <https://www.kitware.com/trame/support/>`_: Leverage Kitware’s 25+ years of experience to quickly build your web application.
