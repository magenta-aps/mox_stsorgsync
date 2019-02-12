import os
import pathlib
import configparser

inipaths = [p for p in [
        pathlib.Path(os.environ.get("MOX_MO_CONFIG", "")),
        pathlib.Path("") / "settings.ini",
        pathlib.Path(__file__).absolute() / "settings.ini",
    ] if p.is_file()
]

if not len(inipaths):
    inifile = ""
else:
    inifile = inipaths[0]

config = configparser.ConfigParser(defaults={
    "MOX_LOG_LEVEL": "10",
    "MOX_LOG_FILE": "",  # "" sends log to console
})
config["settings"] = {}

if inifile:
    config.read(str(inifile))

settings = config["settings"]

