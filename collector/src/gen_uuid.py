#!/usr/bin/python2.6

import sys
# this is only needed for the get_ghetto_uuid()
import uuid
from snowflakeclient.client import Client

CONFIG_PATH = '/scripts'

sys.path.append(CONFIG_PATH)
from configs import SNOWFLAKE_HOST, SNOWFLAKE_PORT, SNOWFLAKE_AGENT
from prov_logging import log_info


def get_ghetto_uuid():
    """
    Generate and return a universal unique identifier (UUID).

    In development mode, this UUID may be generated w/ Python's ``uuid``
    module.

    In production mode, the UUID should be generated by ``Snowflake``, a
    component created by Twitter for creating robust identifiers quickly.
    """
    # generate a 128 bit integer and shift it 66 places to create an
    # 18 digit  UUID
    return int(uuid.uuid1()) >> 66


def get_snowflake_uuid():
    """
    Generate and return a universal unique identifier using the Snowflake
    algorithm.

    This is the expect production mode and depends upon the Twitter component,
    ``Snowflake``.
    """
    client = Client(SNOWFLAKE_HOST, SNOWFLAKE_PORT)
    return client.get_id(SNOWFLAKE_AGENT)


def get_uuid(obj_data):
    """
    Provide a universal unique identifier.
    """
    log_info(obj_data)
    #return get_ghetto_uuid() # <= if you don't have snowflake deployed
    return get_snowflake_uuid()


# this was the previous implementation - I'm leaving it here for preserving it
    # host = 'localhost'
    # port = 7610

    # try:
    #   socket = TSocket.TSocket(host, port)
    #   transport = TTransport.TFramedTransport(socket)
    #   protocol = TBinaryProtocol.TBinaryProtocol(transport)
    #   client = Snowflake.Client(protocol)
    #   trans_out = transport.open()

    #   timestmp = client.get_timestamp()
    #   id = client.get_id("provenanceAPI")

    #   snflake_data = "[" + str(socket) + "," + str(transport) + "," +
    #                   str(protocol) + "," + str(client) + "," + str(trans_out)
    #                   + "," + str(timestmp) + "," + str(id) + "]"
    #   info_msg = snflake_data + " " + obj_data
    #   log_info(info_msg)

    #   return id
    # except Exception, e:
    #   err_msg = "Snowflake Server exception: " + str(e) + " " + obj_data
    #   log_exception(err_msg)
    #   failed_inserts_audit(obj_data)