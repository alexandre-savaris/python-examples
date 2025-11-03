import aiorun
import hl7
from hl7.mllp import open_hl7_connection
import asyncio

async def main():
    message = 'MSH|^~\&|GHH LAB|ELAB-3|GHH OE|BLDG4|200202150930||ORU^R01|CNTRL-3456|P|2.4\r'
    message += 'PID|||555-44-4444||EVERYWOMAN^EVE^E^^^^L|JONES|196203520|F|||153 FERNWOOD DR.^^STATESVILLE^OH^35292||(206)3345232|(206)752-121||||AC555444444||67-A4335^OH^20030520\r'
    message += 'OBR|1|845439^GHH OE|1045813^GHH LAB|1554-5^GLUCOSE|||200202150730||||||||555-55-5555^PRIMARY^PATRICIA P^^^^MD^^LEVEL SEVEN HEALTHCARE, INC.|||||||||F||||||444-44-4444^HIPPOCRATES^HOWARD H^^^^MD\r'
    message += 'OBX|1|SN|1554-5^GLUCOSE^POST 12H CFST:MCNC:PT:SER/PLAS:QN||^182|mg/dl|70_105|H|||F\r'

    # Open the connection to the HL7 receiver.
    # Using wait_for is optional, but recommended so
    # a dead receiver won't block for long.
    hl7_reader, hl7_writer = await asyncio.wait_for(
        open_hl7_connection('127.0.0.1', 2575),
        timeout=10,
    )

    hl7_message = hl7.parse(message)

    # Write the HL7 message, and then wait for the writer
    # to drain to actually send the message.
    hl7_writer.writemessage(hl7_message)
    await hl7_writer.drain()
    print(f'Sent message:\n{hl7_message}'.replace('\r', '\n'))

    # Now wait for the ACK message from the receiver.
    hl7_ack = await asyncio.wait_for(
        hl7_reader.readmessage(),
        timeout=10,
    )
    print(f'Received ACK:\n{hl7_ack}'.replace('\r', '\n'))

aiorun.run(main(), stop_on_unhandled_errors=True)
