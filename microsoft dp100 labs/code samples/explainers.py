from interpret.ext.blackbox import PFIExplainer, TabularExplainer, MimicExplainer
from interpret.ext.glassbox import DecisionTreeExplainableModel

# Local model explainer: explainers for feature importance
# Global feature importance: feature importance for the overall dataset
# Local feature importance: feature importance for a subset of data


# MimicExplainer
# Creates a global surrogate model that approximates your trained model and can
# be used to generate explanations
# The explainable model must have the same kind of architecture as your trained model
###############################################################################
mim_explainer = MimicExplainer(
    model=model,
    initialization_examples=X_test,
    explainable_model=DecisionTreeExplainableModel,
    features=[
        "loan_amount",
        "income",
        "age",
        "marital_status"
    ],
    classes=[
        "reject",
        "approve"
    ]
)
###############################################################################


# TabularExplainer
# An explainer that acts as a wrapper around various SHAP explainer algorithms,
# automatically choosing the one that is most appropriate for your model architecture
###############################################################################
tab_explainer = TabularExplainer(
    model=model,
    initialization_examples=X_test,
    features=[
        "loan_amount",
        "income",
        "age",
        "marital_status"
    ],
    classes=[
        "reject",
        "approve"
    ]
)
###############################################################################


# PFIExplainer
# Permutation Feature Importance explainer that analyzes feature importance by
# shuffling feature values and measuring the impact on prediction performance
###############################################################################
pfi_explainer = PFIExplainer(
    model=model,
    features=[
        "loan_amount",
        "income",
        "age",
        "marital_status"
    ],
    classes=[
        "reject",
        "approve"
    ]
)
###############################################################################


# Global feature importance
###############################################################################
# MimicExplainer
global_mim_explanation = mim_explainer.explain_global(X_train)
global_mim_feature_importance = global_mim_explanation.get_feature_importance_dict()


# TabularExplainer
global_tab_explanation = tab_explainer.explain_global(X_train)
global_tab_feature_importance = global_tab_explanation.get_feature_importance_dict()


# PFIExplainer
global_pfi_explanation = pfi_explainer.explain_global(X_train, y_train)
global_pfi_feature_importance = global_pfi_explanation.get_feature_importance_dict()
###############################################################################


# Local feature importance
###############################################################################
# MimicExplainer
local_mim_explanation = mim_explainer.explain_local(X_test[0:5])
local_mim_features = local_mim_explanation.get_ranked_local_names()
local_mim_importance = local_mim_explanation.get_ranked_local_values()


# TabularExplainer
local_tab_explanation = tab_explainer.explain_local(X_test[0:5])
local_tab_features = local_tab_explanation.get_ranked_local_names()
local_tab_importance = local_tab_explanation.get_ranked_local_values()
###############################################################################



# Upload explanation
###############################################################################
from azureml.core.run import Run
from azureml.contrib.interpret.explanation.explanation_client import ExplanationClient
from interpret.ext.blackbox import TabularExplainer

# Get the experiment run context
run = Run.get_context()

# Train model
...

# Get explanation
explainer = TabularExplainer(model, X_train, features=features, classes=labels)
explanation = explainer.explain_global(X_test)

# Get an Explanation Client and upload the explanation
explain_client = ExplanationClient.from_run(run)
explain_client.upload_model_explanation(explanation, comment='Tabular Explanation')

# Complete the run
run.complete()
###############################################################################


# View explanation
###############################################################################
from azureml.contrib.interpret.explanation.explanation_client import ExplanationClient

client = ExplanationClient.from_run_id(
    workspace=ws,
    experiment_name=experiment.experiment_name, 
    run_id=run.id
)
explanation = client.download_model_explanation()
feature_importances = explanation.get_feature_importance_dict()
###############################################################################