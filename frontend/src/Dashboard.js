import { useState } from 'react';
import './Dashboard.css';
import translations from './i18n';

// ── Static invoice data ───────────────────────────────────
const INVOICES = [
  { id: 'INV-001', client: 'Acme Corp',     amount: '$4,200', date: 'Apr 20', risk: 87, status: 'Flagged', duplicate: 'warning', documents: 'missing',  behavior: 'warning' },
  { id: 'INV-002', client: 'Bright Studio', amount: '$1,850', date: 'Apr 22', risk: 54, status: 'Review',  duplicate: 'ok',      documents: 'missing',  behavior: 'warning' },
  { id: 'INV-003', client: 'Fast Freight',  amount: '$920',   date: 'Apr 23', risk: 12, status: 'Clear',   duplicate: 'ok',      documents: 'ok',       behavior: 'ok'      },
  { id: 'INV-004', client: 'Nova Services', amount: '$3,100', date: 'Apr 24', risk: 78, status: 'Flagged', duplicate: 'ok',      documents: 'ok',       behavior: 'warning' },
  { id: 'INV-005', client: 'Peak Supplies', amount: '$2,400', date: 'Apr 25', risk: 32, status: 'Clear',   duplicate: 'ok',      documents: 'ok',       behavior: 'ok'      },
  { id: 'INV-006', client: 'Zenith Co',     amount: '$5,600', date: 'Apr 26', risk: 91, status: 'Flagged', duplicate: 'warning', documents: 'missing',  behavior: 'warning' },
];

// ── Helpers ───────────────────────────────────────────────
const rc = s => s >= 70 ? 'high' : s >= 35 ? 'medium' : 'low';
const rl = (s, t) => s >= 70 ? t.risk_high : s >= 35 ? t.risk_medium : t.risk_low;

const statusLabel = (s, t) => ({ Flagged: t.st_flagged, Review: t.st_review, Clear: t.st_clear }[s] || s);

// ── SVG Icon ──────────────────────────────────────────────
const PATHS = {
  home:   'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6',
  doc:    'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
  swap:   'M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4',
  bell:   'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9',
  cog:    'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065zM15 12a3 3 0 11-6 0 3 3 0 016 0z',
  search: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z',
  x:      'M6 18L18 6M6 6l12 12',
  check:  'M5 13l4 4L19 7',
  flag:   'M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9',
  arrowl: 'M10 19l-7-7m0 0l7-7m-7 7h18',
};

function Icon({ name, size = 18 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor"
      strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
      <path d={PATHS[name]} />
    </svg>
  );
}

// ── Lang Toggle ───────────────────────────────────────────
function LangToggle({ lang, setLang }) {
  return (
    <button className="lang-toggle" onClick={() => setLang(lang === 'en' ? 'ar' : 'en')}>
      {translations[lang].lang_btn}
    </button>
  );
}

// ── Sidebar ───────────────────────────────────────────────
function Sidebar({ active, onNavigate, onBack, t }) {
  const nav = [
    { id: 'dashboard',    label: t.db_nav_dashboard,    icon: 'home'  },
    { id: 'invoices',     label: t.db_nav_invoices,      icon: 'doc'   },
    { id: 'transactions', label: t.db_nav_transactions,  icon: 'swap'  },
    { id: 'alerts',       label: t.db_nav_alerts,        icon: 'bell', badge: 3 },
    { id: 'settings',     label: t.db_nav_settings,      icon: 'cog'   },
  ];
  return (
    <aside className="db-sidebar">
      <div className="db-logo">
        <span className="db-logo-mark">⚑</span>
        <span className="db-logo-text">FraudGuard</span>
      </div>
      <nav className="db-nav">
        {nav.map(item => (
          <button
            key={item.id}
            className={`db-nav-btn${active === item.id ? ' active' : ''}`}
            onClick={() => onNavigate(item.id)}
          >
            <Icon name={item.icon} />
            <span>{item.label}</span>
            {item.badge && <span className="db-nav-badge">{item.badge}</span>}
          </button>
        ))}
      </nav>
      <button className="db-back-btn" onClick={onBack}>
        <Icon name="arrowl" size={14} />
        {t.db_back}
      </button>
    </aside>
  );
}

