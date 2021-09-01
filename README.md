
 The provided usernames are checked on over 350 websites within few seconds. The goal behind this tool was to get results quickly while maintaining low amounts of false positives.

## Features

* **Fast**, lookup can complete **under 20 seconds**
* Over **350** platforms are included
* Batch processing
    * GET request with data in browser address bar
    * POST request with data in Json
    * Return Json response with find Usernames and URLs

## Installation

```bash
git clone site
cd api_search_usename_on_sites
python -r requirements.txtt
```

## Usage

```bash
Run server: uvicorn fast_app:app --reload
Open browser and follow http://127.0.0.1:8000/docs where you can test code

# Single username
http://127.0.0.1:8000/username/Alex

# Multiple *%* separated usernames
http://127.0.0.1:8000/username_list/Alex%Nikol%Sam