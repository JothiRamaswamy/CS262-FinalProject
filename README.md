## Prerequisites
This code requires Python 3.x to run. Additionally, the `grpc`, `openai`, `pyyaml`, `skypilot`, `torch`, `numpy`, `seaborn`, and `matplotlib` libraries must be installed.

Additionally, you must have Google Cloud Platform and AWS configured on your computer before running this code. This is necessary in order to run Skypilot and obtain metadata surrounding the files we run on both of these platforms (Skypilot must also be configured on your computer). Lastly, you must have access to OpenAI APIs that can access GPT4 based models, which we leverage for our code that identifies GPU/CPU heavy tasks in our scripts.

## Configure Google Cloud Platform

You can get access to Google Cloud Platform and configure it on your computer by following instructions in the following link: https://cloud.google.com/sdk/gcloud

## Configure AWS

You can get access to AWS and configure it on your computer by following instructions in the following link: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html

## Configure SkyPilot

You can get access to Skypilot and configure it on your computer by following instructions in the following link: https://skypilot.readthedocs.io/en/latest/getting-started/installation.html

## Set up OpenAI

You can get access to GPT4 models on OpenAI by following instructions in the following links https://openai.com/product/gpt-4
https://platform.openai.com/overview
https://platform.openai.com/docs/api-reference

## Running the code
Clone this current repository and open a terminal or command prompt and navigate to the directory containing the code file.
Run the command 
```
python3 start.py client
``` 
to execute the client side program. To execute the interoperability layer(s), which we treat as "servers" in relation to the client above, run the following command up to 3 times
```
python3 start.py server
``` 
This code also requires that on your local server, ports 3001-3003 are available for use. This code currently leverages localhost, but can also be replaced by any available IPv4 address.

## Running the tests

The `tests.py` file includes a series of unit tests that confirm that many of the functions in the above files work correctly.

To run the tests, first run the following lines of code:

```
python3 -m venv env
source ./env/bin/activate
python3 -m pip install pytest
python3 -m pip install grpcio
python3 -m pip install grpcio-tools
pip install pyyaml
pip install openai
```
Now run
```
pytest tests.py
```

## Stopping the program
To stop the program in the middle, press Ctrl-C in the terminal. The program will catch the `KeyboardInterrupt` exception and terminate gracefully in both the client and server interfaces.