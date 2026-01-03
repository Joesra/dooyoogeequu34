from app import create_app
app = create_app()
client = app.test_client()
resp = client.get('/events/design1')
print('status:', resp.status_code)
print(resp.get_data(as_text=True)[:2000])
