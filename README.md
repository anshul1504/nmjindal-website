# NM Jindal Global website

Premium dark-and-gold website for NM Jindal Global (import-export, agro focus). Django 5.2, Bootstrap 5, Poppins.
Live: https://nmjindalglobal.com

## What is editable from the admin (`/admin/`, Jazzmin theme)

Site settings (company, contact details, hero text, about), hero slides, products and categories, services,
insights (articles), regions, shipping terms, FAQs, mission / strengths / process / quality / document lists,
privacy and terms pages, and incoming enquiries.

## Run locally

```bash
python -m venv .venv && .venv\Scripts\activate      # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_content      # starting content and photos (only fills empty tables)
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ and http://127.0.0.1:8000/admin/.

## Configuration

Local development needs no setup. On a server, copy `.env.example` to `.env` and fill it in
(secret key, allowed hosts, SMTP mailbox). `.env`, the database and uploaded media are never committed.

## Enquiry emails

A submitted contact form emails the team (`Site settings > Send enquiries to`) and sends the visitor an
acknowledgement. Templates are in `core/templates/core/email/`. SMTP details come from `.env`.

## Deploy (cPanel, CloudLinux Python App)

1. Upload the project to an app folder and create a Python App (3.12) with startup file `passenger_wsgi.py`, entry point `application`.
2. Install `requirements.txt` into the app's virtualenv.
3. Create `.env` (see `.env.example`), then run `migrate`, `seed_content` and `collectstatic --noinput`.
4. Restart the app (`touch tmp/restart.txt`).

Static files are served by WhiteNoise; uploaded media by the WSGI layer (`config/wsgi.py`).

## Photos

Photo credits are in `CREDITS.md`. Source images are not stored in the repository; `tools/build_photos.py` documents how they were cropped.
