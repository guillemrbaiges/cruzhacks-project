include ../Makefile.common

EXCLUDED_COMPONENTS =

##@ Components

.PHONY: components-python-init
components-python-init: ## Initialize the python environment to all the components
	for component_name in $(call get_components_list); do \
		$(MAKE) -C ../components/$$component_name python-init || exit 1; \
	done

.PHONY: components-python-update
components-python-update:  ## Updates the python environment to all the components
	for component_name in $(call get_components_list); do \
		$(MAKE) -C ../components/$$component_name python-update || exit 1; \
	done

.PHONY: components-python-test
components-python-test:  ## Updates the python environment to all the components
	for component_name in $(call get_components_list); do \
		$(MAKE) -C ../components/$$component_name python-test || exit 1; \
	done

.PHONY: components-list
components-list: ## List your components
	poetry run kfp-unicron components list

.PHONY: components-build-all
components-build-all: ## Build all your components
	poetry run kfp-unicron components build-all

.PHONY: clean
clean: ## Clean the temporary folders used on your components
	poetry run kfp-unicron components clean


##@ Pipelines

.PHONY: pipeline-compile-prompt-eng
pipeline-compile-prompt-eng: ## Compiles the prompt_eng pipeline.
	poetry run kfp-unicron pipelines compile prompt_eng deploy_streamlit_app --output deploy_streamlit_app-world.yaml

.PHONY: pipeline-run-prompt-eng
pipeline-run-prompt-eng: ## Runs the prompt-eng pipeline.
	poetry run kfp-unicron pipelines run prompt_eng deploy_streamlit_app


define get_components_list
	$(filter-out $(EXCLUDED_COMPONENTS),$(shell poetry run kfp-unicron components list))
endef
