import cx_Freeze

executables = [cx_Freeze.Executable("game.py")]

cx_Freeze.setup(
    name="Ad Hoc TV",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["assets/"]}},
    executables=executables

)
