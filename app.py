from flask import Flask, jsonify, request

from data_scraper import scrape_data
from db_client import load_villagers, load_villager, search_villagers

app = Flask(__name__)


@app.route('/villagers', methods=['GET'])
def villagers():
    villagers_list = load_villagers()
    if villagers_list:
        return jsonify(villagers_list), 200
    return jsonify({'error': 'Unable to load Villagers'}), 404


@app.route('/villager/<int:villager_id>', methods=['GET'])
def villager(villager_id):
    result = load_villager(villager_id)
    if result is None:
        return jsonify({'id': villager_id, 'error': 'Villager does not exist'}), 404
    else:
        return jsonify(result), 200


@app.route('/villagers/search', methods=['GET'])
def search():
    search_name = request.args.get('name')
    if search_name:
        result = search_villagers(search_name)
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Invalid Search Parameter'}), 406


@app.route('/villagers/scraper', methods=['POST'])
def scrape():
    tbl_name = request.args.get('tbl')
    if tbl_name:
        result_code, result_msg = scrape_data(tbl_name)
        if result_code == 0:
            return jsonify(result_msg), 201
        else:
            return jsonify(result_msg), 501
    else:
        return jsonify({'error': 'Invalid Table Parameter'}), 406
