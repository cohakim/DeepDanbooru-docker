.PHONY: download
download:
	@docker compose run --rm download

.PHONY: evaluate
evaluate:
	@docker compose run --rm -e TARGET evaluate TARGET=${TARGET}

