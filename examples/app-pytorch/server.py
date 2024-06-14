from logging import INFO
import os
from typing import List, Tuple

from flwr.server import ServerApp, ServerConfig
from flwr.server.strategy import FedAvg
from flwr.common import Metrics, ndarrays_to_parameters
from flwr.common.logger import log

from task import Net, get_weights


# Define metric aggregation function
def weighted_average(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    examples = [num_examples for num_examples, _ in metrics]

    # Multiply accuracy of each client by number of examples used
    train_losses = [num_examples * m["train_loss"] for num_examples, m in metrics]
    train_accuracies = [
        num_examples * m["train_accuracy"] for num_examples, m in metrics
    ]
    val_losses = [num_examples * m["val_loss"] for num_examples, m in metrics]
    val_accuracies = [num_examples * m["val_accuracy"] for num_examples, m in metrics]

    # Aggregate and return custom metric (weighted average)
    return {
        "train_loss": sum(train_losses) / sum(examples),
        "train_accuracy": sum(train_accuracies) / sum(examples),
        "val_loss": sum(val_losses) / sum(examples),
        "val_accuracy": sum(val_accuracies) / sum(examples),
    }


# Initialize model parameters
ndarrays = get_weights(Net())
parameters = ndarrays_to_parameters(ndarrays)

env_var_num_rounds = int(os.environ['HOKEUN_FLWR_NUM_ROUNDS'])
log(INFO, "Hokeun! env_var_num_rounds: %i", env_var_num_rounds)

env_var_noise_enabled = False
if 'HOKEUN_FLWR_NOISE_ENABLED' in os.environ and int(os.environ['HOKEUN_FLWR_NOISE_ENABLED']) != 0:
    env_var_noise_enabled = True

log(INFO, "Hokeun! env_var_noise_enabled: %r", env_var_noise_enabled)

env_var_gauss_noise_sigma = 0.0
if env_var_noise_enabled:
    env_var_gauss_noise_sigma = float(os.environ['HOKEUN_FLWR_GAUSS_NOISE_SIGMA'])
    log(INFO, "Hokeun! env_var_gauss_noise_sigma: %r", env_var_gauss_noise_sigma)



# Define strategy
strategy = FedAvg(
    fraction_fit=1.0,  # Select all available clients
    fraction_evaluate=0.0,  # Disable evaluation
    min_available_clients=2,
    fit_metrics_aggregation_fn=weighted_average,
    initial_parameters=parameters,
    noise_enabled=env_var_noise_enabled,
    gauss_noise_sigma=env_var_gauss_noise_sigma,
    # inplace=False,  # Hokeun! set inplace false
)


# Define config
config = ServerConfig(num_rounds=env_var_num_rounds)


# Flower ServerApp
app = ServerApp(
    config=config,
    strategy=strategy,
)


# Legacy mode
if __name__ == "__main__":
    from flwr.server import start_server

    start_server(
        server_address="0.0.0.0:8080",
        config=config,
        strategy=strategy,
    )
