# Container image for vem-project. See guidance/containers.md.
#
#   docker build -t vem-project .
#   docker run --rm -v /path/to/data:/data vem-project measure /data/params.yml
#
# Official slim Python image: small, maintained, and matches a supported
# Python version. Use a CUDA base image instead if you add GPU code.
ARG PYTHON_IMAGE=python:3.13-slim

# Build stage: builds the wheel, so build tools stay out of the final image.
FROM ${PYTHON_IMAGE} AS build
WORKDIR /src
COPY . .
RUN pip install --no-cache-dir build && python -m build --wheel --outdir /dist

FROM ${PYTHON_IMAGE}
ARG VERSION=unknown
ARG REVISION=unknown
LABEL org.opencontainers.image.title="vem-project" \
      org.opencontainers.image.description="One-line description of what this tool does for volume EM / CLEM data." \
      org.opencontainers.image.source="https://github.com/ccp-volume-em/vem-project" \
      org.opencontainers.image.licenses="BSD-3-Clause" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.revision="${REVISION}"

# Installing the wheel (not copying source) keeps version metadata and the
# vem-project command working. For a reproducible image, pin the direct
# dependencies with a constraints file: pip install -c constraints.txt ...
COPY --from=build /dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm /tmp/*.whl

# Run as a non-root user. Mount data at /data; outputs are written wherever
# the parameter file says, so that folder must be writable by this user
# (add --user "$(id -u):$(id -g)" to docker run to match your own user).
RUN useradd --create-home --uid 1000 vem
USER vem
WORKDIR /data

ENTRYPOINT ["vem-project"]
CMD ["--help"]
