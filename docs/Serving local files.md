If you wish to serve local files, such as custom `.css` stylesheets or images, they will need to be placed in the `./static` folder, relative to the project root.
```
.
├── .envrc
├── app.py
├── .pythonwebio/
│   └── config.toml
└── static/
```

Files stored here can be referenced using a `/static/image.png`-like URL.

For security reasons (to prevent a malicious user accessing the entire server using a few `../../`), the underlying `FastAPI` server will not serve local files from outside this directory.
