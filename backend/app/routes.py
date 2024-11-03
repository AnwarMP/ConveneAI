from flask import Blueprint, request, jsonify
from src.agent import EmailQueryAgent, MeetingAnalysisAgent
from config import Config

main = Blueprint('main', __name__)

# Initialize with OpenAI
email_agent = EmailQueryAgent(
    llm_provider="openai",
    api_key=Config.OPENAI_API_KEY
)

meeting_agent = MeetingAnalysisAgent(
    api_key=Config.ANTHROPIC_API_KEY
)

@main.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

from flask import Blueprint, request, jsonify
from src.agent import MeetingAnalysisAgent
from config import Config

main = Blueprint('main', __name__)

# Initialize the MeetingAnalysisAgent
meeting_agent = MeetingAnalysisAgent(api_key=Config.ANTHROPIC_API_KEY)

@main.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@main.route('/analyze-transcript', methods=['POST'])
async def analyze_transcript():
    """
    Endpoint to analyze transcript segments and update meeting summary
    
    Expected JSON payload:
    {
        "transcript": "Text with timestamps and messages..."
    }
    """
    try:
        data = request.get_json()
        if not data or 'transcript' not in data:
            return jsonify({
                'error': 'No transcript provided'
            }), 400

        # Get the transcript text
        transcript = data['transcript']
        print("Received transcript:", transcript)  # Debug log

        # Process transcript for summary update - pass transcript directly
        updated_summary = meeting_agent.process_segment(
            existing_summary='',  # Start fresh each time
            new_transcript=transcript  # Pass the formatted transcript directly
        )

        print("Updated summary:", updated_summary)  # Debug log
        
        return jsonify({
            'status': 'success',
            'results': {
                'summary': updated_summary
            }
        }), 200
    
    except Exception as e:
        print("Error processing transcript:", str(e))  # Debug log
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


@main.route('/demo-queries', methods=['GET'])
async def demo_queries():
    """Demo endpoint with sample transcripts and their analysis"""
    
    sample_transcripts = [
        {
            "scenario": "Budget Review Email",
            "transcript": """
            John: Hey team, can someone forward me that email Sarah sent last week about the Q4 budget review?
            Mary: The one with the Excel spreadsheet attachments?
            John: Yeah, the one she sent to the whole finance team on Thursday.
            Bob: I think it had 'FY24 Q4 Budget Final' in the subject line.
            """
        },
        {
            "scenario": "Marketing Campaign PDF",
            "transcript": """
            Alice: Has anyone seen the marketing presentation Janet sent yesterday?
            Bob: Was it the PDF with the new campaign designs?
            Alice: Yes, she sent it to the marketing team with all the Q1 plans.
            """
        },
        {
            "scenario": "Project Timeline",
            "transcript": """
            Mike: Could you find that email thread from David about project timelines?
            Sarah: The one from last month with the Gantt chart attached?
            Mike: Yes, he sent it to all project managers with subject 'Updated 2024 Roadmap'
            """
        }
    ]
    
    try:
        results = []
        for sample in sample_transcripts:
            analysis = await email_agent.analyze_transcript_segment(sample["transcript"])
            results.append({
                "scenario": sample["scenario"],
                "transcript": sample["transcript"],
                "analysis": analysis
            })
        
        return jsonify({
            'status': 'success',
            'sample_analyses': results
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500
    
@main.route('/test-email', methods=['POST'])
async def test_email():
    """Endpoint for direct email queries from chat"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({
                'error': 'No query provided',
                'status': 'error'
            }), 400

        analysis_results = await email_agent.analyze_transcript_segment(query)
        
        return jsonify({
            'status': 'success',
            'results': analysis_results
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500