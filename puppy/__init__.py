from flask import Flask

app = Flask(__name__)

import puppy.views
import puppy.puppypopulator