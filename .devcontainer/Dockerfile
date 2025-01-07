# [Choice] Python version (via pyenv): 3
# Look in common-debian.sh for other apt-get commands to "build" your image
# https://github.com/microsoft/vscode-dev-containers/tree/main/script-library/docs
FROM mcr.microsoft.com/devcontainers/python:0-3.10-bullseye

# [Option] Install Node.js
ARG INSTALL_NODE="false"
ARG NODE_VERSION="lts/*"

# [Option] Install GitHub CLI
ARG INSTALL_GITHUB_CLI="true"

# [Option] Upgrade pip / setuptools / wheel
ARG UPGRADE_PIP_PACKAGES="true"

# Install apt-utils and dialog to avoid debconf warnings
RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1

# Install Git, process tools, lsb-release (common in install scripts).
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        git \
        wget \
        curl \
        ca-certificates \
        less \
    #
    # Install lsb-release & dependency for adding apt repos
    && apt-get -y install --no-install-recommends lsb-release gnupg apt-transport-https dirmngr

# Install Node.js
COPY library-scripts/node-debian.sh /tmp/library-scripts/
RUN if [ "${INSTALL_NODE}" = "true" ]; then /bin/bash /tmp/library-scripts/node-debian.sh "${NODE_VERSION}"; fi

# Install GitHub CLI
COPY library-scripts/github-debian.sh /tmp/library-scripts/
RUN if [ "${INSTALL_GITHUB_CLI}" = "true" ]; then /bin/bash /tmp/library-scripts/github-debian.sh; fi

# Upgrade pip / setuptools / wheel
COPY library-scripts/python-debian.sh /tmp/library-scripts/
RUN if [ "${UPGRADE_PIP_PACKAGES}" = "true" ]; then /bin/bash /tmp/library-scripts/python-debian.sh; fi

# Clean up
RUN apt-get autoremove -y && apt-get clean -y

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog

# Set pip options via environment variable to persist across multiple pip installs
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_COLOR=1 \
    PIP_NO_INPUT=1

# Install Python packages from requirements.txt
COPY requirements.txt /tmp/requirements.txt
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/requirements.txt
