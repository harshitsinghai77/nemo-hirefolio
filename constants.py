# JOBS_SCHEMA = [
#     "Company Name",
#     "Job Title",
#     "Link",
#     "Status",
#     "Applied",
#     "Application Method",
#     "Date",
#     "Contact Person",
#     "Cold Email Sent",
#     "Notes",
#     "Next Steps",
#     "key",
# ]

JOBS_SCHEMA = [
    {"name": "Company Name", "id": "company_name"},
    {"name": "Job Title", "id": "job_title", "width": 140},
    {"name": "Link", "id": "link"},
    {"name": "Status", "id": "status"},
    {"name": "Applied", "id": "applied"},
    {"name": "Application Method", "id": "application_method"},
    {"name": "Date", "id": "application_date", "width": 135},
    {"name": "Contact Person", "id": "contact_person"},
    {"name": "Cold Email Sent", "id": "cold_email_sent"},
    {"name": "Notes", "id": "notes"},
    {"name": "Next Steps", "id": "next_steps", "width": 310},
    {"name": "key", "id": "key", "editable": False},
]

JOBS_SCHEMA_SET = set(job['id'] for job in JOBS_SCHEMA)