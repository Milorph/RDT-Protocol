def create_checksum(packet_wo_checksum):
    """create the checksum of the packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet_wo_checksum: the packet byte data (including headers except for checksum field)

    Returns:
      the checksum in bytes

    """

    if len(packet_wo_checksum) % 2 == 1:
        packet_wo_checksum += b'\x00'  # make byte count even

    total = 0
    for i in range(0, len(packet_wo_checksum), 2):
        
        word = (packet_wo_checksum[i] << 8) + packet_wo_checksum[i + 1]
        total += word
        
        #adding overflow back to the total
        total = (total & 0xFFFF) + (total >> 16)

    # Perform one's complement of the total sum
    checksum = ~total & 0xFFFF
    return checksum.to_bytes(2, byteorder='big')
  
def verify_checksum(packet):
    """verify packet checksum (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet: the whole (including original checksum) packet byte data

    Returns:
      True if the packet checksum is the same as specified in the checksum field
      False otherwise

    """
    original_checksum = packet[8:10]  # checksum is at bytes 9-10
    data_to_verify = packet[:8] + packet[10:]  # Exclude the checksum bytes

    # Calculate the checksum on the data to verify
    calculated_checksum = create_checksum(data_to_verify)

    # Compare the calculated checksum with the original checksum
    return calculated_checksum == original_checksum

def make_packet(data_str, ack_num, seq_num):
    """Make a packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      data_str: the string of the data (to be put in the Data area)
      ack: an int tells if this packet is an ACK packet (1: ack, 0: non ack)
      seq_num: an int tells the sequence number, i.e., 0 or 1

    Returns:
      a created packet in bytes

    """
    
    # make sure your packet follows the required format!
    
    HEADER = b'COMPNETW'
    MAX_DATA_LENGTH = 1000

    # Main.py says its string but just in case, check for others
    if isinstance(data_str, str):
        data_bytes = data_str.encode()[:MAX_DATA_LENGTH]
    elif isinstance(data_str, bytes):
        data_bytes = data_str[:MAX_DATA_LENGTH]
    else:
        raise ValueError("Data must be a string or bytes")

    data_length = len(data_bytes) + 12  # Total length

    # Combine length, ack_num, and seq_num into two bytes
    length_and_control = (data_length << 2) | (ack_num << 1) | seq_num
    length_and_control_bytes = length_and_control.to_bytes(2, byteorder='big')

    checksum_bytes = create_checksum(HEADER + length_and_control_bytes + data_bytes)

    # Constructing the packet
    packet = HEADER + checksum_bytes + length_and_control_bytes + data_bytes
    return packet


###### These three functions will be automatically tested while grading. ######
###### Hence, your implementation should NOT make any changes to         ######
###### the above function names and args list.                           ######
###### You can have other helper functions if needed.                    ######  
