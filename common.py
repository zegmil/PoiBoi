# Preamble for basic client verification
HANDSHAKE_MESSAGE = b'proszemniewpuscicdotegoczolga'
CLIENT_LISTENING_PORT = 5006
SERVER_LISTENING_PORT = 5005
CLIENT_AUTH_ID_LENGTH = 16
PAYLOAD_LENGTH = 8
SERVER_FRAME_LENGTH = CLIENT_AUTH_ID_LENGTH + PAYLOAD_LENGTH
