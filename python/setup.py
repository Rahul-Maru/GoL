import cx_Freeze

executables = [cx_Freeze.Executable("game.py")]

cx_Freeze.setup(
    name="Game of Life",
    options={"build_exe": {"packages":["pygame", "math", "sys"],
                           "include_files":["render.py", "constants.py"]}},
    executables = executables

    )