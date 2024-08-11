import json
import socket
from logging import DEBUG, CRITICAL
import time
import ssl

from logger import logger

# set to true on debug environment only
ENABLE_DEBUG = False

# default connection properites
DEFAULT_XAPI_ADDRESS = "xapi.xtb.com"
DEFAULT_XAPI_PORT = 5124

# API inter-command timeout (in ms)
API_SEND_TIMEOUT = 100

# max connection tries
API_MAX_CONN_TRIES = 3

if ENABLE_DEBUG:
    logger.setLevel(DEBUG)
else:
    logger.setLevel(CRITICAL)


class JsonSocket(object):
    def __init__(self, address, port, encrypt=False):
        self._ssl = encrypt
        if self._ssl is not True:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket = ssl.wrap_socket(sock)
        self.conn = self.socket
        self._timeout = None
        self._address = address
        self._port = port
        self._decoder = json.JSONDecoder()
        self._receivedData = ""

    def connect(self):
        for i in range(API_MAX_CONN_TRIES):
            try:
                self.socket.connect((self.address, self.port))
            except socket.error as msg:
                logger.error("SockThread Error: %s" % msg)
                time.sleep(0.25)
                continue
            logger.info("Socket connected")
            return True
        return False

    def _sendObj(self, obj):
        msg = json.dumps(obj)
        self._waitingSend(msg)

    def _waitingSend(self, msg):
        if self.socket:
            sent = 0
            msg = msg.encode("utf-8")
            while sent < len(msg):
                sent += self.conn.send(msg[sent:])
                logger.info("Sent: " + str(msg))
                time.sleep(API_SEND_TIMEOUT / 1000)

    def _read(self, bytesSize=4096):
        if not self.socket:
            raise RuntimeError("socket connection broken")
        while True:
            char = self.conn.recv(bytesSize).decode()
            self._receivedData += char
            try:
                (resp, size) = self._decoder.raw_decode(self._receivedData)
                if size == len(self._receivedData):
                    self._receivedData = ""
                    break
                elif size < len(self._receivedData):
                    self._receivedData = self._receivedData[size:].strip()
                    break
            except ValueError:
                continue
        logger.info("Received: " + str(resp))
        return resp

    def _readObj(self):
        msg = self._read()
        return msg

    def close(self):
        logger.debug("Closing socket")
        self._closeSocket()
        if self.socket is not self.conn:
            logger.debug("Closing connection socket")
            self._closeConnection()

    def _closeSocket(self):
        self.socket.close()

    def _closeConnection(self):
        self.conn.close()

    def _get_timeout(self):
        return self._timeout

    def _set_timeout(self, timeout):
        self._timeout = timeout
        self.socket.settimeout(timeout)

    def _get_address(self):
        return self._address

    def _set_address(self, address):
        pass

    def _get_port(self):
        return self._port

    def _set_port(self, port):
        pass

    def _get_encrypt(self):
        return self._ssl

    def _set_encrypt(self, encrypt):
        pass

    timeout = property(_get_timeout, _set_timeout, doc="Get/set the socket timeout")
    address = property(
        _get_address, _set_address, doc="read only property socket address"
    )
    port = property(_get_port, _set_port, doc="read only property socket port")
    encrypt = property(_get_encrypt, _set_encrypt, doc="read only property socket port")


class APIClient(JsonSocket):
    def __init__(
        self, address=DEFAULT_XAPI_ADDRESS, port=DEFAULT_XAPI_PORT, encrypt=True
    ):
        super(APIClient, self).__init__(address, port, encrypt)
        if not self.connect():
            raise Exception(
                "Cannot connect to "
                + address
                + ":"
                + str(port)
                + " after "
                + str(API_MAX_CONN_TRIES)
                + " retries"
            )

    def execute(self, dictionary):
        self._sendObj(dictionary)
        return self._readObj()

    def disconnect(self):
        self.close()
