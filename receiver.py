import time 
# importing sleep only causes time to be undefined, since the assignment mentioned that we could use time.sleep()
# I just imported the whole time module and used only time.sleep()
from socket import *
from util import verify_checksum, make_packet

class Receiver:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(('localhost', 10155)) 
        self.expected_seq_num = 0  # First seq num should be 0
        self.packet_count = 0 

    def start(self):
        while True:
            packet, addr = self.sock.recvfrom(1024)  # Receive our packet from sender
            self.packet_count += 1  
            print(f"packet num.{self.packet_count} received: {packet}")

            # modulo 6 of packet count will cause timeout
            if self.packet_count % 6 == 0:
                print("simulating packet loss: sleep a while to trigger timeout event on the send side...")
                time.sleep(5)  # Cause the timeout
                
            # If there is no timeout send ack
            else: 
                # Simulate corruption for packets divisible by 3, but not those also divisible by 6
                is_corrupted = self.packet_count % 3 == 0 and self.packet_count % 6 != 0

                if not is_corrupted and verify_checksum(packet) and self.has_correct_seq(packet, self.expected_seq_num):
                    data = packet[12:]  # Data starts at byte 12 so get everything after
                    print(f"packet is expected, message string delivered: {data.decode()}")
                    self.send_ack(self.expected_seq_num, addr)
                    print("packet is delivered, now creating and sending the ACK packet...")
                    self.expected_seq_num = 1 - self.expected_seq_num
                else:
                    print("simulating packet bit errors/corrupted: ACK the previous packet!")
                    self.send_ack(1 - self.expected_seq_num, addr) 

            print("all done for this packet!\n")

    # Function help check if the seq is as expected
    def has_correct_seq(self, packet, seq):
        received_seq = packet[11] & 0x01 
        return received_seq == seq

    # Function to send the ack to the sender
    def send_ack(self, seq, addr):
        ack_packet = make_packet(b'', ack_num=1, seq_num=seq)
        self.sock.sendto(ack_packet, addr)

if __name__ == "__main__":
    receiver = Receiver()
    receiver.start()