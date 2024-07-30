from typing import NamedTuple 
from kfp.components import OutputPath


def get_app_context(
    source_folder: str, app_name: str, 
    app_deployment_namespace: str, app_deployment_env: str,
    model_k8s_manifests_folder_path: OutputPath()  # type: ignore
) -> NamedTuple('ParseOutputs', [('argocd_application_name', str), ('argocd_dest_namespace', str)]):  # type: ignore
    import os
    from collections import namedtuple
    from shutil import copytree

    
    parse_output = namedtuple('ParseOutputs', ['argocd_application_name', 'argocd_dest_namespace'])  # type: ignore

    # Copying folder with deployment manifests
    os.makedirs(model_k8s_manifests_folder_path, exist_ok=True)
    copytree(src=f'{source_folder}/deploy', dst=str(model_k8s_manifests_folder_path), dirs_exist_ok=True)

    argocd_app_name = app_name + '-api-' + app_deployment_env
    argocd_namespace = app_deployment_namespace + '-' + app_deployment_env

    return parse_output(argocd_app_name, argocd_namespace)
