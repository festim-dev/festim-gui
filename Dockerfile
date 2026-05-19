FROM kitware/trame:conda

# Set Python and Vue versions
ENV TRAME_PYTHON=3.12
ENV TRAME_CLIENT_TYPE=vue3

# -------------------------------------------------------------------
# !!! Using path from root directory !!!
# -------------------------------------------------------------------
# Copy the local app and the deploy directory when using local
# directory (./setup/initialize.sh) instead of
# a published package (./setup/requirements.txt)
# => use one or the other
COPY --chown=trame-user:trame-user . /local-app
COPY --chown=trame-user:trame-user ./setup /deploy/setup
# -------------------------------------------------------------------

RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main \
    && conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r \
    && gosu trame-user conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main \
    && gosu trame-user conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r \
    && /opt/trame/entrypoint.sh build
