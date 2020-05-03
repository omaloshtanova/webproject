from flask import Blueprint
from forms.public import *
from .utils import for_admins

admin = Blueprint('admin', __name__, template_folder='admin', url_prefix='/admin')


@admin.route('/')
@for_admins
def index():
    return ''