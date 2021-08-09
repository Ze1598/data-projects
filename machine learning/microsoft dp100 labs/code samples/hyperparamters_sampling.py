# Grid sampling
###############################################################################
# Can only be used when all hyperparameters are discrete
# Tries every possible combination of parameters in the search space

from azureml.train.hyperdrive import GridParameterSampling, choice

# This grid sampling tries every possible combination of batch_size 
# and learning_rate values
param_space = {
    "--batch_size": choice(16, 32, 64),
    "--learning_rate": choice(0.01, 0.1, 1.0)
}

param_sampling = GridParameterSampling(param_space)
###############################################################################


# Random sampling
###############################################################################
# Randomly select a value for each hyperparameter, which can be a mix of discrete and 
# continuous values

from azureml.train.hyperdrive import RandomParameterSampling, choice, normal

param_space = {
    "--batch_size": choice(16, 32, 64),
    "--learning_rate": normal(10, 3)
}

param_sampling = RandomParameterSampling(param_space)
###############################################################################


# Bayesian sampling
###############################################################################
# Chooses hyperparameter values based on the Bayesian optimization algorithm, 
# which tries to select parameter combinations that will result in improved
# performance from the previous selection

from azureml.train.hyperdrive import BayesianParameterSampling, choice, uniform

param_space = {
    "--batch_size": choice(16, 32, 64),
    "--learning_rate": uniform(0.05, 0.1)
}

param_sampling = BayesianParameterSampling(param_space)
###############################################################################