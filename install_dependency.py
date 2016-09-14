from urllib import request
import os

dependencies = [
    ('https://raw.githubusercontent.com/thomaspark/bootswatch/gh-pages/paper/bootstrap.min.css',
     'templates/css/bootstrap.min.css'),
    ('https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js',
     'templates/js/bootstrap.min.js'),
    ('https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js',
     'templates/js/jquery-3.1.0.min.js')
]

for dep, dest in dependencies:
    print('Copying file to {}'.format(dest))
    dest_dir = os.path.dirname(dest)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    request.urlretrieve(dep, dest)
