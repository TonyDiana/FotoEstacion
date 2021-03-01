# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = ./
BUILDDOC      = ../docs

# Put it first so that "make" without argument is like "make help".
help:
	@clear
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDOC)" $(SPHINXOPTS) $(O)

	@echo ""
	@echo "	all --- Borrar todo y generar todo y html"
	@echo ""

.PHONY: help Makefile

.PHONY: web
web:
	# Borrar todo para regenerar de nuevo
	@-rm -r $(BUILDDOC)

	make html

	@rm -r $(BUILDDOC)/doctrees/
	@rm -r $(BUILDDOC)/html/_sources/

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDOC)" $(SPHINXOPTS) $(O)
	@cp $(SOURCEDIR)/index.html $(BUILDDOC)
	@cp $(SOURCEDIR)/.nojekyll $(BUILDDOC)
