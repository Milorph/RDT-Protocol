from socket import *
from util import make_packet, verify_checksum

class Sender:
    
    def __init__(self):
        """ 
        Your constructor should not expect any argument passed in,
        as an object will be initialized as follows:
        sender = Sender()
        
        Please check the main.py for a reference of how your function will be called.
        """
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.settimeout(4)  # 4 second timeout
        self.address = ('localhost', 10155) # based on my su id, the calculation of 10100 + (4178555 % 500) = 10155
        self.seq_num = 0 # start with sequence num 0
        self.packet_count = 0
        
    def rdt_send(self, app_msg_str):
        """realibly send a message to the receiver (MUST-HAVE DO-NOT-CHANGE)

        Args:
            app_msg_str: the message string (to be put in the data field of the packet)

        """
        # First make the packet
        self.packet_count += 1
        packet = make_packet(app_msg_str.encode(), ack_num=0, seq_num=self.seq_num)

        print(f"original message string: {app_msg_str}")
        print(f"packet created: {packet}")
        print(f"packet num.{self.packet_count} is successfully sent to the receiver.")

        #Send the packet
        self.send_packet(packet, app_msg_str)
        print()

    def send_packet(self, packet, app_msg_str):
        while True:
            try:
                self.sock.sendto(packet, self.address)
                # Wait for the acknowledgment from the receiver
                ack, _ = self.sock.recvfrom(1024)
                
                # Check checksum and ack coming back if correct
                if (verify_checksum(ack) and self.is_ack(ack, self.seq_num)):
                    print(f"packet is received correctly: seq. num {self.seq_num} - ACK num. {self.seq_num}. all done!")
                    self.seq_num = 1 - self.seq_num 
                    break
                else:
                    # If ack is for previous pkt based on the modulo 3 but not 6 then resend packet
                    print("receiver acked the previous pkt, resend!")
                    self.packet_count += 1
                    print()
                    print(f"[ACK.Previous retransmission]: {app_msg_str}")
                    print(f"packet num.{self.packet_count} is successfully sent to the receiver.")
                    
            # When simulating the timeout, run this
            except timeout:
                print("socket timeout! Resend!")
                self.packet_count += 1
                print()
                print(f"[timeout retransmission]: {app_msg_str}")
                print(f"packet num.{self.packet_count} is successfully sent to the receiver.")
                

    def is_ack(self, packet, expected_seq):
        
        ack_flag = (packet[11] >> 1) & 0x01 # Getting the 15th bit of the 11th and 12th byte
        ack_seq_num = packet[11] & 0x01 # Getting the 16th bit of the 11th and 12th byte
        return ack_flag == 1 and ack_seq_num == expected_seq # Return bool for the expected
    

if __name__ == "__main__":
    # note: no arguments will be passed in
    sender = Sender() 

    for i in range(1, 8):
        # this is where your rdt_send will be called
        sender.rdt_send('msg' + str(i))

  ####### Your Sender class in sender.py MUST have the rdt_send(app_msg_str)  #######
  ####### function, which will be called by an application to                 #######
  ####### send a message. DO NOT change the function name.                    #######                    
  ####### You can have other functions if needed.                             #######   