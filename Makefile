## DO NOT EDIT THIS file
.DEFAULT_GOAL := doc-build

SHELL := /bin/bash

PYTHONPATH=".:$(shell poetry run python -c "import os; print(':'.join([os.path.join('./components', folder, 'src') for folder in next(os.walk('./components'))[1]]))")"

##@ General

# The help target prints out all targets with their descriptions organized
# beneath their categories. The categories are represented by '##@' and the
# target descriptions by '##'. The awk commands is responsible for reading the
# entire set of makefiles included in this invocation, looking for lines of the
# file as xyz: ## something, and then pretty-format the target and help. Then,
# if there's a line with ##@ something, that gets pretty-printed as a category.
# More info on the usage of ANSI control characters for terminal formatting:
# https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_parameters
# More info on the awk command:
# http://linuxcommand.org/lc3_adv_awk.php

.PHONY: help
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Documentation

.PHONY: doc-install-adv
ADV_INSTALL_DIR="/tmp/adv-install"
doc-install-adv: ## Install adv tool.
	git clone -b master --single-branch https://github.mpi-internal.com/cli/adv "${ADV_INSTALL_DIR}"
	"${ADV_INSTALL_DIR}/bin/adv-install"
	rm -fr ${ADV_INSTALL_DIR}
	adv --version

.PHONY: doc-view
doc-view:
	PYTHONPATH="${PYTHONPATH}" adv yack view --docs-dir _docs --project-root .

.PHONY: doc-build
doc-build: ## Builds the doc.
	rm -rf /tmp/build
	rm -rf docs
	# rendered html contents can change depending on your terminal size due to line wrappings, that's why we have COLUMNS=80 below
	COLUMNS=80 PYTHONPATH="${PYTHONPATH}" adv yack build --docs-dir _docs --build-dir /tmp/build
	mv /tmp/build docs
	rm -f docs/yack.metadata.json docs/yack.log docs/sitemap.xml*

.PHONY: doc-test
doc-test: doc-build ## Test the doc generation
	adv --version
	test -z "$(shell git status --porcelain --untracked-files=no docs | grep -v 'objects.inv\|search_index.json')" || (echo "there are uncommitted changes in the 'docs' folder, to fix it you can do 'make doc-build && git add docs && git commit ...'." && git diff && exit 1)


