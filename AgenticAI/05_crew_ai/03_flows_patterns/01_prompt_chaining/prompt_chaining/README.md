# Prompt Chaining Pattern Flow 

## How to run locally

### Pre-Requisites

- Python 3.10 or higher
- Get your API key from [Goolge AI Studio](https://aistudio.google.com/)
- Add your api key in `.env` file.
-  UV(our preferred command-line runner)

1. Rename .env.example to .env and add GOOGLE_API_KEY.

2. Install required packages
```bash
uv sync
```
5. Run the Flow
```bash
uv run kickoff
```
or
```bash
crewai flow kickoff
```

6. Create the Plot
```bash
uv run plot
```
or
```bash
crewai flow plot
```
