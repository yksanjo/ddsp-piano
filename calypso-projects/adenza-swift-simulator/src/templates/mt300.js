class MT300Template {
  generate(tradeData) {
    const tradeDate = this.formatDate(tradeData.tradeDate || new Date());
    const valueDate = this.formatDate(tradeData.valueDate || tradeData.tradeDate || new Date());
    const tradeId = tradeData.id || tradeData.trade_id || 'TRADE001';
    
    // Extract currencies from instrument (e.g., "USD/EUR")
    const currencies = this.extractCurrencies(tradeData.instrument || 'USD/EUR');
    const buyCurrency = currencies[0];
    const sellCurrency = currencies[1];
    const buyAmount = this.formatAmount(tradeData.notional || 0);
    const sellAmount = this.calculateSellAmount(tradeData.notional || 0, tradeData.rate || 1);

    // MT300 structure
    let message = '{1:F01BANKUS33AXXX1234567890}';
    message += '{2:I300BANKGB22AXXXN}';
    message += '{4:';
    message += ':15A:';
    message += ':20:' + tradeId;
    message += ':22A:NEWT';
    message += ':22C:' + tradeId;
    message += ':82A:/' + (tradeData.counterparty || 'COUNTERPARTY');
    message += ':87A:/' + (tradeData.ourBank || 'OURBANK');
    message += ':30T:' + tradeDate;
    message += ':30V:' + valueDate;
    message += ':36:' + (tradeData.rate || '1.0000');
    message += ':32B:' + buyCurrency + buyAmount;
    message += ':53A:/' + (tradeData.buyBank || 'BUYBANK');
    message += ':57A:/' + (tradeData.sellBank || 'SELLBANK');
    message += ':33B:' + sellCurrency + sellAmount;
    message += ':57A:/' + (tradeData.sellBank || 'SELLBANK');
    message += ':58A:/' + (tradeData.beneficiary || 'BENEFICIARY');
    message += '-}';
    message += '{5:{MAC:12345678}{CHK:ABCDEF123456}}';

    return message;
  }

  formatDate(date) {
    if (typeof date === 'string') {
      date = new Date(date);
    }
    const year = date.getFullYear().toString();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return year + month + day;
  }

  formatAmount(amount) {
    const formatted = Math.abs(amount).toFixed(2).replace('.', ',');
    return formatted.padStart(15, '0');
  }

  extractCurrencies(instrument) {
    const parts = instrument.split('/');
    return parts.length === 2 ? parts : ['USD', 'EUR'];
  }

  calculateSellAmount(buyAmount, rate) {
    return this.formatAmount(buyAmount * rate);
  }
}

module.exports = new MT300Template();

