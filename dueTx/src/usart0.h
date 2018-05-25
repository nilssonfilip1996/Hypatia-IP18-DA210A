/*
 * usart0.h
 *
 * Created: 2018-05-19
 *  Author: Filip Nilsson
 */ 


#ifndef UART_H_
#define UART_H_

void usart0_init(void);
void usart0_transmit(unsigned char data);
char usart0_receive(void);
extern uint8_t finalXYCoordinates[];		//Global
extern int recieve_flag;					//Global


#endif /* UART_H_ */