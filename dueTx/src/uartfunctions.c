/*
 * 
 * Functions for testing sending and recieve chars
 */ 

#include "uart.h"
#include "uartfunctions.h"

/************************************************************************/
/* Send char, used fot testing                                          */
/************************************************************************/
void send_char(uint8_t chr){
	/*Wait for uart transmitter*/
	while (!uart_transmitter_ready());
	uart_send_char(chr);
}


/************************************************************************/
/* Reads char from register                                            */
/************************************************************************/
uint8_t read_char(void){
	/*Read char if receiver is ready*/
	if (uart_receiver_ready())
	{
		return uart_receive_char();
	}
	/*failed to read char*/
	return 0;
}

/************************************************************************/
/* Waits until reciever is ready and then reads register                */
/************************************************************************/
uint8_t read_when_ready(void){
	while (!uart_receiver_ready());
	return read_char();
}
