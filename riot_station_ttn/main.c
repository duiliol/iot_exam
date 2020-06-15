/*
 * Copyright (C) 2017 Inria
 *               2017 Inria Chile
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
 */

/**
 * @ingroup     tests
 *
 * @file
 * @brief       Semtech LoRaMAC test application
 *
 * @author      Alexandre Abadie <alexandre.abadie@inria.fr>
 * @author      Jose Alamos <jose.alamos@inria.cl>
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#ifdef MODULE_SEMTECH_LORAMAC_RX
#include "thread.h"
#include "msg.h"
#endif

#include "shell.h"
#include "semtech_loramac.h"

extern semtech_loramac_t loramac;

#ifdef MODULE_SEMTECH_LORAMAC_RX
#define LORAMAC_RECV_MSG_QUEUE                   (4U)
static msg_t _loramac_recv_queue[LORAMAC_RECV_MSG_QUEUE];
static char _recv_stack[THREAD_STACKSIZE_DEFAULT];

static void *_wait_recv(void *arg)
{
    msg_init_queue(_loramac_recv_queue, LORAMAC_RECV_MSG_QUEUE);

    (void)arg;
    while (1) {
        /* blocks until something is received */
        switch (semtech_loramac_recv(&loramac)) {
            case SEMTECH_LORAMAC_RX_DATA:
                loramac.rx_data.payload[loramac.rx_data.payload_len] = 0;
                printf("Data received: %s, port: %d\n",
                (char *)loramac.rx_data.payload, loramac.rx_data.port);
                break;

            case SEMTECH_LORAMAC_RX_LINK_CHECK:
                printf("Link check information:\n"
                   "  - Demodulation margin: %d\n"
                   "  - Number of gateways: %d\n",
                   loramac.link_chk.demod_margin,
                   loramac.link_chk.nb_gateways);
                break;

            case SEMTECH_LORAMAC_RX_CONFIRMED:
                puts("Received ACK from network");
                break;

            default:
                break;
        }
    }
    return NULL;
}
#endif

/* loramac shell command handler is implemented in
   sys/shell/commands/sc_loramac.c */

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

static int cmd_init_start(int argc, char **argv)
{
    if (argc < 1) {
        printf("usage %s <station_id>\n", argv[0]);
        return 1;
    }

    Station local_station;
    sprintf(local_station.id,"%s",argv[1]);
    printf("Set station ID to %s\n",local_station.id);

    while(1){
        update_sensor_values(&local_station);
        char latest_read_json[255];
        char latest_timestamp[64];
        struct tm *lt = localtime(&local_station.timestamp);
        strftime(latest_timestamp,sizeof(latest_timestamp),"%FT%T",lt);
        sprintf(latest_read_json,"{\"id\": \"%s\", \"time\": \"%s\", \"temperature\": \"%d\", \"humidity\": \"%d\", \"wind_direction\": \"%d\", \"wind_intensity\": \"%d\", \"rain_height\": \"%d\"}",local_station.id, latest_timestamp, local_station.temperature, local_station.humidity, local_station.wind_direction, local_station.wind_intensity, local_station.rain_height);
        printf("%s\n",latest_read_json);
        int ret_code = semtech_loramac_send(&loramac, (uint8_t *)latest_read_json, strlen(latest_read_json));
        if (ret_code == SEMTECH_LORAMAC_TX_DONE || ret_code == SEMTECH_LORAMAC_TX_OK) {
            puts("Message sent.");
        } else {
            printf("Failed to send message.\n");
        }
        xtimer_sleep(10);
    }
    return 0;
}

static const shell_command_t shell_commands[] = {
        { "init_start", "initialize station and start sending values", cmd_init_start },
        { NULL, NULL, NULL }
};

int main(void)
{
#ifdef MODULE_SEMTECH_LORAMAC_RX
    thread_create(_recv_stack, sizeof(_recv_stack),
                  THREAD_PRIORITY_MAIN - 1, 0, _wait_recv, NULL, "recv thread");
#endif

    puts("All up, running the shell now");
    char line_buf[SHELL_DEFAULT_BUFSIZE];
    shell_run(shell_commands, line_buf, SHELL_DEFAULT_BUFSIZE);
}
