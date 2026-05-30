# AutoCoder

AutoCoder is a GitHub Actions-powered automation tool that uses OpenAI's ChatGPT to generate code directly from GitHub Issues. When a developer opens an issue labeled `autocoder-bot` and describes the code they need, the workflow automatically sends the issue body as a prompt to ChatGPT, extracts the generated code snippets, commits them to a new branch, and opens a pull request for review.

## How It Works

1. Open a GitHub Issue with the label `autocoder-bot`.
2. Write a clear prompt in the issue body describing the code to generate, including file names and expected content.
3. The GitHub Actions workflow triggers, calls the ChatGPT API with your prompt, and saves the generated files.
4. A pull request is automatically created on a branch named `autocoder-branch-<issue-number>` for you to review and merge.

## Tech Stack

- **GitHub Actions** — orchestrates the automation pipeline
- **Bash** — the script that calls the GitHub and OpenAI APIs
- **OpenAI ChatGPT API** — generates code based on issue prompts
- **PyGithub** — Python library used in tests to verify repository state

## Repository Structure

```
AutoCoder/
├── .github/
│   └── workflows/
│       └── main.yml   # GitHub Actions workflow
├── scripts/
│   └── script.sh      # Script to call ChatGPT and generate code
└── README.md
```

## Setup

1. Fork or clone this repository.
2. Add `OPENAI_API_KEY` as a repository secret (Settings → Secrets → Actions).
3. Create an issue with the `autocoder-bot` label and a descriptive prompt body.
4. Watch the Actions tab as the workflow runs and a pull request is created automatically.
