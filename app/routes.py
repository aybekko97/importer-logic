import pandas as pd
from flask import request, Response, jsonify
from flask_cors import cross_origin

from app import app, db, models

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def import_to_db(io):
    df = pd.read_excel(io, dtype='object')
    df.columns = ['fullname', 'index', 'mail_id', 'weight', 'cost']

    records = df.to_dict('records')

    # errors = []
    # for (ind, record) in enumerate(records, 2):
    #     error = models.Order.validate(record)
    #     if error:
    #         error['row'] = ind
    #         errors.append(error)
    #
    # if errors:
    #     return jsonify({'code': 400, 'message': errors}), 200


    try:
        db.session.bulk_insert_mappings(models.Order, records)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 400, 'message': str(e)}), 200

    return jsonify({'code': 201, 'message': 'Success!'}), 200


@app.route('/import', methods=['POST'])
@cross_origin()
def upload_file():
    file = request.files.get('file', None)

    if file is None or file.filename == '':
        return jsonify({'code': 404, 'message': "Couldn't find a file to upload!"}), 200

    if file and allowed_file(file.filename):
        res = import_to_db(file.stream)
        return res

    return jsonify({'code': 403, 'message': 'File format is not allowed! Only xls, xlsx.'}), 200


@app.route('/', methods=['GET'])
@cross_origin()
def get_orders():
    orders = models.Order.query.all()
    result = {'orders': [order.as_dict() for order in orders]}
    return jsonify(result)


@app.route('/', methods=['DELETE'])
@cross_origin()
def delete_all():
    models.Order.query.delete()  # Don't do this in production!
    db.session.commit()
    return Response(status=200)
