submissions-scraper
-------------------

This script is a work-around to getting data about submissions into a submissions csv (pulled from the `redistricting_plansubmissions` table). It scrapes the submissions report HTML for each submission line in the CSV and adds `competitiveness`, `split_counties`, `majority_minority`, `compactness`, and `population_equivalence` to each line.

# Pre-requisites

To use the script, you need to:
 - Install Golang on your machine.
 - Download the submissions CSV. You can do this by running `\copy (SELECT * FROM redistricting_plansubmission) TO '/tmp/submissions.csv' WITH CSV HEADER` on psql shell and extracting the file down to local.
 - Download the submission reports HTMLs. Generate each report using the management command in the Django docker container. `./manage.py submission_report {ID}`.

# Usage

```sh
go build main.go
./main path/to/submissions.csv path/to/submissions/report/dir/
```

The result will be in in `output.csv`. It will omit the submission report HTML files that you did not have in your directory and will log a list of the missing files to stdout.
