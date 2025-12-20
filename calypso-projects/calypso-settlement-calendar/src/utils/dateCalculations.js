class DateCalculations {
  calculateSettlementDate(tradeDate, currencyPair, holidays = []) {
    const [baseCurrency, quoteCurrency] = currencyPair.split('/');
    const settlementDays = this.getSettlementDays(baseCurrency, quoteCurrency);
    
    let settlementDate = new Date(tradeDate);
    settlementDate.setDate(settlementDate.getDate() + settlementDays);

    // Skip holidays
    while (this.isHoliday(settlementDate, holidays)) {
      settlementDate.setDate(settlementDate.getDate() + 1);
    }

    return settlementDate;
  }

  getSettlementDays(baseCurrency, quoteCurrency) {
    // T+2 for most currency pairs
    const tPlus2Pairs = ['USD', 'EUR', 'GBP', 'JPY'];
    
    if (tPlus2Pairs.includes(baseCurrency) && tPlus2Pairs.includes(quoteCurrency)) {
      return 2;
    }

    // T+1 for some pairs
    if (baseCurrency === 'USD' && quoteCurrency === 'CAD') {
      return 1;
    }

    // Default T+2
    return 2;
  }

  isHoliday(date, holidays) {
    const dateStr = date.toISOString().split('T')[0];
    return holidays.some(holiday => {
      const holidayDate = new Date(holiday.date).toISOString().split('T')[0];
      return holidayDate === dateStr;
    });
  }
}

module.exports = new DateCalculations();



