# Copyright 2020 Flower Labs GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Aggregation functions for strategy implementations."""
# mypy: disallow_untyped_calls=False

from functools import reduce
from logging import INFO, ERROR
from typing import Any, Callable, List, Tuple

import numpy as np
import random
import copy
import sys
import math

from flwr.common import FitRes, NDArray, NDArrays, parameters_to_ndarrays
from flwr.common.logger import log
from flwr.server.client_proxy import ClientProxy


def aggregate(results: List[Tuple[NDArrays, int]]) -> NDArrays:
    """Compute weighted average."""
    log(INFO, 'Hokeun! aggregate: beginning')
    # Calculate the total number of examples used during training
    num_examples_total = sum(num_examples for (_, num_examples) in results)

    # Create a list of weights, each multiplied by the related number of examples
    weighted_weights = [
        [layer * num_examples for layer in weights] for weights, num_examples in results
    ]

    # Compute average weights of each layer
    weights_prime: NDArrays = [
        reduce(np.add, layer_updates) / num_examples_total
        for layer_updates in zip(*weighted_weights)
    ]
    return weights_prime

# Count the number of float32 numbers in multi-dimensional array recursively.
def hokeun_deep_count_float32(arrays: np.ndarray):
    if len(arrays) == 0:
        log(ERROR, "Hokeun! hokeun_deep_count_float32: len(arrays) is 0")
        sys.exit(1)
    if isinstance(arrays[0], np.ndarray):
        sum = 0
        for i in range(len(arrays)):
            sum += hokeun_deep_count_float32(arrays[i])
        return sum
    elif isinstance(arrays[0], np.float32):
        return len(arrays)
    else:
        log(ERROR, "Hokeun! hokeun_deep_count_float32: wrong type array element! %r", type(arrays[0]))
        sys.exit(1)


def hokeun_deep_diff_float32(array1: np.ndarray, array2: np.ndarray, indices: List[int], print_diff: bool):
    if len(array1) == 0:
        log(ERROR, "Hokeun! hokeun_deep_diff_float32: len(array1) is 0")
        sys.exit(1)
    if len(array2) == 0:
        log(ERROR, "Hokeun! hokeun_deep_diff_float32: len(array2) is 0")
        sys.exit(1)
    if len(array1) != len(array2):
        log(ERROR, "Hokeun! hokeun_deep_diff_float32: len(array1) != len(array2)")
        sys.exit(1)
    if type(array1) != type(array2):
        log(ERROR, "Hokeun! hokeun_deep_diff_float32: type(array1) != type(array2)")
        sys.exit(1)

    if isinstance(array1[0], np.ndarray):
        diff_count = 0
        for i in range(len(array1)):
            copy_of_indices = indices.copy()
            copy_of_indices.append(i)
            diff_count += hokeun_deep_diff_float32(array1[i], array2[i], copy_of_indices, print_diff)
        return diff_count
    elif isinstance(array1[0], np.float32):
        diff_count = 0
        for i in range(len(array1)):
            # if array1[i] != array2[i]:
            # Proper comparison of floating point numbers
            # Default rel_tol=1e-09
            if not math.isclose(array1[i], array2[i], rel_tol=1e-06):
                diff_count += 1
                copy_of_indices = indices.copy()
                copy_of_indices.append(i)
                if print_diff:
                    # Print each diff.
                    # Using .astype(str) to print with full precision.
                    log(INFO, "Hokeun! hokeun_deep_diff_float32: Found diff at %r, val1: %s, val2: %s, difference: %s",
                        copy_of_indices, array1[i].astype(str), array2[i].astype(str), (array1[i] - array2[i]).astype(str))
        return diff_count

    else:
        log(ERROR, "Hokeun! hokeun_deep_count_float32: wrong type array element! %r", type(array1[0]))
        sys.exit(1)



