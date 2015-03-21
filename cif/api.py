from flask import Flask, session, redirect, url_for, escape, request
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import logging
import textwrap
import time
import ujson as json

from pprint import pprint


from cif import LOG_FORMAT

# https://github.com/mitsuhiko/flask/blob/master/examples/minitwit/minitwit.py

app = Flask(__name__)
logger = logging.getLogger(__name__)

# @app.before_request
# def before_request():
#     return 'true'

@app.route("/")
def help():
    pprint(request)
    return "Hello World!"

@app.route("/search")
def search():
    pprint(request.headers['User-Agent'])
    q = request.args.get('q')
    return q

@app.route("/observables", methods=['GET', 'POST'])
def observables():
    return "Observables"

@app.route("/ping", methods=['GET', 'POST'])
def ping():
    return str(time.time())

def main():
    parser = ArgumentParser(
        description=textwrap.dedent('''\
        example usage:
            $ cif-api -d
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='wf'
    )

    parser.add_argument("-v", "--verbose", dest="verbose", action="count",
                        help="set verbosity level [default: %(default)s]")
    parser.add_argument('-d', '--debug', dest='debug', action="store_true")

    args = parser.parse_args()

    loglevel = logging.WARNING
    if args.verbose:
        loglevel = logging.INFO
    if args.debug:
        loglevel = logging.DEBUG

    console = logging.StreamHandler()
    logging.getLogger('').setLevel(loglevel)
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger('').addHandler(console)

    options = vars(args)
    app.run(debug=options.get('debug'))

if __name__ == "__main__":
    main()