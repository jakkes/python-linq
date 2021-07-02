from uuid import uuid4
from argparse import ArgumentParser
from subprocess import run


parser = ArgumentParser(
    description="Executes the tests using limited CPU power. Requires Docker to be "
    "installed and in your PATH."
)
parser.add_argument(
    "-p",
    "--processes",
    type=int,
    default=1,
    help="Number of processes allocated to the docker container.",
)


def main(args):
    image_name = str(uuid4())
    run(f"docker build -f docker/Dockerfile . -t {image_name}", check=True, shell=True)
    try:
        run(
            f"docker run -it --rm --cpus={args.processes} {image_name} pytest",
            shell=True,
            check=True,
        )
    finally:
        run(f"docker rmi {image_name}", shell=True, check=True)

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
