# NOTE: save this file as .envrc and activate using `direnv allow` from same directory

# if testing `tests/linux_gpt.py`, set your OpenAI API Key
export OPENAI_API_KEY=""

# flask server env vars
export FLASK_SECRET_KEY=""
export FLASK_SESSION_PERMANENT=false
export FLASK_SESSION_USE_SIGNER=true
# flask server-side sessions env var
export FLASK_SESSION_TYPE="filesystem"
