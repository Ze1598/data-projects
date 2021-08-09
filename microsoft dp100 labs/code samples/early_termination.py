# Bandit policy
###############################################################################
# Stop a run if the target performance metric underperforms the best run so far
# by a specified margin

from azureml.train.hyperdrive import BanditPolicy


# Applies the policy for every iteration (`evaluation_interval = 1`) after the 
# first five (`delay_evaluation = 5`), and abandon runs where the reported target 
# metric is 0.2 (`slack_amount = 0.2`) or more worse than the best performing
# run after `delay_evaluation` runs
early_termination_policy = BanditPolicy(
    slack_amount = 0.2,
    evaluation_interval = 1,
    delay_evaluation = 5,
)
# Bandit policy can also use a `slack_factor` to compare the performance metric as a
# ratio instead of an absolute value (`slack_amount`)
###############################################################################


# Median stopping policy
###############################################################################
# Abandons runs where the target performance metric is worse than the median of 
# the running averages for all runs

from azureml.train.hyperdrive import MedianStoppingPolicy

# Cancels run where the target metric is worse than running median. The policy is 
# applied every run, after the first five runs
early_termination_policy = MedianStoppingPolicy(
    evaluation_interval = 1,
    delay_evaluation = 5
)
###############################################################################


# Truncation selection policy
###############################################################################
# Cancels the lowest performing X% of runs at each evaluation interval based on
# the truncation_percentage value specified for X
from azureml.train.hyperdrive import TruncationSelectionPolicy

# Cancels the 10% lowest performing runs. The policy is applied every run after
# the first five
early_termination_policy = TruncationSelectionPolicy(
    truncation_percentage = 10,
    evaluation_interval = 1,
    delay_evaluation = 5
)
###############################################################################