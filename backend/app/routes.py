from flask import Blueprint, request, jsonify

main = Blueprint('main', __name__)

@main.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@main.route('/process-transcript', methods=['POST'])
def process_transcript():
    try:
        data = request.get_json()
        if not data or 'transcript' not in data:
            return jsonify({'error': 'No transcript provided'}), 400
        
        transcript = data['transcript']
        # TODO: Process transcript (we'll implement this later)
        
        return jsonify({'message': 'Transcript received', 'length': len(transcript)}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500