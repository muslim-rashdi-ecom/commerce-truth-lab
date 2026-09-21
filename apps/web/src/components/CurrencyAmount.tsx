import React from 'react';

interface CurrencyAmountProps {
  amount_minor: number;
  currency: string;
}

export const CurrencyAmount: React.FC<CurrencyAmountProps> = ({ amount_minor, currency }) => {
  const getFractionDigits = (curr: string) => {
    const code = curr.toUpperCase();
    if (code === 'JPY') return 0;
    if (code === 'KWD') return 3;
    return 2;
  };

  const fractionDigits = getFractionDigits(currency);
  const majorAmount = amount_minor / Math.pow(10, fractionDigits);

  const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency.toUpperCase(),
    minimumFractionDigits: fractionDigits,
    maximumFractionDigits: fractionDigits,
  });

  return <span>{formatter.format(majorAmount)}</span>;
};
