from uu_game import run

# The extra module level is needed because IDEs like to use global imports,
# and having a namespace of your own that isn't "src" is good for other reasons.
if __name__ == "__main__":
    run()