mult_count = 0
# Perform deep element-wise multiplication of float32 numbers in multi-dimensional array recursively.
def hokeun_perform_recursive_deep_multiplication(scaling_factor: float, params: np.ndarray, arrays: np.ndarray, noise_enabled: bool, gauss_noise_sigma: float):
    if len(params) == 0:
        log(ERROR, "Hokeun! hokeun_perform_recursive_deep_multiplication: len(params) is 0")
        sys.exit(1)
    if len(params) != len(arrays):
        log(ERROR, "Hokeun! hokeun_perform_recursive_deep_multiplication: len(params) != len(array)")
        sys.exit(1)

    if isinstance(params[0], np.ndarray):
        for i in range(len(params)):
            hokeun_perform_recursive_deep_multiplication(scaling_factor, params[i], arrays[i], noise_enabled, gauss_noise_sigma)
    elif isinstance(params[0], np.float32):
        for i in range(len(params)):
            noise_factor = 1.0
            if noise_enabled:
                noise_factor += random.gauss(0, gauss_noise_sigma)
            params[i] = params[i] + scaling_factor * arrays[i] * noise_factor
            global mult_count
            mult_count += 1
    else:
        log(ERROR, "Hokeun! hokeun_perform_recursive_deep_multiplication: wrong type array element! %r", type(params[0]))
        sys.exit(1)



def aggregate_inplace(results: List[Tuple[ClientProxy, FitRes]], noise_enabled: bool = False, gauss_noise_sigma: float = 0.0) -> NDArrays:
    """Compute in-place weighted average."""
    log(INFO, "Hokeun! aggregate_inplace: beginning")
    # Count total examples
    num_examples_total = sum(fit_res.num_examples for (_, fit_res) in results)

    # Compute scaling factors for each result
    scaling_factors = [
        fit_res.num_examples / num_examples_total for _, fit_res in results
    ]

    # Let's do in-place aggregation
    # Get first result, then add up each other
    params = [
        scaling_factors[0] * x for x in parameters_to_ndarrays(results[0][1].parameters)
    ]
    log(INFO, "Hokeun! aggregate_inplace: noise_enabled: %r", noise_enabled)
    log(INFO, "Hokeun! aggregate_inplace: gauss_noise_sigma: %r", gauss_noise_sigma)

    hokeun_params = copy.deepcopy(params)
    for i, (_, fit_res) in enumerate(results[1:]):
        noise_factor = 1.0
        if noise_enabled:
            noise_factor += random.gauss(0, gauss_noise_sigma)
            log(INFO, "Hokeun! noise_factor: %f", noise_factor)

        ndarrays = parameters_to_ndarrays(fit_res.parameters)
        log(INFO, "Hokeun! aggregate_inplace: len(ndarrays): %i", len(ndarrays))
        log(INFO, "Hokeun! aggregate_inplace: len(params): %i", len(params))
        log(INFO, "Hokeun! aggregate_inplace: len(hokeun_params): %i", len(hokeun_params))

        hokeun_perform_recursive_deep_multiplication(scaling_factors[i + 1], hokeun_params, ndarrays, noise_enabled, gauss_noise_sigma)

        log(INFO, "Hokeun! aggregate_inplace: mult_count: %i", mult_count)
        # for j in range(len(ndarrays)):
        #     # Element-wise add ndarrays[j] and params[j]
        #     log(INFO, "Hokeun! aggregate_inplace: len(ndarrays[%i]): %i", j, len(ndarrays[j]))
        #     log(INFO, "Hokeun! aggregate_inplace: len(params[%i]): %i", j, len(params[j]))
        #     log(INFO, "Hokeun! aggregate_inplace: len(hokeun_params[%i]): %i", j, len(hokeun_params[j]))
        #     for k in range(len(ndarrays[j])):
        #         # log(INFO, "Hokeun! aggregate_inplace: len(ndarrays[%i][%i]): %i", j, k, len(ndarrays[j][k]))
        #         hokeun_params[j][k] += scaling_factors[i + 1] * ndarrays[j][k] #* noise_factor


        res = (
            scaling_factors[i + 1] * x # * noise_factor
            # Giving 10% error.
            # scaling_factors[i + 1] * x * 1.1 
            for x in ndarrays
        )
        params = [reduce(np.add, layer_updates) for layer_updates in zip(params, res)]


        # log(INFO, "Hokeun! type(hokeun_params): %r", type(hokeun_params))
        # log(INFO, "Hokeun! type(params): %r", type(params))

        # log(INFO, "Hokeun! type(hokeun_params[0]): %r", type(hokeun_params[0]))
        # log(INFO, "Hokeun! type(params[0]): %r", type(params[0]))

        # log(INFO, "Hokeun! type(hokeun_params[0][0]): %r", type(hokeun_params[0][0]))
        # log(INFO, "Hokeun! type(params[0][0]): %r", type(params[0][0]))

        # log(INFO, "Hokeun! type(hokeun_params[0][0]): %r", str(hokeun_params[0][0]))
        # log(INFO, "Hokeun! type(params[0][0]): %r", str(params[0][0]))

        # log(INFO, "Hokeun! type(hokeun_params[0][0][0]): %r", type(hokeun_params[0][0][0]))
        # log(INFO, "Hokeun! type(params[0][0][0]): %r", type(params[0][0][0]))

        # log(INFO, "Hokeun! type(hokeun_params[0][0][0]): %r", str(hokeun_params[0][0][0]))
        # log(INFO, "Hokeun! type(params[0][0][0]): %r", str(params[0][0][0]))

        # log(INFO, "Hokeun! type(hokeun_params[0][0][0][0]): %r", type(hokeun_params[0][0][0][0]))
        # log(INFO, "Hokeun! type(params[0][0][0][0]): %r", type(params[0][0][0][0]))

        # # This type(params[0][0][0][0]) is: numpy.ndarray
        # log(INFO, "Hokeun! type(hokeun_params[0][0][0][0]): %r", str(hokeun_params[0][0][0][0]))
        # log(INFO, "Hokeun! type(params[0][0][0][0]): %r", str(params[0][0][0][0]))

        # # This type(params[0][0][0][0][0]) is: numpy.float32
        # log(INFO, "Hokeun! type(hokeun_params[0][0][0][0][0]): %r", type(hokeun_params[0][0][0][0][0]))
        # log(INFO, "Hokeun! type(params[0][0][0][0][0]): %r", type(params[0][0][0][0][0]))

        # log(INFO, "Hokeun! type(hokeun_params[0][0][0][0][0]): %r", str(hokeun_params[0][0][0][0][0]))
        # log(INFO, "Hokeun! type(params[0][0][0][0][0]): %r", str(params[0][0][0][0][0]))

        log(INFO, "Hokeun! are hokeun_params and params the same in string?: %r", str(hokeun_params) == str(params))
        # log(INFO, "Hokeun! are hokeun_params and params the same numerically?: %r", hokeun_params == params)
        
        log(INFO, "Hokeun! aggregate_inplace: hokeun_deep_count_float32(hokeun_params): %i", hokeun_deep_count_float32(hokeun_params))
        log(INFO, "Hokeun! aggregate_inplace: hokeun_deep_count_float32(params): %i", hokeun_deep_count_float32(params))

        # The following lines print out raw data.
        # log(INFO, "Hokeun! aggregate_inplace: hokeun_params: %r", hokeun_params)
        # log(INFO, "Hokeun! aggregate_inplace: params: %r", params)

    log(INFO, "Hokeun! aggregate_inplace: Final results: hokeun_deep_count_float32(hokeun_params): %i", hokeun_deep_count_float32(hokeun_params))
    log(INFO, "Hokeun! aggregate_inplace: Final results: hokeun_deep_count_float32(params): %i", hokeun_deep_count_float32(params))
    log(INFO, "Hokeun! aggregate_inplace: Final results: calling hokeun_deep_diff_float32() ...")

    print_diff = False
    log(INFO, "Hokeun! aggregate_inplace: Final results: hokeun_deep_diff_float32(hokeun_params, params): %i",
        hokeun_deep_diff_float32(hokeun_params, params, [], print_diff))

    return params


