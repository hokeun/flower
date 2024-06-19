# Flower App (PyTorch) 🧪

> 🧪 = This example covers experimental features that might change in future versions of Flower
> Please consult the regular PyTorch code examples ([quickstart](https://github.com/adap/flower/tree/main/examples/quickstart-pytorch), [advanced](https://github.com/adap/flower/tree/main/examples/advanced-pytorch)) to learn how to use Flower with PyTorch.

The following steps describe how to start a long-running Flower server (SuperLink) and then run a Flower App (consisting of a `ClientApp` and a `ServerApp`).

## Preconditions

Let's assume the following project structure:

```bash
$ tree .
.
├── client.py           # <-- contains `ClientApp`
├── server.py           # <-- contains `ServerApp`
├── server_workflow.py  # <-- contains `ServerApp` with workflow
├── server_custom.py    # <-- contains `ServerApp` with custom main function
├── task.py             # <-- task-specific code (model, data)
└── requirements.txt    # <-- dependencies
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run a simulation

```bash
flower-simulation --server-app server:app --client-app client:app --num-supernodes 2
```

## Run a deployment

### Start the long-running Flower server (SuperLink)

```bash
flower-superlink --insecure
```

### Start the long-running Flower client (SuperNode)

In a new terminal window, start the first long-running Flower client:

```bash
flower-client-app client:app --insecure
```

In yet another new terminal window, start the second long-running Flower client:

```bash
flower-client-app client:app --insecure
```

### Run the Flower App

With both the long-running server (SuperLink) and two clients (SuperNode) up and running, we can now run the actual Flower App:

```bash
flower-server-app server:app --insecure
```

Or, to try the workflow example, run:

```bash
flower-server-app server_workflow:app --insecure
```

Or, to try the custom server function example, run:

```bash
flower-server-app server_custom:app --insecure
```

## More customized commands for WPES paper experiments
```bash
HOKEUN_FLWR_NUM_ROUNDS=7 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 2'
```

To disable noise, assign 0 to `HOKEUN_FLWR_NOISE_ENABLED`:
```bash
HOKEUN_FLWR_NUM_ROUNDS=5 HOKEUN_FLWR_NOISE_ENABLED=0 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.1 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 3'
```

Example command with Gaussian noise:
```bash
HOKEUN_FLWR_NUM_ROUNDS=5 HOKEUN_FLWR_NOISE_ENABLED=1 HOKEUN_FLWR_GAUSS_NOISE_SIGMA=0.1 bash -c 'flower-simulation --server-app server:app --client-app client:app --num-supernodes 3'
```

## Using shell script

IMPORTANT! You must run `poetry shell` before running the shell script. For example:

```bash
poetry shell
./run_experiments.sh &
exit
```

After starting the script background using `%`, you can first `exit` to exit from poetry and check if the script still runs.

## Killing experiments script running in the background

Check out this page: [Killing a shell script running in background](https://unix.stackexchange.com/questions/174028/killing-a-shell-script-running-in-background).

Find the process ID of the script like this:

```
ps -aux | grep run_experiments*
```

Then, kill the process.
