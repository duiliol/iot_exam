/*
 * Copyright (C) 2015 Freie Universität Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

/**
 * @ingroup     examples
 * @{
 *
 * @file
 * @brief       Example application for demonstrating RIOT's MQTT-SN library
 *              emCute
 *
 * @author      Hauke Petersen <hauke.petersen@fu-berlin.de>
 *
 * @}
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#include "shell.h"
#include "msg.h"
#include "net/emcute.h"
#include "net/ipv6/addr.h"
#include "net/gnrc/netif.h"

#ifndef EMCUTE_ID
#define EMCUTE_ID           ("gertrud")
#endif
#define EMCUTE_PORT         (1883U)
#define EMCUTE_PRIO         (THREAD_PRIORITY_MAIN - 1)

#define NUMOFSUBS           (16U)
#define TOPIC_MAXLEN        (64U)

static char stack[THREAD_STACKSIZE_DEFAULT];
static msg_t queue[8];
static int dev_init = 0;

static emcute_sub_t subscriptions[NUMOFSUBS];
static char topics[NUMOFSUBS][TOPIC_MAXLEN];

typedef struct {
    char id[20];
    time_t timestamp;
    int temperature;
    int humidity;
    int wind_direction;
    int wind_intensity;
    int rain_height;
} Station;

int generate_sensor_value(int lower_bound, int upper_bound) {
    srand(time(NULL));
    return (rand() % (upper_bound + 1 - lower_bound) + lower_bound);
}

static void update_sensor_values(Station* upd_station){
    upd_station->timestamp = time(NULL);
    upd_station->temperature = generate_sensor_value(-50,50);
    upd_station->humidity = generate_sensor_value(0,100);
    upd_station->wind_direction = generate_sensor_value(0,360);
    upd_station->wind_intensity = generate_sensor_value(0,100);
    upd_station->rain_height = generate_sensor_value(0,50);
}

static void *emcute_thread(void *arg)
{
    (void)arg;
    emcute_run(EMCUTE_PORT, EMCUTE_ID);
    return NULL;    /* should never be reached */
}

static int connect_publish(char* address, int port, char* topic_name, char* message, int qos)
{
    //connect to gateway using its IP address and port
    sock_udp_ep_t gw = { .family = AF_INET6, .port = EMCUTE_PORT };
    char *topic = NULL;
    char *message = NULL;
    size_t len = 0;

    /* parse address */
    if (ipv6_addr_from_str((ipv6_addr_t *)&gw.addr.ipv6, address) == NULL) {
        printf("error parsing IPv6 address\n");
        return 1;
    }

    if (emcute_con(&gw, true, topic, message, len, 0) != EMCUTE_OK) {
        printf("error: unable to connect to [%s]:%i\n", argv[1], (int)gw.port);
        return 1;
    }
    printf("Successfully connected to gateway at [%s]:%i\n",
           address, port);

    //publish
    emcute_topic_t t;
    unsigned flags = EMCUTE_QOS_0;

    printf("publishing %s on topic %s\n", topic_name, message);

    /* step 1: get topic id and QoS level*/
    t.name = topic_name;
    if (emcute_reg(&t) != EMCUTE_OK) {
        puts("error: unable to obtain topic ID");
        return 1;
    }
    if(qos == 1)
        flags = EMCUTE_QOS_1;
    else if (qos == 2)
        flags = EMCUTE_QOS_2;

    /* step 2: publish data */
    if (emcute_pub(&t, message, strlen(message), flags) != EMCUTE_OK) {
        printf("error: unable to publish data to topic '%s [%i]'\n",
                t.name, (int)t.id);
        return 1;
    }

    printf("published %s on topic %s\n", t.name, message);

    //disconnect
    int res = emcute_discon();
    if (res == EMCUTE_NOGW) {
        puts("error: not connected to any broker");
        return 1;
    }
    else if (res != EMCUTE_OK) {
        puts("error: unable to disconnect");
        return 1;
    }
    puts("Disconnect successful");
    return 0;

}

static int cmd_init_start(int argc, char **argv)
{
    if (argc < 4) {
        printf("usage %s <station_id> <broker_address> <broker_port>\n", argv[0]);
        return 1;
    }

    Station local_station;
    sprintf(local_station.id,"%s",argv[1]);
    printf("Set station ID to %s\n",local_station.id);

    char broker_ip_address[128];
    int broker_port;
    sprintf(broker_ip_address,"%s",argv[2]);
    broker_port = atoi(argv[3]);
    /*printf("Attempting connection to broker %s:%d\n",broker_ip_address,broker_port);
    while(connect(broker_ip_address, broker_port)!=0){
        printf("Connection failed. Retrying...\n");
        sleep(5);
    }*/

    while(1){
        update_sensor_values(&local_station);
        char latest_read_json[255];
        char latest_timestamp[64];
        struct tm *lt = localtime(&local_station.timestamp);
        strftime(latest_timestamp,sizeof(latest_timestamp),"%FT%T",lt);
        sprintf(latest_read_json,"{\"id\": \"%s\", \"time\": \"%s\", \"temperature\": \"%d\", \"humidity\": \"%d\", \"wind_direction\": \"%d\", \"wind_intensity\": \"%d\", \"rain_height\": \"%d\"}",local_station.id, latest_timestamp, local_station.temperature, local_station.humidity, local_station.wind_direction, local_station.wind_intensity, local_station.rain_height);
        printf("%s\n",latest_read_json);
        connect_publish(broker_ip_address, broker_port,"sensor_values", latest_read_json, 0);
        /*publish("sensor_values",latest_read_json,0);*/
        sleep(10);
    }
    return 0;
}

static const shell_command_t shell_commands[] = {
    { "init_start", "initialize station and start sending values", cmd_init_start },
    { NULL, NULL, NULL }
};

int main(void)
{
    puts("RIOT-OS environmental station\n");
    puts("Type 'help' to get started. Have a look at the README.md for more"
         "information.");

    /* the main thread needs a msg queue to be able to run `ping6`*/
    msg_init_queue(queue, ARRAY_SIZE(queue));

    /* initialize our subscription buffers */
    memset(subscriptions, 0, (NUMOFSUBS * sizeof(emcute_sub_t)));

    /* start the emcute thread */
    thread_create(stack, sizeof(stack), EMCUTE_PRIO, 0,
                  emcute_thread, NULL, "emcute");

    /* start shell */
    char line_buf[SHELL_DEFAULT_BUFSIZE];
    shell_run(shell_commands, line_buf, SHELL_DEFAULT_BUFSIZE);

    /* should be never reached */
    return 0;
}
