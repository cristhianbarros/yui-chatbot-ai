from services.WhatsAppService  import whatsapp_service

class MessageHandler:

    def __init__(self):
        self.appointment_state = {}
        self.assistant_state = {}

    def handle_incoming_message(self, message, sender_info):

        if message.get('type') == 'text':
            incoming_message = message['text']['body'].lower().strip()

            if self.is_greeting(incoming_message):
                self.send_welcome_message(message['from'], message['id'], sender_info)
                self.send_welcome_menu(message['from'])
            elif incoming_message == 'media':
                self.send_media(message['from'])
            elif message['from'] in self.appointment_state:
                self.handle_appointment_flow(message['from'], incoming_message)
            elif message['from'] in self.assistant_state:
                self.handle_assistant_flow(message['from'], incoming_message)
            else:
                self.handle_menu_option(message['from'], incoming_message)
            whatsapp_service.mark_as_read(message['id'])
        elif message.get('type') == 'interactive':
            option = message.get('interactive', {}).get('button_reply', {}).get('id')
            #await self.handle_menu_option(message['from'], option)
            #await whatsapp_service.mark_as_read(message['id'])

    def is_greeting(self, message):
        greetings = ["hola", "hello", "hi", "buenas tardes"]
        return message in greetings

    def send_welcome_message(self, to, message_id, sender_info):
        name = self.get_sender_name(sender_info)
        welcome_message = f"Hola {name}, Bienvenido a Nolos Pizza, Tu pizzería favorita en línea. ¿En qué podemos ayudarte hoy?"
        whatsapp_service.send_message(to, welcome_message)

    def send_welcome_menu(self, to):
        menu_message = "Elige una Opción"
        buttons = [
            {'type': 'reply', 'reply': {'id': 'option_1', 'title': 'Realizar un Pedido'}},
            {'type': 'reply', 'reply': {'id': 'option_2', 'title': 'Consultar'}},
            {'type': 'reply', 'reply': {'id': 'option_3', 'title': 'Ubicación'}}
        ]
        whatsapp_service.send_interactive_buttons(to, menu_message, buttons)

    async def send_media(self, to):
        media_url = 'https://s3.amazonaws.com/gndx.dev/medpet-file.pdf'
        caption = '¡Esto es un PDF!'
        type = 'document'
        await whatsapp_service.send_media_message(to, type, media_url, caption)

    async def handle_appointment_flow(self, to, message):
        state = self.appointment_state[to]
        if state['step'] == 'name':
            state['name'] = message
            state['step'] = 'pet_name'
            response = "Gracias, Ahora, ¿Cuál es el nombre de tu Mascota?"
        elif state['step'] == 'pet_name':
            state['pet_name'] = message
            state['step'] = 'pet_type'
            response = '¿Qué tipo de mascota es? (por ejemplo: perro, gato, huron, etc.)'
        elif state['step'] == 'pet_type':
            state['pet_type'] = message
            state['step'] = 'reason'
            response = '¿Cuál es el motivo de la Consulta?'
        elif state['step'] == 'reason':
            state['reason'] = message
            response = self.complete_appointment(to)
        await whatsapp_service.send_message(to, response)

    async def handle_assistant_flow(self, to, message):
        """
        state = self.assistant_state[to]
        if state['step'] == 'question':
            response = await open_ai_service(message)
        del self.assistant_state[to]
        await whatsapp_service.send_message(to, response)
        menu_message = "¿La respuesta fue de tu ayuda?"
        buttons = [
            {'type': 'reply', 'reply': {'id': 'option_4', 'title': "Si, Gracias"}},
            {'type': 'reply', 'reply': {'id': 'option_5', 'title': 'Hacer otra pregunta'}},
            {'type': 'reply', 'reply': {'id': 'option_6', 'title': 'Emergencia'}}
        ]
        await whatsapp_service.send_interactive_buttons(to, menu_message, buttons)
        """

    def get_sender_name(self, sender_info):
        return sender_info.get('profile', {}).get('name') or sender_info.get('wa_id')

    async def handle_menu_option(self, to, option):
        if option == 'option_1':
            self.appointment_state[to] = {'step': 'name'}
            response = "Por favor, ingresa tu nombre:"
        elif option == 'option_2':
            self.assistant_state[to] = {'step': 'question'}
            response = "Realiza tu consulta"
        elif option == 'option_3':
            response = 'Te esperamos en nuestra sucursal.'
            await self.send_location(to)
        elif option == 'option_6':
            response = "Si esto es una emergencia, te invitamos a llamar a nuestra linea de atención"
            await self.send_contact(to)
        else:
            response = "Lo siento, no entendí tu selección, Por Favor, elige una de las opciones del menú."
        await whatsapp_service.send_message(to, response)

    async def send_contact(self, to):
        contact = {
            'addresses': [
                {
                    'street': "123 Calle de las Mascotas",
                    'city': "Ciudad",
                    'state': "Estado",
                    'zip': "12345",
                    'country': "País",
                    'country_code': "PA",
                    'type': "WORK"
                }
            ],
            'emails': [
                {
                    'email': "contacto@medpet.com",
                    'type': "WORK"
                }
            ],
            'name': {
                'formatted_name': "MedPet Contacto",
                'first_name': "MedPet",
                'last_name': "Contacto",
                'middle_name': "",
                'suffix': "",
                'prefix': ""
            },
            'org': {
                'company': "MedPet",
                'department': "Atención al Cliente",
                'title': "Representante"
            },
            'phones': [
                {
                    'phone': "+1234567890",
                    'wa_id': "1234567890",
                    'type': "WORK"
                }
            ],
            'urls': [
                {
                    'url': "https://www.medpet.com",
                    'type': "WORK"
                }
            ]
        }
        await whatsapp_service.send_contact_message(to, contact)

    async def send_location(self, to):
        latitude = 6.2071694
        longitude = -75.574607
        name = 'Platzi Medellín'
        address = 'Cra. 43A #5A - 113, El Poblado, Medellín, Antioquia.'
        await whatsapp_service.send_location_message(to, latitude, longitude, name, address)
    """
    def complete_appointment(self, to):
        appointment = self.appointment_state[to]
        del self.appointment_state[to]

        user_data = [
            to,
            appointment['name'],
            appointment['pet_name'],
            appointment['pet_type'],
            appointment['reason'],
            datetime.now().isoformat()
        ]

        append_to_sheet(user_data)

        return f"Gracias por agendar tu cita. \nResumen de tu cita:\n\nNombre: {appointment['name']}\nNombre de la mascota: {appointment['pet_name']}\nTipo de mascota: {appointment['pet_type']}\nMotivo: {appointment['reason']}\n\nNos pondremos en contacto contigo pronto para confirmar la fecha y hora de tu cita."
    """

message_handler = MessageHandler()