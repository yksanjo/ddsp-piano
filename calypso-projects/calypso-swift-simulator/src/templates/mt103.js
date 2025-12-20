class MT103Template {
  generate(tradeData) {
    const date = this.formatDate(tradeData.tradeDate || new Date());
    const amount = this.formatAmount(tradeData.notional || 0, tradeData.currency || 'USD');
    const counterparty = tradeData.counterparty || 'COUNTERPARTY';
    const tradeId = tradeData.id || tradeData.trade_id || 'TRADE001';

    // MT103 structure
    let message = '{1:F01BANKUS33AXXX1234567890}';
    message += '{2:I103BANKGB22AXXXN}';
    message += '{3:{113:SEPA}{108:' + tradeId + '}}';
    message += '{4:';
    message += ':20:' + tradeId;
    message += ':23B:CRED';
    message += ':32A:' + date + tradeData.currency + amount;
    message += ':50A:/' + counterparty;
    message += ':59:/' + (tradeData.beneficiary || counterparty);
    message += ':70:' + (tradeData.reference || 'Trade Payment');
    message += ':71A:SHA';
    message += '-}';
    message += '{5:{MAC:12345678}{CHK:ABCDEF123456}}';

    return message;
  }

  formatDate(date) {
    if (typeof date === 'string') {
      date = new Date(date);
    }
    const year = date.getFullYear().toString().substring(2);
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return year + month + day;
  }

  formatAmount(amount, currency) {
    const formatted = Math.abs(amount).toFixed(2).replace('.', ',');
    return formatted.padStart(15, '0');
  }
}

module.exports = new MT103Template();



