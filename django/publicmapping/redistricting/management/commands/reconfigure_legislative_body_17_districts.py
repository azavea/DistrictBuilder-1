from django.core.management.base import BaseCommand
from django.db import connection

import subprocess

from redistricting.models import ComputedDistrictScore, Plan, ScoreFunction, Subject


class Command(BaseCommand):
    """
    A one-off command to reconfigure the app to accomodate new config for
    a second legislative body with 17 districts (while still preserving all
    templates and plans).
    """
    help = 'Reconfigure for legislative body with 17 districts'

    def handle(self, *args, **options):
        """
        Performs the steps
        """
        print('Reconfiguring for legislative body with 17 districts...')
        remove_score_config()
        download_pa_17_shapefile()
        configure_templates()
        print('Reconfiguration complete!')

def remove_score_config():
    """
    Call removescoreconfig management command
    """
    print('Calling removecoreconfig...')
    subprocess.check_call('./manage.py removescoreconfig', shell=True)

def download_pa_17_shapefile():
    """
    Fetches the shapefile and unzips it. This is because data is not persisted in the container.
    """
    print('Fetching and unzipping shapefile')
    subprocess.check_call('wget -q -O /data/districtbuilder_data.zip http://s3.amazonaws.com/global-districtbuilder-data-us-east-1/pa/pa_3785_w_17.zip', shell=True)
    subprocess.check_call('unzip -o /data/districtbuilder_data.zip -d /data', shell=True)

def configure_templates():
    """
    Configure templates
    """
    print('Configure templates')
    subprocess.check_call('./manage.py setup config/config.xml -t', shell=True)
