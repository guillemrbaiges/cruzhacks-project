from pathlib import Path

from kfp.dsl import pipeline  # type: ignore
from kfp_unicron.pipelines import load_config
from kfp_unicron.pipelines.pipeline_model import PipelineConfig


@pipeline()  # type: ignore
def deploy_schip(
    app_name: str,
    app_version: str,
    app_serving_image: str,
    app_deployment_env: str,
):
    pipeline_config: PipelineConfig = load_config(Path(__file__).parent.name)
    gitops_repo = (
        pipeline_config.get_organization()
        + "/"
        + pipeline_config.config["GITOPS_REPOSITORY"]
    )

    # Get model's context
    get_app_context_step = pipeline_config.components["get-app-context"](
        "/app",
        app_name,
        pipeline_config.config["MODEL_DEPLOYMENT_NAMESPACE"],
        app_deployment_env,
    ).apply(pipeline_config.default_modifiers)

    # Deploy model into the Gitops repository
    trigger_model_deployment_step = pipeline_config.components["deploy-model"](
        argocd_dest_namespace=get_app_context_step.outputs["argocd_dest_namespace"],
        image=app_serving_image,
        application=get_app_context_step.outputs["argocd_application_name"],
        kustomize_folder="kustomize",
        catalog_file="catalog/application.yaml",
        branch=pipeline_config.get_environment(),
        skip_pull_request="true",
        gitops_repo=gitops_repo,
        context=get_app_context_step.outputs["model_k8s_manifests_folder"],
        version=app_version,
        delete_all="false",
    ).apply(pipeline_config.modifiers["deploy-model"])

    # Wait for a succeeded deployment
    pipeline_config.components["wait-argocd-sync"](
        application=get_app_context_step.outputs["argocd_application_name"]
    ).apply(pipeline_config.default_modifiers).after(trigger_model_deployment_step)
