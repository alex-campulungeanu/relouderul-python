.PHONY: first

#############
## SUMMARY ##
#############
help:
	@echo " "
	@echo "✨ Available commands:"
	@echo " "
	@echo "	💡 Services:"
	@echo "		make first
	@echo "		make second"

## Start services ##
###############

first:
	uv run python main.py --service first