def aggregate_median(results: List[Tuple[NDArrays, int]]) -> NDArrays:
    """Compute median."""
    # Create a list of weights and ignore the number of examples
    weights = [weights for weights, _ in results]

    # Compute median weight of each layer
    median_w: NDArrays = [
        np.median(np.asarray(layer), axis=0) for layer in zip(*weights)
    ]
    return median_w


def aggregate_krum(
    results: List[Tuple[NDArrays, int]], num_malicious: int, to_keep: int
) -> NDArrays:
    """Choose one parameter vector according to the Krum function.

    If to_keep is not None, then MultiKrum is applied.
    """
    # Create a list of weights and ignore the number of examples
    weights = [weights for weights, _ in results]

    # Compute distances between vectors
    distance_matrix = _compute_distances(weights)

    # For each client, take the n-f-2 closest parameters vectors
    num_closest = max(1, len(weights) - num_malicious - 2)
    closest_indices = []
    for distance in distance_matrix:
        closest_indices.append(
            np.argsort(distance)[1 : num_closest + 1].tolist()  # noqa: E203
        )

    # Compute the score for each client, that is the sum of the distances
    # of the n-f-2 closest parameters vectors
    scores = [
        np.sum(distance_matrix[i, closest_indices[i]])
        for i in range(len(distance_matrix))
    ]

    if to_keep > 0:
        # Choose to_keep clients and return their average (MultiKrum)
        best_indices = np.argsort(scores)[::-1][len(scores) - to_keep :]  # noqa: E203
        best_results = [results[i] for i in best_indices]
        return aggregate(best_results)

    # Return the model parameters that minimize the score (Krum)
    return weights[np.argmin(scores)]


