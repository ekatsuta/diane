import { ReactNode, FormEvent } from 'react';
import { Link } from 'react-router-dom';
import { Loader2, ArrowRight } from 'lucide-react';

interface AuthCardProps {
  title: string;
  onSubmit: (e: FormEvent) => void;
  children: ReactNode;
  submitText: string;
  linkText: string;
  linkHref: string;
  loading: boolean;
  disabled: boolean;
  error?: string;
}

export const AuthCard = ({
  title,
  onSubmit,
  children,
  submitText,
  linkText,
  linkHref,
  loading,
  disabled,
  error,
}: AuthCardProps) => {
  return (
    <div className="bg-paper-cream border-2 border-line-warm shadow-none rounded-xl flex flex-col gap-6">
      <div className="px-6 pt-6 pb-6 border-b border-line-warm">
        <h2 className="text-2xl text-center text-charcoal leading-none">{title}</h2>
      </div>

      <form onSubmit={onSubmit} className="space-y-6">
        {children}

        {error && (
          <div className="px-6">
            <div className="p-4 bg-blush-light/30 border border-line-warm rounded-lg">
              <p className="text-sm text-terracotta-dark">{error}</p>
            </div>
          </div>
        )}

        <div className="px-6 pb-6">
          <button
            type="submit"
            disabled={disabled || loading}
            className="w-full inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg font-medium transition-all bg-terracotta text-paper-white hover:bg-terracotta-dark border-0 shadow-none py-6 group outline-none disabled:pointer-events-none disabled:opacity-50"
          >
            {loading ? (
              <div className="flex items-center justify-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin" strokeWidth={1.5} />
                <span>Please wait...</span>
              </div>
            ) : (
              <div className="flex items-center justify-center gap-2">
                <span>{submitText}</span>
                <ArrowRight
                  className="w-4 h-4 group-hover:translate-x-1 transition-transform"
                  strokeWidth={1.5}
                />
              </div>
            )}
          </button>
        </div>
      </form>

      <div className="px-6 pb-6 pt-6 border-t border-line-warm text-center">
        <Link
          to={linkHref}
          className="text-warm-gray hover:text-terracotta transition-colors text-sm underline"
        >
          {linkText}
        </Link>
      </div>
    </div>
  );
};
