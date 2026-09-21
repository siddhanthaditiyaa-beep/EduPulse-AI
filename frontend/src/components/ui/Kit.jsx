import React from 'react';

/*
  Shared building blocks for EduPulse AI.
  Kept deliberately few and reused everywhere so the app feels like one
  coherent place rather than 14 separately-styled screens. Every
  interactive element is sized for an easy tap/click and always pairs
  an icon with a text label — nothing here relies on an icon alone.
*/

const VARIANT_STYLES = {
  primary: 'bg-sun-500 hover:bg-sun-600 text-white shadow-[0_4px_0_0_rgba(233,111,34,0.55)] active:translate-y-0.5 active:shadow-none',
  ocean: 'bg-ocean-500 hover:bg-ocean-600 text-white shadow-[0_4px_0_0_rgba(35,76,107,0.45)] active:translate-y-0.5 active:shadow-none',
  soft: 'bg-white hover:bg-cream-soft text-ink border-2 border-ink/10',
  ghost: 'bg-transparent hover:bg-ocean-50 text-ocean-600',
  danger: 'bg-white hover:bg-coral-100 text-coral-600 border-2 border-coral-100',
};

const SIZE_STYLES = {
  md: 'text-base px-5 py-3',
  lg: 'text-lg px-7 py-4',
  sm: 'text-sm px-4 py-2.5',
};

export const Button = ({
  as: Tag = 'button',
  variant = 'primary',
  size = 'md',
  icon: Icon,
  iconRight: IconRight,
  loading = false,
  disabled = false,
  className = '',
  children,
  ...props
}) => (
  <Tag
    disabled={disabled || loading}
    className={`inline-flex items-center justify-center gap-2 rounded-2xl font-bold font-display tracking-normal transition-all duration-150 disabled:opacity-50 disabled:pointer-events-none whitespace-nowrap ${VARIANT_STYLES[variant]} ${SIZE_STYLES[size]} ${className}`}
    {...props}
  >
    {loading ? (
      <Spinner size={size === 'lg' ? 22 : 18} />
    ) : (
      <>
        {Icon && <Icon className={size === 'lg' ? 'w-6 h-6' : 'w-5 h-5'} strokeWidth={2.4} />}
        <span>{children}</span>
        {IconRight && <IconRight className={size === 'lg' ? 'w-6 h-6' : 'w-5 h-5'} strokeWidth={2.4} />}
      </>
    )}
  </Tag>
);

export const Spinner = ({ size = 20, className = '' }) => (
  <div
    className={`border-[3px] border-current border-t-transparent rounded-full animate-spin ${className}`}
    style={{ width: size, height: size }}
  />
);

export const Card = ({ className = '', padded = true, children, ...props }) => (
  <div
    className={`bg-paper rounded-3xl border-2 border-ink/[0.06] ${padded ? 'p-6' : ''} ${className}`}
    {...props}
  >
    {children}
  </div>
);

const BADGE_STYLES = {
  sun: 'bg-sun-100 text-sun-600',
  ocean: 'bg-ocean-100 text-ocean-600',
  meadow: 'bg-meadow-100 text-meadow-600',
  coral: 'bg-coral-100 text-coral-600',
  berry: 'bg-berry-100 text-berry-600',
  gold: 'bg-gold-400/25 text-sun-600',
};

export const Badge = ({ tone = 'ocean', icon: Icon, className = '', children }) => (
  <span
    className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-sm font-bold ${BADGE_STYLES[tone]} ${className}`}
  >
    {Icon && <Icon className="w-4 h-4" strokeWidth={2.6} />}
    {children}
  </span>
);

const BAR_TONES = {
  ocean: 'bg-ocean-500',
  sun: 'bg-sun-500',
  meadow: 'bg-meadow-500',
  berry: 'bg-berry-500',
};

export const ProgressBar = ({ value = 0, tone = 'meadow', className = '', height = 'h-4' }) => (
  <div className={`w-full ${height} rounded-full bg-ink/[0.07] overflow-hidden ${className}`}>
    <div
      className={`${height} rounded-full ${BAR_TONES[tone]} transition-all duration-500`}
      style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
    />
  </div>
);

export const PageHeader = ({ eyebrowIcon: EyebrowIcon, title, subtitle, action }) => (
  <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-8">
    <div>
      {EyebrowIcon && (
        <div className="w-11 h-11 rounded-2xl bg-ocean-500 text-white flex items-center justify-center mb-3 shadow-[0_3px_0_0_rgba(35,76,107,0.5)]">
          <EyebrowIcon className="w-6 h-6" strokeWidth={2.2} />
        </div>
      )}
      <h1 className="text-3xl sm:text-4xl font-display font-bold text-ink">{title}</h1>
      {subtitle && <p className="mt-1.5 text-ink-soft text-lg max-w-xl">{subtitle}</p>}
    </div>
    {action && <div className="shrink-0">{action}</div>}
  </div>
);

export const EmptyState = ({ icon: Icon, title, subtitle, action }) => (
  <Card className="flex flex-col items-center text-center py-14 px-6">
    {Icon && (
      <div className="w-16 h-16 rounded-full bg-ocean-50 text-ocean-500 flex items-center justify-center mb-4">
        <Icon className="w-8 h-8" strokeWidth={2} />
      </div>
    )}
    <h3 className="text-xl font-display font-bold text-ink mb-1.5">{title}</h3>
    {subtitle && <p className="text-ink-soft max-w-sm mb-5">{subtitle}</p>}
    {action}
  </Card>
);

export const Field = ({ label, icon: Icon, error, children }) => (
  <div>
    <label className="block text-base font-bold text-ink mb-2">{label}</label>
    <div className="relative">
      {Icon && <Icon className="w-5 h-5 text-ink-faint absolute left-4 top-1/2 -translate-y-1/2" />}
      {children}
    </div>
    {error && <p className="mt-1.5 text-sm font-semibold text-coral-600">{error}</p>}
  </div>
);

export const inputClass = (hasIcon = true) =>
  `w-full ${hasIcon ? 'pl-12' : 'pl-4'} pr-4 py-3.5 bg-cream-soft border-2 border-ink/10 rounded-2xl text-base text-ink placeholder:text-ink-faint focus:outline-hidden focus:border-ocean-500 focus:bg-white transition`;