# pylint: disable=too-many-locals
def aggregate_bulyan(
    results: List[Tuple[NDArrays, int]],
    num_malicious: int,
    aggregation_rule: Callable,  # type: ignore
    **aggregation_rule_kwargs: Any,
) -> NDArrays:
    """Perform Bulyan aggregation.

    Parameters
    ----------
    results: List[Tuple[NDArrays, int]]
        Weights and number of samples for each of the client.
    num_malicious: int
        The maximum number of malicious clients.
    aggregation_rule: Callable
        Byzantine resilient aggregation rule used as the first step of the Bulyan
    aggregation_rule_kwargs: Any
        The arguments to the aggregation rule.

    Returns
    -------
    aggregated_parameters: NDArrays
        Aggregated parameters according to the Bulyan strategy.
    """
    byzantine_resilient_single_ret_model_aggregation = [aggregate_krum]
    # also GeoMed (but not implemented yet)
    byzantine_resilient_many_return_models_aggregation = []  # type: ignore
    # Brute, Medoid (but not implemented yet)

    num_clients = len(results)
    if num_clients < 4 * num_malicious + 3:
        raise ValueError(
            "The Bulyan aggregation requires then number of clients to be greater or "
            "equal to the 4 * num_malicious + 3. This is the assumption of this method."
            "It is needed to ensure that the method reduces the attacker's leeway to "
            "the one proved in the paper."
        )
    selected_models_set: List[Tuple[NDArrays, int]] = []

    theta = len(results) - 2 * num_malicious
    beta = theta - 2 * num_malicious

    for _ in range(theta):
        best_model = aggregation_rule(
            results=results, num_malicious=num_malicious, **aggregation_rule_kwargs
        )
        list_of_weights = [weights for weights, num_samples in results]
        # This group gives exact result
        if aggregation_rule in byzantine_resilient_single_ret_model_aggregation:
            best_idx = _find_reference_weights(best_model, list_of_weights)
        # This group requires finding the closest model to the returned one
        # (weights distance wise)
        elif aggregation_rule in byzantine_resilient_many_return_models_aggregation:
            # when different aggregation strategies available
            # write a function to find the closest model
            raise NotImplementedError(
                "aggregate_bulyan currently does not support the aggregation rules that"
                " return many models as results. "
                "Such aggregation rules are currently not available in Flower."
            )
        else:
            raise ValueError(
                "The given aggregation rule is not added as Byzantine resilient. "
                "Please choose from Byzantine resilient rules."
            )

        selected_models_set.append(results[best_idx])

        # remove idx from tracker and weights_results
        results.pop(best_idx)

    # Compute median parameter vector across selected_models_set
    median_vect = aggregate_median(selected_models_set)

    # Take the averaged beta parameters of the closest distance to the median
    # (coordinate-wise)
    parameters_aggregated = _aggregate_n_closest_weights(
        median_vect, selected_models_set, beta_closest=beta
    )
    return parameters_aggregated


def weighted_loss_avg(results: List[Tuple[int, float]]) -> float:
    """Aggregate evaluation results obtained from multiple clients."""
    num_total_evaluation_examples = sum(num_examples for (num_examples, _) in results)
    weighted_losses = [num_examples * loss for num_examples, loss in results]
    return sum(weighted_losses) / num_total_evaluation_examples


def aggregate_qffl(
    parameters: NDArrays, deltas: List[NDArrays], hs_fll: List[NDArrays]
) -> NDArrays:
    """Compute weighted average based on Q-FFL paper."""
    demominator: float = np.sum(np.asarray(hs_fll))
    scaled_deltas = []
    for client_delta in deltas:
        scaled_deltas.append([layer * 1.0 / demominator for layer in client_delta])
    updates = []
    for i in range(len(deltas[0])):
        tmp = scaled_deltas[0][i]
        for j in range(1, len(deltas)):
            tmp += scaled_deltas[j][i]
        updates.append(tmp)
    new_parameters = [(u - v) * 1.0 for u, v in zip(parameters, updates)]
    return new_parameters


