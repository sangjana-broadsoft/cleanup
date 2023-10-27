from cx_Freeze import setup, Executable

setup(
    name = "BPACleanup",
    version = "0.1",
    description = "I wish programming was this easy",
    executables = [Executable("main.py")], target_name="BPACleanup")