// ── TopBar ────────────────────────────────────────────────
function TopBar({ notifCount, t, lang, setLang }) {
  return (
    <header className="db-topbar">
      <div className="db-search-wrap">
        <Icon name="search" size={15} />
        <input className="db-search-input" placeholder={t.db_search} />
      </div>
      <div className="db-topbar-right">
        <LangToggle lang={lang} setLang={setLang} />
        <button className="db-notif-btn">
          <Icon name="bell" size={18} />
          {notifCount > 0 && <span className="db-notif-dot">{notifCount}</span>}
        </button>
        <div className="db-avatar">JD</div>
      </div>
    </header>
  );
}

// ── Stat Cards ────────────────────────────────────────────
function StatCard({ label, value, sub, variant }) {
  return (
    <div className={`db-stat-card${variant ? ` db-stat-${variant}` : ''}`}>
      <div className="db-stat-value">{value}</div>
      <div className="db-stat-label">{label}</div>
      {sub && <div className="db-stat-sub">{sub}</div>}
    </div>
  );
}

// ── Risk Overview ─────────────────────────────────────────
function RiskOverview({ t }) {
  const score = 56;
  return (
    <div className="db-card db-risk-card">
      <div className="db-card-title">{t.risk_title}</div>
      <div className="db-risk-hero">
        <span className="db-risk-big medium">{score}%</span>
        <span className="db-risk-level medium">{t.risk_medium}</span>
      </div>
      <div className="db-progress-wrap">
        <div className="db-progress-gradient">
          <div className="db-progress-thumb" style={{ left: `${score}%` }} />
        </div>
        <div className="db-progress-labels">
          <span>{t.risk_l}</span><span>{t.risk_m}</span><span>{t.risk_h}</span>
        </div>
      </div>
      <p className="db-risk-note">{t.risk_note}</p>
    </div>
  );
}

// ── Alert Item ────────────────────────────────────────────
function AlertItem({ type, desc, risk, invoiceId, onReview, feedback, onFeedback, alertId, t }) {
  return (
    <div className={`db-alert risk-border-${risk}`}>
      <div className="db-alert-top">
        <span className={`db-risk-badge ${risk}`}>
          {risk === 'high' ? t.badge_high : t.badge_med}
        </span>
        <span className="db-alert-type">{type}</span>
      </div>
      <p className="db-alert-desc">{desc}</p>
      <div className="db-alert-footer">
        <div className="db-fb-inline">
          <span className="db-fb-label">{t.fb_correct}</span>
          <button className={`db-fb-btn${feedback === true  ? ' yes-active' : ''}`} onClick={() => onFeedback(alertId, true)}>👍</button>
          <button className={`db-fb-btn${feedback === false ? ' no-active'  : ''}`} onClick={() => onFeedback(alertId, false)}>👎</button>
        </div>
        <button className="db-review-btn" onClick={() => onReview(invoiceId)}>{t.review}</button>
      </div>
    </div>
  );
}

// ── Alerts Panel ──────────────────────────────────────────
function AlertsPanel({ onReview, feedback, onFeedback, t }) {
  const alerts = [
    { id: 1, invoiceId: 'INV-001', risk: 'high',   type: t.a1_type, desc: t.a1_desc },
    { id: 2, invoiceId: 'INV-002', risk: 'medium', type: t.a2_type, desc: t.a2_desc },
    { id: 3, invoiceId: 'INV-004', risk: 'high',   type: t.a3_type, desc: t.a3_desc },
  ];
  return (
    <div className="db-card db-alerts-card">
      <div className="db-card-header">
        <div className="db-card-title">{t.alerts_title}</div>
        <span className="db-count-badge">{alerts.length}</span>
      </div>
      <div className="db-alerts-list">
        {alerts.map(a => (
          <AlertItem key={a.id} {...a} alertId={a.id}
            onReview={onReview} feedback={feedback[a.id]} onFeedback={onFeedback} t={t} />
        ))}
      </div>
    </div>
  );
}