def _compute_distances(weights: List[NDArrays]) -> NDArray:
    """Compute distances between vectors.

    Input: weights - list of weights vectors
    Output: distances - matrix distance_matrix of squared distances between the vectors
    """
    flat_w = np.array([np.concatenate(p, axis=None).ravel() for p in weights])
    distance_matrix = np.zeros((len(weights), len(weights)))
    for i, flat_w_i in enumerate(flat_w):
        for j, flat_w_j in enumerate(flat_w):
            delta = flat_w_i - flat_w_j
            norm = np.linalg.norm(delta)
            distance_matrix[i, j] = norm**2
    return distance_matrix


def _trim_mean(array: NDArray, proportiontocut: float) -> NDArray:
    """Compute trimmed mean along axis=0.

    It is based on the scipy implementation.

    https://docs.scipy.org/doc/scipy/reference/generated/
    scipy.stats.trim_mean.html.
    """
    axis = 0
    nobs = array.shape[axis]
    lowercut = int(proportiontocut * nobs)
    uppercut = nobs - lowercut
    if lowercut > uppercut:
        raise ValueError("Proportion too big.")

    atmp = np.partition(array, (lowercut, uppercut - 1), axis)

    slice_list = [slice(None)] * atmp.ndim
    slice_list[axis] = slice(lowercut, uppercut)
    result: NDArray = np.mean(atmp[tuple(slice_list)], axis=axis)
    return result


def aggregate_trimmed_avg(
    results: List[Tuple[NDArrays, int]], proportiontocut: float
) -> NDArrays:
    """Compute trimmed average."""
    # Create a list of weights and ignore the number of examples
    weights = [weights for weights, _ in results]

    trimmed_w: NDArrays = [
        _trim_mean(np.asarray(layer), proportiontocut=proportiontocut)
        for layer in zip(*weights)
    ]

    return trimmed_w


def _check_weights_equality(weights1: NDArrays, weights2: NDArrays) -> bool:
    """Check if weights are the same."""
    if len(weights1) != len(weights2):
        return False
    return all(
        np.array_equal(layer_weights1, layer_weights2)
        for layer_weights1, layer_weights2 in zip(weights1, weights2)
    )


def _find_reference_weights(
    reference_weights: NDArrays, list_of_weights: List[NDArrays]
) -> int:
    """Find the reference weights by looping through the `list_of_weights`.

    Raise Error if the reference weights is not found.

    Parameters
    ----------
    reference_weights: NDArrays
        Weights that will be searched for.
    list_of_weights: List[NDArrays]
        List of weights that will be searched through.

    Returns
    -------
    index: int
        The index of `reference_weights` in the `list_of_weights`.

    Raises
    ------
    ValueError
        If `reference_weights` is not found in `list_of_weights`.
    """
    for idx, weights in enumerate(list_of_weights):
        if _check_weights_equality(reference_weights, weights):
            return idx
    raise ValueError("The reference weights not found in list_of_weights.")


def _aggregate_n_closest_weights(
    reference_weights: NDArrays, results: List[Tuple[NDArrays, int]], beta_closest: int
) -> NDArrays:
    """Calculate element-wise mean of the `N` closest values.

    Note, each i-th coordinate of the result weight is the average of the beta_closest
    -ith coordinates to the reference weights


    Parameters
    ----------
    reference_weights: NDArrays
        The weights from which the distances will be computed
    results: List[Tuple[NDArrays, int]]
        The weights from models
    beta_closest: int
        The number of the closest distance weights that will be averaged

    Returns
    -------
    aggregated_weights: NDArrays
        Averaged (element-wise) beta weights that have the closest distance to
         reference weights
    """
    list_of_weights = [weights for weights, num_examples in results]
    aggregated_weights = []

    for layer_id, layer_weights in enumerate(reference_weights):
        other_weights_layer_list = []
        for other_w in list_of_weights:
            other_weights_layer = other_w[layer_id]
            other_weights_layer_list.append(other_weights_layer)
        other_weights_layer_np = np.array(other_weights_layer_list)
        diff_np = np.abs(layer_weights - other_weights_layer_np)
        # Create indices of the smallest differences
        # We do not need the exact order but just the beta closest weights
        # therefore np.argpartition is used instead of np.argsort
        indices = np.argpartition(diff_np, kth=beta_closest - 1, axis=0)
        # Take the weights (coordinate-wise) corresponding to the beta of the
        # closest distances
        beta_closest_weights = np.take_along_axis(
            other_weights_layer_np, indices=indices, axis=0
        )[:beta_closest]
        aggregated_weights.append(np.mean(beta_closest_weights, axis=0))
    return aggregated_weights
