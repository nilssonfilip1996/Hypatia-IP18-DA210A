/*
 * Author: Viktor Kullberg
 *
 * UART CONFIGURATION
 */ 
#include "asf.h"
#include "uart.h"


/* UART Control Register */
uint32_t *const p_UART_CR = (uint32_t *) 0x400E0800U;
/* UART Mode Register*/
uint32_t *const p_UART_MR = (uint32_t *) 0x400E0804U;
/* UART Status Register*/
uint32_t *const p_UART_SR = (uint32_t *) 0x400E0814U;
/* UART Receiver Holding Register*/
uint32_t *const p_UART_RHR = (uint32_t *) 0x400E0818U;
/* UART Transmit Holding Register*/
uint32_t *const p_UART_THR = (uint32_t *) 0x400E081CU;
/* UART Baud Rate Generator Register*/
uint32_t *const p_UART_BRGR = (uint32_t *) 0x400E0820U;

/************************************************************************/
/* Initialize the UART													*/
/************************************************************************/
void uart_config(uint32_t baud){
	/* reset and disable receiver & transmitter */
	UART_CR = UART_CR_RSTRX | UART_CR_RSTTX	| UART_CR_RXDIS | UART_CR_TXDIS;
	/* configure baud rate */
	UART_BRGR = (MCK >> 4) / baud;
	/* configure mode, normal, no parity */
	UART_MR = UART_MR_PAR_NO | UART_MR_CHMODE_NORMAL;
	/* enable receiver and transmitter, (transmitter for testing) */
	UART_CR = UART_CR_RXEN | UART_CR_TXEN;
	/* configure RX0 pin as pull-up, this works */
	ioport_set_pin_mode(PIO_PA8_IDX, IOPORT_MODE_PULLUP);	
}

/************************************************************************/
/* See if transmitter is ready                                         */
/************************************************************************/
int uart_transmitter_ready(void){
	return (UART_SR & UART_SR_TXRDY);
}


/************************************************************************/
/* See if reciever is ready                                             */
/************************************************************************/
int uart_receiver_ready(void){
	return (UART_SR & UART_SR_RXRDY);
}


/************************************************************************/
/* Send char, used for testing                                         */
/************************************************************************/
void uart_send_char(uint8_t chr){
	UART_THR = chr;
}

/************************************************************************/
/* Recieve char and return it                                           */
/************************************************************************/
char uart_receive_char(void){
	char chr = UART_RHR;
	return chr;
}