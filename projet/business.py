from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from projet.auth import login_required
from projet.db import get_db

bp = Blueprint('business', __name__)