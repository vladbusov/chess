from cx_Freeze import setup, Executable

setup(
    name = "chess",
    version = "0.1",
    description = "Blackjack",
    executables = [Executable("main.py")]
)