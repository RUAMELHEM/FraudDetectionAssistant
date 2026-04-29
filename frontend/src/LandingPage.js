import './App.css';
import translations from './i18n';

const previewInvoices = [
  { id: 'INV-2024-001', vendor: 'Acme Corp',     amount: '$4,200', risk: 'high',   label: 'Duplicate'      },
  { id: 'INV-2024-002', vendor: 'Bright Studio',  amount: '$1,850', risk: 'medium', label: 'Missing Doc'    },
  { id: 'INV-2024-003', vendor: 'Fast Freight',   amount: '$920',   risk: 'low',    label: 'Clear'          },
  { id: 'INV-2024-004', vendor: 'Nova Services',  amount: '$3,100', risk: 'high',   label: 'Unusual Speed'  },
];

function LangToggle({ lang, setLang }) {
  return (
    <button
      className="lang-toggle"
      onClick={() => setLang(lang === 'en' ? 'ar' : 'en')}
      title="Switch language"
    >
      {translations[lang].lang_btn}
    </button>
  );
}

function RiskBadge({ risk, label }) {
  return <span className={`badge badge-${risk}`}>{label}</span>;
}

function DashboardPreview() {
  return (
    <div className="dashboard-card">
      <div className="dashboard-header">
        <span className="dashboard-title">Invoice Risk Overview</span>
        <span className="dashboard-date">Apr 28, 2026</span>
      </div>
      <div className="risk-score-row">
        <div className="risk-score-circle">
          <svg viewBox="0 0 36 36" className="risk-circle-svg">
            <path className="circle-bg"   d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
            <path className="circle-fill" strokeDasharray="72, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
            <text x="18" y="20.35" className="circle-text">72%</text>
          </svg>
          <div className="risk-label">Overall Risk</div>
        </div>
        <div className="risk-stats">
          <div className="stat"><span className="stat-dot high"   />2 High Risk</div>
          <div className="stat"><span className="stat-dot medium" />1 Needs Review</div>
          <div className="stat"><span className="stat-dot low"    />1 Clear</div>
        </div>
      </div>
      <div className="invoice-list">
        {previewInvoices.map(inv => (
          <div key={inv.id} className="invoice-row">
            <div className="invoice-info">
              <span className="invoice-id">{inv.id}</span>
              <span className="invoice-vendor">{inv.vendor}</span>
            </div>
            <span className="invoice-amount">{inv.amount}</span>
            <RiskBadge risk={inv.risk} label={inv.label} />
          </div>
        ))}
      </div>
    </div>
  );
}

function FeatureCard({ icon, title, desc }) {
  return (
    <div className="feature-card">
      <div className="feature-icon">{icon}</div>
      <h3 className="feature-title">{title}</h3>
      <p className="feature-desc">{desc}</p>
    </div>
  );
}

function StepCard({ num, title, desc }) {
  return (
    <div className="step-card">
      <div className="step-num">{num}</div>
      <h4 className="step-title">{title}</h4>
      <p className="step-desc">{desc}</p>
    </div>
  );
}

function TestimonialCard({ quote, name, role }) {
  return (
    <div className="testimonial-card">
      <p className="testimonial-quote">"{quote}"</p>
      <div className="testimonial-author">
        <div className="author-avatar">{name[0]}</div>
        <div>
          <div className="author-name">{name}</div>
          <div className="author-role">{role}</div>
        </div>
      </div>
    </div>
  );
}

