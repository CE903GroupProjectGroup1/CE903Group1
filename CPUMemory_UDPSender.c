#include <errno.h>
#include <string.h>
#include <netdb.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <time.h>
#include <unistd.h>
#include <sys/resource.h>

int parseLine(char* line){
    // This assumes that a digit will be found and the line ends in " Kb".
	//this function removes the KB at the end of the value
    int i = strlen(line);
    const char* p = line;
    while (*p <'0' || *p > '9') p++;
    line[i-3] = '\0';
    i = atoi(p);
    return i;
}

double getCPU(){
	char c[10];
	FILE*prostf;
	long double a[7], b[7], cpuaggr, total,cpuUsage;

	//CPU FIRST Reading
	prostf = fopen("/proc/stat", "r");
	fscanf(prostf, "%s %Lf %Lf %Lf %Lf %Lf %Lf %Lf", c, &a[0], &a[1], &a[2], &a[3], &a[4], &a[5], &a[6]);
	fclose(prostf);	
	usleep(1000000);
	//CPU SECOND reading
	prostf = fopen("/proc/stat", "r");
	fscanf(prostf, "%s %Lf %Lf %Lf %Lf %Lf %Lf %Lf", c, &b[0], &b[1], &b[2], &b[3], &b[4], &b[5], &b[6]);
	fclose(prostf);

	cpuaggr = (b[0] + b[1] + b[2] + b[4] + b[5] + b[6])-(a[0] + a[1] + a[2] + a[4] + a[5] +a[6]);
	total= (b[0] + b[1] + b[2] +  b[3] + b[4] + b[5] + b[6])-(a[0] + a[1] + a[2] + a[3] + a[4] + a[5] +a[6]);
	cpuUsage=(cpuaggr/total) * 100;
	printf("The current CPU usage is : %Lf\n", cpuUsage);
	return cpuUsage	;
}

double getMemory(){
	char buff[128];
	FILE*prostf;
	int memFirst[4];
	long double total, loadavg,memoryUsage;

	//MEMORY Reading
	prostf = fopen("/proc/meminfo", "r");
	while (fgets(buff, 128, prostf)!= NULL){
		if (strncmp(buff, "MemTotal:", 7) == 0){
	   		memFirst[0] = parseLine(buff)/1024;
		}
		if (strncmp(buff, "MemFree:", 7) == 0){
	   		memFirst[1] = parseLine(buff)/1024;        
		}
		if (strncmp(buff, "Buffers:", 7) == 0){
	   		memFirst[2] = parseLine(buff)/1024;        
		}
		if (strncmp(buff, "Cached:", 3) == 0){
	   		memFirst[3] = parseLine(buff)/1024;
			 break;        
		}
	}
	fclose(prostf);

	loadavg = (memFirst[0]) - (memFirst[1]+memFirst[2]+memFirst[3]);
	total= (memFirst[0]);
	memoryUsage=(loadavg/total) * 100;
	printf("The current Memory usage is : %Lf\n", memoryUsage);
	return memoryUsage;

}

void ToString(char * outStr, double val)
	{
	    sprintf(outStr,"%.1f",val);
	}

int main(int argc, char**argv){
	char data[80];
	int handle = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP );

	struct sockaddr_in addr;

	 addr.sin_family = AF_INET;
	 addr.sin_port = htons(50065);
	 addr.sin_addr.s_addr = inet_addr("192.168.7.200");
	 memset(addr.sin_zero, '\0', sizeof addr.sin_zero);
	 int addr_size = sizeof addr;
	 
	
	while(1){
		int i=0;
		double CPU=0,Memory=0;
		while(i<10){
			CPU+= getCPU();
			Memory+=getMemory() ;
			usleep(1000000);
			i++;
		}
		CPU = CPU / 10;
		Memory = Memory / 10;
	
		//Get Time
		time_t time_raw_format;
	    	struct tm * ptr_time;
	    	char buffer[50];

	    	time ( &time_raw_format );
	    	ptr_time = localtime ( &time_raw_format );
	    	if(strftime(buffer,50,"%H:%M:%S %d.%m.%Y",ptr_time) == 0){
			perror("Couldn't prepare formatted string");
	    	}
	
		char CPUString[100] ;
		ToString(CPUString, CPU);
		char MemString[100] ; 
		ToString(MemString, Memory);
		char hostname[1024];
	    	gethostname(hostname, sizeof(hostname) -1);
		strcpy(data, hostname);
		strcat(data, ",");
		strcat(data,buffer);
		strcat(data,",");
		strcat(data, CPUString);
		strcat(data, ",");
		strcat(data, MemString);
		printf("%s\n", data);
		printf("Sending Message\n");
		int sent_bytes = sendto(handle, data, strlen(data), 0, (const struct sockaddr *)&addr, addr_size);
		if (sent_bytes < 0 ) {
			printf("Did not work\n");
		} else {
			printf("Should have worked\n");
		}
	}

	 

}