// ── Invoice Table ─────────────────────────────────────────
function InvoiceTable({ onSelect, selected, statuses, t }) {
  return (
    <div className="db-card db-table-card">
      <div className="db-card-header">
        <div className="db-card-title">{t.inv_title}</div>
        <span className="db-table-hint">{t.inv_hint}</span>
      </div>
      <div className="db-table-wrap">
        <table className="db-table">
          <thead>
            <tr>
              <th>{t.col_id}</th><th>{t.col_client}</th><th>{t.col_amount}</th>
              <th>{t.col_date}</th><th>{t.col_risk}</th><th>{t.col_status}</th>
            </tr>
          </thead>
          <tbody>
            {INVOICES.map(inv => {
              const status = statuses[inv.id] || inv.status;
              const rClass = rc(inv.risk);
              return (
                <tr
                  key={inv.id}
                  className={`db-table-row${selected?.id === inv.id ? ' selected' : ''}`}
                  onClick={() => onSelect(inv)}
                >
                  <td className="db-cell-id">{inv.id}</td>
                  <td>{inv.client}</td>
                  <td className="db-cell-amount">{inv.amount}</td>
                  <td className="db-cell-date">{inv.date}</td>
                  <td>
                    <div className="db-risk-cell">
                      <span className={`db-risk-pill ${rClass}`}>{inv.risk}%</span>
                      <div className="db-mini-bar">
                        <div className={`db-mini-fill ${rClass}`} style={{ width: `${inv.risk}%` }} />
                      </div>
                    </div>
                  </td>
                  <td>
                    <span className={`db-status ${status.toLowerCase()}`}>
                      {statusLabel(status, t)}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ── Issue Row ─────────────────────────────────────────────
function IssueRow({ label, state, t }) {
  const map = {
    ok:      { icon: '✓', cls: 'ok',   text: t.issue_ok      },
    warning: { icon: '⚠', cls: 'warn', text: t.issue_warn    },
    missing: { icon: '✗', cls: 'bad',  text: t.issue_missing },
  };
  const { icon, cls, text } = map[state] || map.ok;
  return (
    <div className={`db-issue-row ${cls}`}>
      <span className="db-issue-icon">{icon}</span>
      <span className="db-issue-label">{label}</span>
      <span className="db-issue-status">{text}</span>
    </div>
  );
}

// ── Detail Panel ──────────────────────────────────────────
function DetailPanel({ invoice, onClose, onMarkSafe, onFlagFraud, feedback, onFeedback, t, isRtl }) {
  const rClass = rc(invoice.risk);
  const status = invoice.status;
  return (
    <div className="db-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className={`db-detail${isRtl ? ' rtl-panel' : ''}`}>

        <div className="db-detail-header">
          <div>
            <div className="db-detail-id">{invoice.id}</div>
            <div className="db-detail-client">{invoice.client}</div>
          </div>
          <button className="db-close" onClick={onClose}><Icon name="x" size={18} /></button>
        </div>

        <div className="db-detail-meta">
          <div className="db-meta-pill">
            <span className="db-meta-k">{t.col_amount}</span>
            <span className="db-meta-v">{invoice.amount}</span>
          </div>
          <div className="db-meta-pill">
            <span className="db-meta-k">{t.col_date}</span>
            <span className="db-meta-v">{invoice.date}</span>
          </div>
          <div className="db-meta-pill">
            <span className="db-meta-k">{t.col_status}</span>
            <span className={`db-status ${status.toLowerCase()}`}>{statusLabel(status, t)}</span>
          </div>
        </div>

        <div className="db-detail-section">
          <div className="db-detail-section-title">{t.detail_breakdown}</div>
          <div className="db-issues">
            <IssueRow label={t.detail_dup}  state={invoice.duplicate}  t={t} />
            <IssueRow label={t.detail_docs} state={invoice.documents}  t={t} />
            <IssueRow label={t.detail_beh}  state={invoice.behavior}   t={t} />
          </div>
        </div>

        <div className="db-score-block">
          <div className="db-score-label">{t.detail_score}</div>
          <div className={`db-score-num ${rClass}`}>{invoice.risk}%</div>
          <div className={`db-score-level ${rClass}`}>{rl(invoice.risk, t)}</div>
        </div>

        <div className="db-detail-actions">
          <button className="db-action-safe"  onClick={() => onMarkSafe(invoice.id)}>
            <Icon name="check" size={15} />{t.act_safe}
          </button>
          <button className="db-action-fraud" onClick={() => onFlagFraud(invoice.id)}>
            <Icon name="flag"  size={15} />{t.act_fraud}
          </button>
        </div>

        <div className="db-feedback-block">
          <div className="db-fb-question">{t.fb_q}</div>
          <div className="db-fb-row">
            <button className={`db-fb-big yes${feedback === true  ? ' active' : ''}`} onClick={() => onFeedback(invoice.id, true)} >{t.fb_yes}</button>
            <button className={`db-fb-big no${feedback  === false ? ' active' : ''}`} onClick={() => onFeedback(invoice.id, false)}>{t.fb_no}</button>
          </div>
          {feedback !== undefined && <p className="db-fb-thanks">{t.fb_thanks}</p>}
        </div>

      </div>
    </div>
  );
}

// ── Placeholder ───────────────────────────────────────────
function Placeholder({ title, t }) {
  return (
    <div className="db-placeholder">
      <div className="db-placeholder-icon">◻</div>
      <div className="db-placeholder-title">{title}</div>
      <p className="db-placeholder-sub">{t.placeholder_sub}</p>
    </div>
  );
}

// ── Dashboard (main) ──────────────────────────────────────
export default function Dashboard({ lang, setLang, onBack }) {
  const [activeNav,       setActiveNav]       = useState('dashboard');
  const [selectedInvoice, setSelectedInvoice] = useState(null);
  const [statuses,        setStatuses]        = useState({});
  const [alertFeedback,   setAlertFeedback]   = useState({});
  const [invFeedback,     setInvFeedback]     = useState({});

  const t     = translations[lang];
  const isRtl = lang === 'ar';
  const dir   = isRtl ? 'rtl' : 'ltr';

  const handleReview    = id => { const inv = INVOICES.find(i => i.id === id); if (inv) setSelectedInvoice(inv); };
  const handleMarkSafe  = id => { setStatuses(p => ({ ...p, [id]: 'Clear'   })); setSelectedInvoice(null); };
  const handleFlagFraud = id => { setStatuses(p => ({ ...p, [id]: 'Flagged' })); setSelectedInvoice(null); };

  return (
    <div className="db-layout" dir={dir}>

      <Sidebar active={activeNav} onNavigate={setActiveNav} onBack={onBack} t={t} />

      <div className="db-main">
        <TopBar notifCount={3} t={t} lang={lang} setLang={setLang} />

        <div className="db-content">

          {activeNav === 'dashboard' && (
            <>
              <div className="db-page-head">
                <h1 className="db-page-title">{t.db_title}</h1>
                <p className="db-page-sub">{t.db_sub}</p>
              </div>

              <div className="db-stats-grid">
                <StatCard label={t.stat1_label} value="48"  sub={t.stat1_sub} />
                <StatCard label={t.stat2_label} value="12"  sub={t.stat2_sub} variant="danger"  />
                <StatCard label={t.stat3_label} value="56%" sub={t.stat3_sub} variant="warning" />
                <StatCard label={t.stat4_label} value="7"   sub={t.stat4_sub} />
              </div>

              <div className="db-mid-row">
                <RiskOverview t={t} />
                <AlertsPanel
                  onReview={handleReview}
                  feedback={alertFeedback}
                  onFeedback={(id, val) => setAlertFeedback(p => ({ ...p, [id]: val }))}
                  t={t}
                />
              </div>

              <InvoiceTable
                onSelect={setSelectedInvoice}
                selected={selectedInvoice}
                statuses={statuses}
                t={t}
              />
            </>
          )}

          {activeNav === 'invoices' && (
            <>
              <div className="db-page-head">
                <h1 className="db-page-title">{t.inv_page_title}</h1>
                <p className="db-page-sub">{t.inv_page_sub}</p>
              </div>
              <InvoiceTable onSelect={setSelectedInvoice} selected={selectedInvoice} statuses={statuses} t={t} />
            </>
          )}

          {activeNav === 'alerts' && (
            <>
              <div className="db-page-head">
                <h1 className="db-page-title">{t.alerts_page_title}</h1>
                <p className="db-page-sub">{t.alerts_page_sub}</p>
              </div>
              <AlertsPanel
                onReview={handleReview}
                feedback={alertFeedback}
                onFeedback={(id, val) => setAlertFeedback(p => ({ ...p, [id]: val }))}
                t={t}
              />
            </>
          )}

          {activeNav === 'transactions' && <Placeholder title={t.db_nav_transactions} t={t} />}
          {activeNav === 'settings'     && <Placeholder title={t.db_nav_settings}     t={t} />}

        </div>
      </div>

      {selectedInvoice && (
        <DetailPanel
          invoice={selectedInvoice}
          onClose={() => setSelectedInvoice(null)}
          onMarkSafe={handleMarkSafe}
          onFlagFraud={handleFlagFraud}
          feedback={invFeedback[selectedInvoice.id]}
          onFeedback={(id, val) => setInvFeedback(p => ({ ...p, [id]: val }))}
          t={t}
          isRtl={isRtl}
        />
      )}

    </div>
  );
}
