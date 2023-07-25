# # Simple makefile to simplify repetitive build env management tasks under posix

# CODESPELL_DIRS ?= .
# CODESPELL_SKIP ?= "*.pyc,*.txt,*.gif,*.png,*.jpg,*.js,*.html,*.doctree,*.ttf,*.woff,*.woff2,*.eot,*.mp4,*.inv,*.pickle,*.ipynb,flycheck*,./.git/*,./.hypothesis/*,*.yml,./doc/build/*,./doc/images/*,./dist/*,*~,.hypothesis*,./doc/source/examples/*,*cover,*.dat,*.mac,build,./factory/*,PKG-INFO,*.mypy_cache/*,./_unused/*,./doc/source/_templates/*"
# CODESPELL_IGNORE ?= "doc/styles/Vocab/ANSYS/accept.txt"

# all: doctest flake8

# doctest: codespell

# codespell:
# 	@echo "Running codespell"
# 	@codespell $(CODESPELL_DIRS) -S $(CODESPELL_SKIP) # -I $(CODESPELL_IGNORE)

# flake8:
# 	@echo "Running flake8"
# 	@flake8 .
