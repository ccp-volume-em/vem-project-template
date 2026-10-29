# Containers

From the guide: [Making software public → Containerisation](https://ccp-volume-em.github.io/guide/software_publishing/#containerisation)
and [Container Testing](https://ccp-volume-em.github.io/guide/container_testing/).

A container image bundles the interpreter, libraries, system packages and
configuration, so users get the same environment as the developers. This
matters for volume EM tools, which often combine Python packages, compiled
libraries, GPU frameworks and command-line tools. Containers complement a
PyPI or conda package; they don't replace it. Introduction:
[Using Containers](https://rosalindfranklininstitute.github.io/volume-em-container-documentation/intro/containers/).

## Writing the `Dockerfile`

- Keep it in the repository, so it's versioned and reviewed with the code.
  Build from a release or a specific commit, not uncommitted local files.
- Start from a minimal, maintained base image (e.g. official Python or CUDA)
  and record why you chose it.
- Pin the versions of the dependencies your application directly relies on.
  Leave auxiliary system and build packages unpinned (pinning everything
  causes security and build problems over time). For exact binary
  reproducibility, archive the image (e.g. on Zenodo).
- Install the software as a package (`pip install .`), not by copying source
  files, so version metadata and entry points work.
- Use multi-stage builds to keep build tools out of the final image; remove
  package-manager caches in the same layer.
- Run as a non-root user, and document any writable directories needed.
- Set an `ENTRYPOINT` so `docker run <image> --help` works.
- Add [OCI labels](https://github.com/opencontainers/image-spec/blob/main/annotations.md):
  `org.opencontainers.image.source`, `.version`, `.revision`, `.licenses`,
  `.description`.
- Keep large data, model weights and test data out of the image; download or
  mount them at run time.
- GUI apps (e.g. napari) need a display: the host X11 socket with `DISPLAY`
  set and display drivers mounted, or a browser-based server such as Xpra.
  See the [RFI vEM container docs](https://rosalindfranklininstitute.github.io/volume-em-container-documentation/).

## Testing in CI

- Build on pull requests and release tags, and check the image starts and
  reports its version.
- Rebuild when the container definition or dependencies change, and on a
  schedule to catch upstream breakage.
- Run the test suite inside the image (with `Xvfb` for GUIs).
- Add start-up checks to the entrypoint that **warn** when something is
  missing (display, GPU, writable mount). See [testing.md](testing.md).
- Build and test each architecture you support (e.g. `amd64`, `arm64`).

## Tagging and publishing

- Publish to a registry your users already use (Docker Hub, Quay.io, GitHub
  Container Registry). Consider rate limits, retention and longevity.
- Tags follow release versions: an immutable `v1.2.0` matching the git tag,
  never moved; optional moving tags `v1.2`, `v1`, `latest`; variant suffixes
  such as `v1.2.0-cuda`, `v1.2.0-xpra`.
- Publish from the same tag as the GitHub Release, and record the version in
  the labels. Generate build provenance and an SBOM where supported.
- Publish from CI with OpenID Connect or short-lived credentials, not stored
  passwords, restricted to protected tags or environments.

## Documenting how to run it

Give a complete command users can copy, and explain every non-obvious option:

```bash
docker pull ghcr.io/your-org/your-tool:1.2.0
docker run --rm -v /path/to/data:/data ghcr.io/your-org/your-tool:1.2.0 --help
```

Document: data mount paths; GPU access (`--gpus all`, driver/CUDA versions);
GUI display settings; file ownership (`--user $(id -u):$(id -g)`); memory,
shared memory and disk needs for large volumes.

## HPC and archiving

- HPC clusters usually have [Apptainer](https://apptainer.org/) (formerly
  Singularity) rather than Docker. It can run published OCI images:

  ```bash
  apptainer pull your-tool_1.2.0.sif docker://ghcr.io/your-org/your-tool:1.2.0
  apptainer run --bind /path/to/data:/data your-tool_1.2.0.sif --help
  ```

  Test this route: bind mounts, home directory, environment and user differ
  from Docker.
- For long-term reproducibility, reference images by digest
  (`your-tool@sha256:<digest>`), and record the digest in the methods.
- Registries aren't archives: deposit the container definition, resolved
  dependency versions and, if size allows, an exported image on Zenodo. A
  definition that rebuilds from pinned inputs often outlasts a stored image.
