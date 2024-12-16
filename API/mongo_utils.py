from pymongo import MongoClient

# Hàm xử lý dữ liệu trước khi lưu vào MongoDB
def process_transcription_data(response, audio_url):
    # Chuyển đổi 'transcript_words' từ object thành dictionary
    transcript_words_processed = []
    transcript_words = response.get('transcript_words', [])
    if transcript_words:
        for word in transcript_words:
            word_dict = {
                "text": word.text,
                "start": word.start,
                "end": word.end,
                "confidence": word.confidence,
                "speaker": word.speaker
            }
            transcript_words_processed.append(word_dict)

    # Chuyển đổi 'utterance' từ object thành dictionary nếu có
    utterances_processed = []
    utterances = response.get('utterance', [])
    if utterances:
        for utterance in utterances:
            utterance_dict = {
                "text": utterance.text,
                "start": utterance.start,
                "end": utterance.end,
                "confidence": utterance.confidence,
                "speaker": utterance.speaker
            }
            utterances_processed.append(utterance_dict)
        
    data_to_save = {
        'transcript': response.get('transcript', ''),
        'transcript_words': transcript_words_processed,
        'utterance': utterances_processed,
        'summary': response.get('summary', ''),
        'topic': response.get('topic', ''),
        'chapter': response.get('chapter', ''),
        'content': response.get('content', ''),
        'phrases': response.get('phrases', ''),
        'sentiment': response.get('sentiment', ''),
        'entities': response.get('entity', '')
    }
    
    return {
        'audio_url': audio_url,
        'data_id': response.get('data_id', ''),
        'data': data_to_save
    }
