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

For development, you can mount the source code into the container:

.. code-block:: console

    docker run -it --rm -p 8080:80 -v .:/local-app festim-gui

Then open ``http://localhost:8080/`` in your browser.

The Docker image includes ``festim``, so Run page executions work inside the
container without any extra local FESTIM installation.

Docker setup files are located under ``setup/``.

GPU support
----------------------------------------

The post-processing view can render either on the client or on the server:

* **Local rendering (default)** -- geometry is sent to the browser and rendered
  in browser. No GPU is needed on the server.
* **Remote rendering (GPU)** -- ParaView renders on the server and streams
  images to the browser. This requires a GPU available to the process, and is
  enabled with the ``--gpu`` flag.

The Docker image exposes both modes as separate apps, declared in
``setup/apps.yml``:

* ``http://localhost:8080/index.html`` -- default app, local rendering.
* ``http://localhost:8080/gpu.html`` -- same app launched with ``--gpu``,
  remote rendering.

Both apps are always served; ``gpu.html`` only works if the container can reach
a GPU.

Running the container with GPUs
========================================

Install the `NVIDIA Container Toolkit
<https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html>`_
on the host, then pass the GPUs to the container with ``--gpus``:

.. code-block:: console

    docker run -it --rm --gpus all -p 8080:80 festim-gui

Then open ``http://localhost:8080/gpu.html`` in your browser.


Professional Support
----------------------------------------

* `Training <https://www.kitware.com/courses/trame/>`_: Learn how to confidently use trame from the expert developers at Kitware.
* `Support <https://www.kitware.com/trame/support/>`_: Our experts can assist your team as you build your web application and establish in-house expertise.
* `Custom Development <https://www.kitware.com/trame/support/>`_: Leverage Kitware’s 25+ years of experience to quickly build your web application.
