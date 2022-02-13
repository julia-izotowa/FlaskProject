
import string

from http import HTTPStatus
from webargs import validate, fields
from webargs.flaskparser import use_kwargs

from database_handler import execute_query
from error_handler import error_handling
from utils import format_records

from flask import abort, Flask, Response


app = Flask(__name__)


@app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
@app.errorhandler(HTTPStatus.BAD_REQUEST)
def error_handler(error):
    return error_handling(error)


@app.route("/")
def hello_world():
    return "<p>Hello, Mykhailo!</p>"


@app.route("/order-price")
@use_kwargs(
    {
        "country": fields.Str(
            required=False,
            missing=None,
            validate=[validate.ContainsOnly(string.ascii_letters)]
        ),
    },
    location="query"
)
def order_price(country):

    country_condition = ""
    if country:
        country_condition = f" WHERE BillingCountry = '{country}'"

    query = f'''
           SELECT BillingCountry
           , SUM(UnitPrice * Quantity) AS OrderPrice
           FROM invoice_items left join invoices
           ON invoice_items.InvoiceId = invoices.InvoiceId
           {country_condition}
           GROUP BY BillingCountry;
       '''

    records = execute_query(query=query)
    if len(records) == 0:
        abort(Response("No data for your request..."))

    return format_records(records)


@app.route("/track-info")
def get_all_info_about_track():

    query = '''
            SELECT tracks.Name
             , tracks.Composer
             , tracks.Milliseconds AS Duration
             , tracks.Bytes AS FileSize
             , tracks.UnitPrice
             , albums.Title
             , artists.Name
             , genres.Name
             , media_types.Name
             , playlists.Name
        FROM tracks
                 left join albums on tracks.AlbumId = albums.AlbumId
                 left join artists on albums.ArtistId = artists.ArtistId
                 left join genres on tracks.GenreId = genres.GenreId
                 left join media_types on tracks.MediaTypeId = media_types.MediaTypeId
                 left join playlist_track on tracks.TrackId = playlist_track.TrackId
                 left join playlists on playlist_track.PlaylistId = playlists.PlaylistId
    '''

    records = execute_query(query=query)
    return format_records(records)


@app.route("/all-tracks-duration")
def get_all_tracks_duration():

    query = '''
            SELECT SUM(Milliseconds) AS Milliseconds
            FROM tracks
    '''

    records = execute_query(query=query)
    duration = records[0][0]/(1000*60*60)

    return f'Duration of all tracks {duration} hours'


app.run(port=5006, debug=True)