export default function LandingPage({ lang, setLang, onStartFree }) {
  const t   = translations[lang];
  const dir = lang === 'ar' ? 'rtl' : 'ltr';

  return (
    <div className="app" dir={dir}>

      <nav className="nav">
        <div className="nav-inner">
          <div className="logo">
            <span className="logo-icon">⚑</span>
            <span className="logo-text">FraudGuard</span>
          </div>
          <div className="nav-links">
            <a href="#features">{t.nav_features}</a>
            <a href="#how">{t.nav_how}</a>
            <a href="#testimonials">{t.nav_stories}</a>
          </div>
          <div className="nav-actions">
            <LangToggle lang={lang} setLang={setLang} />
            <button onClick={onStartFree} className="btn btn-ghost">{t.nav_login}</button>
            <button onClick={onStartFree} className="btn btn-primary">{t.nav_start}</button>
          </div>
        </div>
      </nav>

      <section className="hero">
        <div className="hero-inner">
          <div className="hero-text">
            <div className="hero-eyebrow">{t.hero_eyebrow}</div>
            <h1 className="hero-headline">
              {t.hero_headline.split('\n').map((line, i) => (
                <span key={i}>{line}{i === 0 && <br />}</span>
              ))}
            </h1>
            <p className="hero-sub">{t.hero_sub}</p>
            <div className="hero-ctas">
              <button onClick={onStartFree} className="btn btn-primary btn-lg">{t.hero_cta1}</button>
              <a href="#how" className="btn btn-outline btn-lg">{t.hero_cta2}</a>
            </div>
            <p className="hero-note">{t.hero_note}</p>
          </div>
          <div className="hero-visual">
            <DashboardPreview />
          </div>
        </div>
      </section>

      <section className="trust-bar">
        <p className="trust-label">{t.trust_label}</p>
        <div className="trust-logos">
          {['Notion', 'Stripe', 'QuickBooks', 'Xero', 'Wave'].map(name => (
            <div key={name} className="trust-logo">{name}</div>
          ))}
        </div>
      </section>

      <section className="features section" id="features">
        <div className="section-inner">
          <div className="section-label">{t.feat_label}</div>
          <h2 className="section-title">{t.feat_title}</h2>
          <p className="section-sub">{t.feat_sub}</p>
          <div className="features-grid">
            <FeatureCard icon="⊘" title={t.feat1_title} desc={t.feat1_desc} />
            <FeatureCard icon="⚠" title={t.feat2_title} desc={t.feat2_desc} />
            <FeatureCard icon="⟳" title={t.feat3_title} desc={t.feat3_desc} />
            <FeatureCard icon="◉" title={t.feat4_title} desc={t.feat4_desc} />
          </div>
        </div>
      </section>

      <section className="how section" id="how">
        <div className="section-inner">
          <div className="section-label">{t.how_label}</div>
          <h2 className="section-title">{t.how_title}</h2>
          <div className="steps-row">
            <StepCard num="1" title={t.step1_title} desc={t.step1_desc} />
            <div className="step-connector" />
            <StepCard num="2" title={t.step2_title} desc={t.step2_desc} />
            <div className="step-connector" />
            <StepCard num="3" title={t.step3_title} desc={t.step3_desc} />
          </div>
        </div>
      </section>

      <section className="control section">
        <div className="control-inner">
          <div className="control-visual">
            <div className="control-illustration">
              <div className="ci-person">
                <div className="ci-head" />
                <div className="ci-body" />
              </div>
              <div className="ci-arrow">→</div>
              <div className="ci-doc">
                <div className="ci-doc-line" />
                <div className="ci-doc-line short" />
                <div className="ci-doc-badge">Review</div>
              </div>
            </div>
          </div>
          <div className="control-text">
            <div className="section-label">{t.ctrl_label}</div>
            <h2 className="control-title">
              {t.ctrl_title.split('\n').map((line, i) => (
                <span key={i}>{line}{i === 0 && <br />}</span>
              ))}
            </h2>
            <p className="control-desc">{t.ctrl_desc}</p>
            <ul className="control-list">
              <li>{t.ctrl_li1}</li>
              <li>{t.ctrl_li2}</li>
              <li>{t.ctrl_li3}</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="testimonials section" id="testimonials">
        <div className="section-inner">
          <div className="section-label">{t.test_label}</div>
          <h2 className="section-title">{t.test_title}</h2>
          <div className="testimonials-grid">
            <TestimonialCard quote={t.test1_quote} name={t.test1_name} role={t.test1_role} />
            <TestimonialCard quote={t.test2_quote} name={t.test2_name} role={t.test2_role} />
          </div>
        </div>
      </section>

      <section className="cta-section section" id="cta">
        <div className="cta-inner">
          <h2 className="cta-title">{t.cta_title}</h2>
          <p className="cta-sub">{t.cta_sub}</p>
          <button onClick={onStartFree} className="btn btn-primary btn-xl">{t.cta_btn}</button>
        </div>
      </section>

      <footer className="footer">
        <div className="footer-inner">
          <div className="footer-brand">
            <span className="logo-icon">⚑</span>
            <span className="logo-text">FraudGuard</span>
          </div>
          <div className="footer-links">
            <a href="#features">{t.nav_features}</a>
            <a href="#how">{t.nav_how}</a>
            <a href="#cta">{t.foot_pricing}</a>
            <a href="#cta">{t.foot_privacy}</a>
            <a href="#cta">{t.foot_terms}</a>
            <a href="#cta">{t.foot_contact}</a>
          </div>
          <p className="footer-copy">{t.foot_copy}</p>
        </div>
      </footer>

    </div>
  );
}
