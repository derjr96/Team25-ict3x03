from __future__ import unicode_literals
from .common import SRPSessionBase
from .utils import hex_from, int_from_hex, int_to_bytes


if False:  # pragma: no cover
    from .context import SRPContext


class SRPServerSession(SRPSessionBase):

    role = 'server'

    def __init__(self, srp_context, password_verifier, private=None):
        """
        :param SRPContext srp_context:
        :param st|unicode password_verifier:
        :param st|unicode private:
        """
        super(SRPServerSession, self).__init__(srp_context, private)

        self._password_verifier = int_from_hex(password_verifier)

        if not private:
            self._this_private = srp_context.generate_server_private()

        self._server_public = srp_context.get_server_public(self._password_verifier, self._this_private)

    def init_session_key(self):
        super(SRPServerSession, self).init_session_key()

        premaster_secret = self._context.get_server_premaster_secret(
            self._password_verifier, self._this_private, self._client_public, self._common_secret)

        self._key = self._context.get_common_session_key(premaster_secret)

    def verify_proof(self, key_proof, base64=False):
        proof = self._context.get_common_session_key_proof(
            self._key, self._salt, self._server_public, self._client_public)
        
        return str(hex_from(proof).decode('utf-8')) == str(key_proof)
