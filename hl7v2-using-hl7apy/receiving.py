from hl7apy.mllp import MLLPServer, AbstractHandler, AbstractErrorHandler
from hl7apy.parser import parse_message

# Define a handler for ADT_A01 messages.
class ADTA01Handler(AbstractHandler):
    def handle(self):
        # Parse the incoming message.
        message = parse_message(self.message)
        print(f'Received ADT_A01 message: {message.msh.msh_9.value}')

        # Create the ACK response.
        ack = self.create_ack()
        return ack.to_mllp()
    
# Define a handler for errors.
class MyErrorHandler(AbstractErrorHandler):
    def handle(self):
        print(f'Error occurred: {self.exception}')
        # Optionally, create an error ACK.
        err_ack = self.create_ack(ack_code='AE', text=str(self.exception))
        return err_ack.to_mllp()
    
# Define the handlers dictionary.
handlers = {
    'ADT_A01': (ADTA01Handler, {}),
    'ERR': (MyErrorHandler, {})
}

# Create and start the MLLP server.
HOST = 'localhost'
PORT = 17000
server = MLLPServer(HOST, PORT, handlers)


print(f'MLLP server listening on {HOST}:{PORT}...')
try:
    server.serve_forever()
except KeyboardInterrupt:
    print('Server stopped!')
    server.shutdown()
