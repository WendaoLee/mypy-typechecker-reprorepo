# Reproduce Repo For Mypy Type Checker

## Preliminaries

- Python 3.12+
- Poetry

## Step

1. In the project's folder,run

   ```bash
   poetry config virtualenvs.in-project true
   poetry install
   ```

2. then,activate the venv:

```bash
poetry shell
```

3. In the venv,run mypy to make sure cache has made:

```bash
mypy
```

4. Go to the extension,change the daemon settings,watching the different perfermence between the `mypy-type-checker.preferDaemon=true` and ``mypy-type-checker.preferDaemon=false`