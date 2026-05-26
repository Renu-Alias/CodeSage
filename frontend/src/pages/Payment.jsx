import React, { useState } from 'react';
import { CreditCard, ChevronLeft, Shield, Check } from 'lucide-react';

const PLANS = {
  free: { name: 'Free', price: 0, period: '/month', color: 'var(--text-medium)' },
  pro: { name: 'Pro', price: 299, period: '/month', color: 'var(--brand)' },
  classroom: { name: 'Classroom', price: 999, period: '/month', color: 'var(--text-dark)' },
};

export default function Payment({ selectedPlan, setCurrentPage }) {
  const plan = PLANS[selectedPlan] || PLANS.pro;
  const [cardNumber, setCardNumber] = useState('');
  const [expiry, setExpiry] = useState('');
  const [cvv, setCvv] = useState('');
  const [name, setName] = useState('');
  const [processing, setProcessing] = useState(false);
  const [success, setSuccess] = useState(false);

  const formatCardNumber = (val) => {
    const digits = val.replace(/\D/g, '').slice(0, 16);
    return digits.replace(/(\d{4})(?=\d)/g, '$1 ');
  };

  const formatExpiry = (val) => {
    const digits = val.replace(/\D/g, '').slice(0, 4);
    if (digits.length > 2) return digits.slice(0, 2) + '/' + digits.slice(2);
    return digits;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setProcessing(true);
    setTimeout(() => {
      setProcessing(false);
      setSuccess(true);
    }, 1500);
  };

  if (success) {
    return (
      <div className="payment-page">
        <div className="payment-card payment-success">
          <div className="success-check"><Check size={40} /></div>
          <h2>Payment successful!</h2>
          <p>You're now on the <strong>{plan.name}</strong> plan. Start exploring all features.</p>
          <button className="btn btn-primary" onClick={() => setCurrentPage('dashboard')}>
            Go to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="payment-page">
      <div className="payment-card">
        <button className="payment-back-btn" onClick={() => setCurrentPage('home')}>
          <ChevronLeft size={18} /> Back
        </button>

        <div className="payment-plan-summary" style={{ borderLeftColor: plan.color }}>
          <span className="payment-plan-label">Selected plan</span>
          <span className="payment-plan-name">{plan.name}</span>
          <span className="payment-plan-price">
            {plan.price === 0 ? 'Free' : `₹${plan.price}`}
            {plan.price > 0 && <span className="payment-plan-period">{plan.period}</span>}
          </span>
        </div>

        <h2 className="payment-title">Payment details</h2>

        <form className="payment-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Cardholder name</label>
            <input
              className="auth-input"
              type="text"
              placeholder="John Doe"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Card number</label>
            <div className="input-wrapper">
              <CreditCard size={18} className="input-icon" />
              <input
                className="auth-input input-with-icon"
                type="text"
                placeholder="4242 4242 4242 4242"
                value={cardNumber}
                onChange={(e) => setCardNumber(formatCardNumber(e.target.value))}
                maxLength="19"
                required
              />
            </div>
          </div>

          <div className="payment-row">
            <div className="form-group">
              <label className="form-label">Expiry date</label>
              <input
                className="auth-input"
                type="text"
                placeholder="MM/YY"
                value={expiry}
                onChange={(e) => setExpiry(formatExpiry(e.target.value))}
                maxLength="5"
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">CVV</label>
              <input
                className="auth-input"
                type="text"
                placeholder="123"
                value={cvv}
                onChange={(e) => setCvv(e.target.value.replace(/\D/g, '').slice(0, 3))}
                maxLength="3"
                required
              />
            </div>
          </div>

          <div className="payment-security">
            <Shield size={16} />
            <span>Your payment info is secure and encrypted</span>
          </div>

          <button
            className="btn btn-primary payment-submit-btn"
            type="submit"
            disabled={processing}
          >
            {processing ? (
              <><span className="spinner" /> Processing...</>
            ) : (
              `Pay ${plan.price === 0 ? '₹0' : `₹${plan.price}`}`
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
