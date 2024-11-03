from flask import Blueprint, request, jsonify
from src.agent import MeetingAnalysisAgent
from src.agent import GeminiAgent
from config import Config

main = Blueprint('main', __name__)



# Initialize the MeetingAnalysisAgent (single instance)
meeting_agent = MeetingAnalysisAgent(llm_provider="anthropic", api_key=Config.ANTHROPIC_API_KEY)
# meeting_agent = MeetingAnalysisAgent(llm_provider="openai", api_key=Config.OPENAI_API_KEY)

gemini_agent = GeminiAgent(api_key=Config.GOOGLE_API_KEY)

@main.route('/analyze-transcript', methods=['POST'])
async def analyze_transcript():
    """
    Endpoint to analyze transcript segments and update meeting summary
    
    Expected JSON payload:
    {
        "transcript": "New transcript segment",
        "existing_summary": "Previous summary if any",
        "full_transcript": "Complete meeting transcript history"
    }
    """
    try:
        data = request.get_json()
        if not data or 'transcript' not in data:
            return jsonify({
                'error': 'No transcript provided'
            }), 400

        new_transcript = data['transcript']
        existing_summary = data.get('existing_summary', '')
        full_transcript = data.get('full_transcript', '')
        
        print(f"Received request to analyze transcript")
        print(f"New segment length: {len(new_transcript)} characters")
        print(f"Full transcript length: {len(full_transcript)} characters")

        # Pass both new segment and full transcript to agent
        updated_summary = meeting_agent.process_segment(
            existing_summary=existing_summary,
            new_transcript=new_transcript,
            full_transcript=full_transcript
        )

        print(f"Generated summary length: {len(updated_summary)} characters")
        
        return jsonify({
            'status': 'success',
            'results': {
                'summary': updated_summary
            }
        }), 200
    
    except Exception as e:
        print("Error processing transcript:", str(e))
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@main.route('/call-gemini', methods=['POST'])
async def call_gemini():
    """
    Endpoint for Gemini to analyze and enhance recorded meeting transcript.
    
    Expected JSON payload:
    {
        "transcript": "Raw meeting transcript from recording",
        "existing_notes": "Current meeting notes if any"
    }
    """
    try:
        data = request.get_json()
        if not data or 'transcript' not in data:
            return jsonify({
                'error': 'No transcript provided',
                'status': 'error'
            }), 400

        transcript = data['transcript']
        existing_notes = data.get('existing_notes', '')
        
        print(f"Received request for Gemini transcript enhancement")
        print(f"Transcript length: {len(transcript)} characters")
        print(f"Existing notes length: {len(existing_notes)} characters")

        # Enhance transcript with Gemini
        enhanced_transcript = gemini_agent.analyze_transcript(
            transcript=transcript,
            existing_notes=existing_notes
        )

        print(f"Generated enhanced transcript length: {len(enhanced_transcript)} characters")

        return jsonify({
            'st tus': 'success',
            'results': {
                'enhanced_transcript': enhanced_transcript
            }
        }), 200

    except Exception as e:
        print("Error processing with Gemini:", str(e))
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@main.route('/chat-gemini', methods=['POST'])
async def chat_gemini():
    """
    Endpoint for chatting with Gemini about the video/meeting.
    
    Expected JSON payload:
    {
        "message": "User's message/question",
        "chat_history": "Previous chat messages (optional)"
    }
    """
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'error': 'No message provided',
                'status': 'error'
            }), 400

        message = data['message']
        chat_history = data.get('chat_history', '')
        
        print(f"Received chat request for Gemini")
        print(f"Message: {message}")
        print(f"Chat history length: {len(chat_history)} characters")

        # Chat with Gemini
        response = gemini_agent.chat(
            prompt=message,
            chat_history=chat_history
        )

        print(f"Generated Gemini response length: {len(response)} characters")

        return jsonify({
            'status': 'success',
            'results': {
                'response': response
            }
        }), 200

    except Exception as e:
        print("Error chatting with Gemini:", str(e))
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