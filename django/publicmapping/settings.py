#
#   Copyright 2010 Micah Altman, Michael McDonald
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#   This file is part of The Public Mapping Project
#   http://sourceforge.net/projects/publicmapping/
#
#   Purpose:
#       Configuration settings for The Public Mapping Project
#
#       This file contains application settings for the web application,
#       The Public Mapping Project. This file requires a local configuration
#       file that contains site- and machine-specific configuration settings
#       in /projects/publicmapping/local/settings.ini
#
#   Author: David Zwarg, Andrew Jennings
#

from ConfigParser import RawConfigParser

config = RawConfigParser()
config.read('/projects/publicmapping/local/settings.ini')

# Django settings for publicmapping project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    (config.get('publicmapping','ADMIN_USER'), 
     config.get('publicmapping','ADMIN_EMAIL')),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'   # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = config.get('database','DATABASE_NAME')  # Or path to database file if using sqlite3.
DATABASE_USER = config.get('database', 'DATABASE_USER')  # Not used with sqlite3.
DATABASE_PASSWORD = config.get('database', 'DATABASE_PASSWORD')   # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/projects/publicmapping/trunk/django/publicmapping/site-media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site-media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to 
# use a trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = config.get('publicmapping','SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

# configure cache, according to guidelines for configuring django's
# cache framework: http://docs.djangoproject.com/en/1.0/topics/cache
#CACHE_BACKEND = 'locmem:///?timeout=3600&max_entries=400'
#CACHE_MIDDLEWARE_SECONDS = 3600
#CACHE_MIDDLEWARE_KEY_PREFIX = ''

# Middleware classes. Please note that cache middleware MUST be placed in
# the first and last positions of the middleware classes.  Order matters.
MIDDLEWARE_CLASSES = (
#    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.gzip.GZipMiddleware',
#    'django.middleware.cache.FetchFromCacheMiddleware',
)

AUTH_PROFILE_MODULE = 'redistricting.Profile'

ROOT_URLCONF = 'publicmapping.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/projects/publicmapping/trunk/django/publicmapping/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.gis',
    'redistricting',
)

#
# Settings specific to The Public Mapping Project
#

# Use the GIS test runner for django tests, since we are using geo features
TEST_RUNNER = 'django.contrib.gis.tests.run_tests'

# The database template to use to create test databases
POSTGIS_TEMPLATE='template_postgis'

# This is the base url for the application, where the login page is
LOGIN_URL = '/'

# The url of the geoserver instance where maps are stored
MAP_SERVER = config.get('publicmapping', 'MAP_SERVER')

# The id of the 'base geolevel', the smallest geounit of which the 
# other geounits are composed
BASE_GEOLEVEL = 3

# Declare the maximum number of districts allowed in a plan
MAX_DISTRICTS = 18

# The default subject to use when displaying maps on application entry
# This may be a subject ID, name, or display field
DEFAULT_DISTRICT_DISPLAY = 'POPTOT'

# The bard base shape that will be used to create bard reports.  This 
# should be a bardmap image containing data for the base geounits
BARD_BASESHAPE = '/projects/publicmapping/local/data/h_blocks.bardmap_bard_image.Rdata'

# The R variable of the basemap included in the BARD_BASESHAPE image.  
# Used to create BARD reports
BARD_BASEMAP = 'oh_blocks.bardmap'

# The POPTARGET RANGE variables are used to determine the class breaks for 
# the district choropleths
#
# Example: if the target is 100, POPTARGET_RANGE1 is .1 and 
# POPTARGET_RANGE2 is .2, anything between 90 and 110 is "on target", 
# anything between 80 and 90 or 110 and 120 is "under" or "over", 
# respectively, and anything less than 80 or more than 120 is "farunder" 
# or "farover", respectively
POPTARGET_RANGE1 = .1

# The POPTARGET RANGE variables are used to determine the class breaks for
# the district choropleths
# Example: if the target is 100, POPTARGET_RANGE1 is .1 and 
# POPTARGET_RANGE2 is .2, anything between 90 and 110 is "on target", 
# anything between 80 and 90 or 110 and 120 is "under" or "over", 
# respectively, and anything less than 80 or more than 120 is "farunder" 
# or "farover", respectively
POPTARGET_RANGE2 = .2

# Set up mail server settings. This is required for simple mailing 
# features, such as 'forgotten password' recovery, etc.
MAIL_SERVER = config.get('mailer', 'SERVER')
MAIL_PORT = config.get('mailer', 'PORT')
MAIL_USERNAME = config.get('mailer', 'USERNAME')
MAIL_PASSWORD = config.get('mailer', 'PASSWORD')

# Configure the location of the SLD files. These are used by the application
# to generate legend information regarding map choropleths.
SLD_ROOT = '/projects/publicmapping/trunk/sld/'

# Simplification tolerance. This determines just how much detail should be
# included in the 'simple' versions of the geometries in the District
# and Geounit models. The value is the amount, in spatial units, that the
# geometries will be simplified.
SIMPLE_TOLERANCE = 100.0
