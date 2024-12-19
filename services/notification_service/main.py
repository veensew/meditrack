from flask import Flask
from flask_restx import Api, Resource, fields
from flask_cors import CORS
from database import MongoDB
from models import Notification
from email_sender import EmailSender
from datetime import datetime
import asyncio
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app)

# Initialize Flask-RestX
api = Api(app, version='1.0',
          title='Notification Service API',
          description='A service for sending and managing notifications',
          doc='/',
          prefix='/api')

# Create namespace
ns = api.namespace('notifications', description='Notification operations')

# Define models for Swagger documentation
notification_model = api.model('Notification', {
    'recipient_email': fields.String(required=True, description='Recipient email address'),
    'subject': fields.String(required=True, description='Email subject'),
    'content': fields.String(required=True, description='Email content'),
    'status': fields.String(description='Notification status', enum=['pending', 'sent', 'failed']),
    'id': fields.String(description='Notification ID'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'sent_at': fields.DateTime(description='Sent timestamp')
})

notification_response = api.model('NotificationResponse', {
    'message': fields.String(description='Response message'),
    'error': fields.String(description='Error message if any')
})

db = MongoDB()
email_sender = EmailSender()

@ns.route('/send')
class SendNotification(Resource):
    @ns.expect(notification_model)
    @ns.response(200, 'Success', notification_response)
    @ns.response(500, 'Failed', notification_response)
    def post(self):
        """Send a new notification"""
        try:
            data = api.payload
            notification = Notification(
                recipient_email=data['recipient_email'],
                subject=data['subject'],
                content=data['content'],
                status='pending'
            )

            # Save notification to database
            db.insert_notification(notification.to_dict())

            # Send email
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            success = loop.run_until_complete(
                email_sender.send_email(
                    notification.recipient_email,
                    notification.subject,
                    notification.content
                )
            )
            loop.close()

            if success:
                db.update_notification_status(
                    notification.id,
                    "sent",
                    datetime.now()
                )
                return {"message": "Notification sent successfully"}, 200
            else:
                db.update_notification_status(notification.id, "failed")
                return {"error": "Failed to send notification"}, 500

        except Exception as e:
            return {"error": str(e)}, 500

@ns.route('/pending')
class PendingNotifications(Resource):
    @ns.response(200, 'Success', [notification_model])
    @ns.response(500, 'Failed', notification_response)
    def get(self):
        """Get all pending notifications"""
        try:
            notifications = db.get_pending_notifications()
            return [Notification.from_dict(notif).to_dict() for notif in notifications], 200
        except Exception as e:
            return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8004, debug=True)