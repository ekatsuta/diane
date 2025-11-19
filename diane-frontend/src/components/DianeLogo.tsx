import { Mic } from 'lucide-react';

interface DianeLogoProps {
  size?: 'sm' | 'md' | 'lg';
  showIcon?: boolean;
}

export function DianeLogo({ size = 'md', showIcon = true }: DianeLogoProps) {
  const sizeClasses = {
    sm: 'text-2xl',
    md: 'text-4xl',
    lg: 'text-5xl',
  };

  const iconSizes = {
    sm: 'w-5 h-5',
    md: 'w-7 h-7',
    lg: 'w-8 h-8',
  };

  return (
    <div className="flex items-center gap-3">
      {showIcon && (
        <div className="relative">
          <Mic className={`${iconSizes[size]} text-terracotta`} strokeWidth={1.5} />
          <div className="absolute -bottom-0.5 -right-0.5 w-2 h-2 bg-terracotta rounded-full" />
        </div>
      )}
      <h1 className={`${sizeClasses[size]} text-charcoal font-serif`}>diane</h1>
    </div>
  );
}
