Here's an updated README with comprehensive setup instructions using `environment.yml` and including the `.credentials` directory setup:

---

# ConveneAI  
Intelligent meeting tool that works with your data  

## Backend Setup

### Overview  
This backend service processes meeting transcripts to generate relevant email queries and summaries.

### Prerequisites

- Install [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).
- Ensure [Python 3.10](https://www.python.org/downloads/) is available in the Conda environment.

## Setup

### 1. Create Conda Environment

To create the environment and install all dependencies from `environment.yml`, run:

```bash
# Create and activate environment
conda create -n meeting-assistant python=3.10
conda activate meeting-assistant
conda install --file requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the project root with the necessary API keys:

```env
OPENAI_API_KEY=
FLASK_ENV=development
FLASK_DEBUG=1
ANTHROPIC_API_KEY=
```

### 3. Create `.credentials` Directory

For secure storage of additional credentials (e.g., `token.json` for Gmail API access), create a `.credentials` directory in the backend:

```bash
# Create .credentials directory in backend
not
```

**Note**: Ask Anwar for the necessary tokens and place them in the `.credentials` directory.

## Running the Server

To start the backend server, run:

```bash
# From the project root
python backend/run.py
```

The server will be available at `http://localhost:5000`.

## Testing the Endpoints

### 1. Health Check

To confirm the server is running, check the health endpoint:

```bash
curl http://localhost:5000/health
```

### 2. Test with Sample Data

Try a sample query using:

```bash
curl http://localhost:5000/demo-queries
```

### 3. Test with Custom Transcript

To analyze a custom transcript, use:

```bash
curl -X POST http://localhost:5000/analyze-transcript \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "John: Can you find that budget email from Sarah? Mary: The one from last week with the Excel file?"
  }'
```

--- 

