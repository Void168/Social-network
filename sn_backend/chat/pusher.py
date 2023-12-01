import pusher
from dotenv import load_dotenv
import os

load_dotenv()

pusher_client = pusher.Pusher(
  app_id=os.environ.get('PUSHER_APP_ID'),
  key=os.environ.get('PUSHER_KEY'),
  secret=os.environ.get('PUSHER_SECRET'),
  cluster='ap1',
  ssl=os.environ.get('PUSHER_SSL') == 'True'
)