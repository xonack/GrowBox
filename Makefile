.PHONY: zip
zip:
	zip to_submit.zip *

.PHONY: clean
clean:
	rm to_submit.zip
