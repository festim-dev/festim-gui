FROM kitware/trame:conda

# Set Python and Vue versions
ENV TRAME_PYTHON=3.12
ENV TRAME_CLIENT_TYPE=vue3

# Install ParaView (with ADIOS2 support)
ARG PV_URL=https://www.paraview.org/files/v6.1/ParaView-6.1.1-MPI-Linux-Python3.12-x86_64.tar.gz
RUN mkdir -p /opt/paraview && cd /opt/paraview && wget -qO- $PV_URL | tar --strip-components=1 -xzv
ENV TRAME_PARAVIEW=/opt/paraview

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpciaccess0 \
    libgl1 \
    libegl1 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    libxkbcommon-x11-0 \
    libdbus-1-3 \
 && rm -rf /var/lib/apt/lists/*

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
