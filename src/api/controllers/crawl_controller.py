from flask import Blueprint, request, jsonify
from src.api.services.crawl_service import start_crawl_process

crawl_bp = Blueprint('crawl', __name__)

@crawl_bp.route('/api/crawl', methods=['POST'])
def crawl():
    data = request.json
    response = start_crawl_process(data)
    return jsonify(response)
