/*
 *
 * Functions for sending and recieving over UART
 */ 

#include <asf.h>
#ifndef UART_FUNCTIONS_H_
#define UART_FUNCTIONS_H_

extern void send_char(uint8_t);
extern uint8_t read_char(void);
extern uint8_t read_when_ready(void);




#endif /* UART_FUNCTIONS_H_ */