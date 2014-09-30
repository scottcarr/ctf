#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <arpa/inet.h>


int main() {
    const char *hostname = "vortex.labs.overthewire.org";
    const char *port = "5842";
    int status;
    struct addrinfo hints;
    struct addrinfo *servinfo;  // will point to the results

    memset(&hints, 0, sizeof(hints)); // make sure the struct is empty
    hints.ai_family = AF_UNSPEC;     // don't care IPv4 or IPv6
    hints.ai_socktype = SOCK_STREAM; // TCP stream sockets
    //hints.ai_flags = AI_PASSIVE;     // fill in my IP for me

    if ((status = getaddrinfo(hostname, port, &hints, &servinfo)) != 0) {
        fprintf(stderr, "getaddrinfo error: %s\n", gai_strerror(status));
        exit(1);
    }
    int s;
    if (-1 == (s = socket(servinfo->ai_family, servinfo->ai_socktype, servinfo->ai_protocol))) {
        fprintf(stderr, "error: creating socket failed\n");
        exit(1);

    }
    if(connect(s, servinfo->ai_addr, servinfo->ai_addrlen)) {
        fprintf(stderr, "error: connecting failed\n");
        exit(1);
    }
    unsigned int is[4]; 
    for (int i = 0; i < 4; i++) {
        if (recv(s, &is[i], 4, 0) != 4) {
            fprintf(stderr, "error: recvd failed:\n");
            exit(1);
        }
    }
    int r2;
    unsigned int i1 = is[0] + is[1] + is[2] + is[3];
    send(s, &i1, 4, 0);
    char buf[1024];
    int r = recv(s, buf, 1024, 0);
    printf("%s\n", buf);
}
