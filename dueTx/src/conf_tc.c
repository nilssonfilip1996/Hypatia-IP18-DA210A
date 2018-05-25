/*
 * conf_tc.c
 *
 * Created: 2013-12-10 08:37:41
 *  Author: Tommy
 */ 

#include <asf.h>
#include "conf_tc.h"

#define FREQ 140			//timer frequency
#define CALC (42000000/FREQ)//Timer divisor calculation. Used to configure TC

/************************************************************************/
/* Initialize the Time Counter Interrupt on TC0                         */
/************************************************************************/
void configure_tc(void)
{
	/* Configure PMC */
	pmc_enable_periph_clk(ID_TC0);

	tc_init(TC0, 0, 0 | TC_CMR_CPCTRG);				//Timer_clock_1 - MCK/2 - 42 MHz
	tc_write_rc(TC0, 0, CALC);					

	/* Configure and enable interrupt on RC compare */
	NVIC_EnableIRQ((IRQn_Type) ID_TC0);
	tc_enable_interrupt(TC0, 0, TC_IER_CPCS);

	tc_start(TC0, 0);

}

