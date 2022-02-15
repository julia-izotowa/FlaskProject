
import string

from http import HTTPStatus

from webargs import validate, fields
from webargs.flaskparser import use_kwargs

from database_handler import execute_query
from error_handler import error_handling

from flask import abort, Flask, Response


app = Flask(__name__)


@app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
@app.errorhandler(HTTPStatus.BAD_REQUEST)
def error_handler(error):
    return error_handling(error)


@app.route("/")
def hello_world():
    return "<p>Hello, Mykhailo!</p>"


@app.route("/stats-by-genre")
@use_kwargs(
    {
        "genre": fields.Str(
            required=False,
            missing='Hip Hop',
            validate=[validate.ContainsOnly(string.ascii_letters)]
        ),
    },
    location="query"
)
def stats_by_genre(genre):

    query = f'''
            SELECT i.BillingCity AS City,
                    g.Name AS Genre,
                COUNT(i.InvoiceId) AS CountListeners
            FROM genres g
                     left join tracks t on g.GenreId = t.GenreId
                     left join invoice_items ii on t.TrackId = ii.TrackId
                     inner join invoices i on ii.InvoiceId = i.InvoiceId
            WHERE g.Name LIKE '%{genre}%'
            GROUP BY g.Name, i.BillingCity
            ORDER BY CountListeners DESC
            LIMIT 1
          '''

    records = execute_query(query=query)
    if len(records) == 0:
        abort(Response("No data for your request..."))

    return f'Most people listen to {records[0][1]} in {records[0][0]}'


app.run(port=5007, debug=True)
