from services.http_request.send_to_whatsapp import send_to_whatsapp

class WhatsAppService:
    def send_message(self, to, body):
        data = {
            'messaging_product': 'whatsapp',
            'to': to,
            'text': {'body': body},
        }
        send_to_whatsapp(data)

    def send_interactive_buttons(self, to, body_text, buttons):
        data = {
            'messaging_product': 'whatsapp',
            'to': to,
            'type': 'interactive',
            'interactive': {
                'type': 'button',
                'body': {'text': body_text},
                'action': {
                    'buttons': buttons,
                },
            },
        }
        send_to_whatsapp(data)

    async def send_media_message(self, to, type, media_url, caption):
        media_object = {}

        if type == 'image':
            media_object['image'] = {'link': media_url, 'caption': caption}
        elif type == 'audio':
            media_object['audio'] = {'link': media_url}
        elif type == 'video':
            media_object['video'] = {'link': media_url, 'caption': caption}
        elif type == 'document':
            media_object['document'] = {'link': media_url, 'caption': caption, 'filename': 'medpet-file.pdf'}
        else:
            raise ValueError('Not Supported Media Type')

        data = {
            'messaging_product': 'whatsapp',
            'recipient_type': 'individual',
            'to': to,
            'type': type,
            **media_object,
        }
        await send_to_whatsapp(data)

    def mark_as_read(self, message_id):
        data = {
            'messaging_product': 'whatsapp',
            'status': 'read',
            'message_id': message_id,
        }
        send_to_whatsapp(data)

    async def send_contact_message(self, to, contact):
        data = {
            'messaging_product': 'whatsapp',
            'to': to,
            'type': 'contacts',
            'contacts': [contact],
        }
        await send_to_whatsapp(data)

    async def send_location_message(self, to, latitude, longitude, name, address):
        data = {
            'messaging_product': 'whatsapp',
            'to': to,
            'type': 'location',
            'location': {
                'latitude': latitude,
                'longitude': longitude,
                'name': name,
                'address': address,
            }
        }
        await send_to_whatsapp(data)

whatsapp_service = WhatsAppService()