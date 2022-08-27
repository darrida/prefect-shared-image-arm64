import os
import sys
import subprocess
import click
import tomli


with open('pyproject.toml', 'rb') as f:
    config = tomli.load(f)
name = config["tool"]["poetry"]["name"]
version = config["tool"]["poetry"]["version"]
registry = config["tool"]["docker"]["registry"] 


image = f"{registry}/{name}:{version}"


@click.group()
def cli():
    """Prefect Shared Image Build and Push
    """


@cli.command('build')
def build():
    if input(f"Confirm image name: {image} (y/n): ") == 'y':
        cmd = f"docker build . -t {image}"
        print(f"RUNNING: {cmd}")
        os.system(cmd)
    else:
        print("Docker build cancelled.")


@cli.command('push')
def push():
    cmd = f"docker push {image}"
    if input(f"Confirm image name: {image} (y/n): ") != 'y':
        print("Docker push canceled.")
        return
    print("Checking existing image.")
    try:
        result = subprocess.check_output(f"docker manifest inspect {image}", shell=True, stderr=subprocess.STDOUT)
        if "no such manifest" not in str(result):
            if input("WARNING: Image of supplied name:tag exists in registry. Are you sure you want to *overwrite* that image? (y/n): ") == 'y':
                print(f"RUNNING: {cmd}")
                os.system(cmd)
            else:
                print("Docker push cancelled") 
    except subprocess.CalledProcessError:
        print(f"RUNNING: {cmd}")
        os.system(cmd)
        
        
if __name__ == '__main__':
    cli()  