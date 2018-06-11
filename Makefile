all: debug
debug:
	bash make_build.sh Debug
release:
	bash make_build.sh Release
clean:
	bash make_clean.sh
