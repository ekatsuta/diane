interface AuthInputProps {
  id: string;
  type: string;
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
  disabled?: boolean;
  required?: boolean;
}

export const AuthInput = ({
  id,
  type,
  label,
  value,
  onChange,
  placeholder,
  disabled = false,
  required = false,
}: AuthInputProps) => {
  return (
    <div className="px-6">
      <label htmlFor={id} className="block text-xs mb-3 text-warm-gray uppercase tracking-widest">
        {label}
      </label>
      <input
        id={id}
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full border-0 border-b-2 border-line-warm rounded-none bg-transparent px-0 pb-2 focus:outline-none focus:ring-0 focus:border-terracotta transition-colors"
        disabled={disabled}
        required={required}
      />
    </div>
  );
};
