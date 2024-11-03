# ConveneAI
Intelligent meeting tool that works with your data


## Backend Setup
# ConveneAI Backend

Backend service that processes meeting transcripts to generate relevant email queries.

## Setup

### 1. Create Conda Environment

```bash
# Create environment
conda create -n meeting-assistant python=3.10
conda activate meeting-assistant
```

### 2. Install Dependencies

```bash
# Add required packages
pip install requirements.txt
```

### 3. Environment Variables

Create `.env` file in project root:
```env
OPENAI_API_KEY=
FLASK_ENV=development
FLASK_DEBUG=1
ANTHROPIC_API_KEY=
```

## Running the Server

```bash
# From project root
python backend/run.py
```

Server runs on `http://localhost:5000`

## Testing the Endpoints

### 1. Health Check
```bash
curl http://localhost:5000/health
```

### 2. Test with Sample Data
```bash
curl http://localhost:5000/demo-queries
```

### 3. Test with Custom Transcript
```bash
curl -X POST http://localhost:5000/analyze-transcript \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "John: Can you find that budget email from Sarah? Mary: The one from last week with the Excel file?"
  }'
```

