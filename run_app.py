import streamlit.web.cli as stcli
import sys
import os

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath("."))
    sys.argv = [
        "streamlit",
        "run",
        "src/client/app.py",
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())
