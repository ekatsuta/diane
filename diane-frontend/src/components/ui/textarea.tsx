import { TextareaHTMLAttributes } from 'react';

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  className?: string;
}

export const Textarea = ({ className = '', ...props }: TextareaProps) => {
  return (
    <textarea
      className={`w-full rounded-md border border-line-warm bg-paper-white px-3 py-2 text-sm ring-offset-paper-cream placeholder:text-warm-gray focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-terracotta focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${className}`}
      {...props}
    />
  );
};
