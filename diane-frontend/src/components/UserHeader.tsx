import { useState, useRef, useEffect } from 'react';
import { LogOut, ChevronDown, User } from 'lucide-react';
import { DianeLogo } from './DianeLogo';

interface UserHeaderProps {
  userName: string;
  onLogout: () => void;
}

export const UserHeader = ({ userName, onLogout }: UserHeaderProps) => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <header className="fixed top-0 left-0 right-0 bg-paper-white/95 backdrop-blur-sm border-b-2 border-line-warm z-10">
      <div className="max-w-4xl mx-auto px-6 py-4 flex justify-between items-center">
        {/* Logo */}
        <DianeLogo size="sm" />

        {/* User Dropdown */}
        <div className="relative" ref={dropdownRef}>
          <button
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            className="flex items-center gap-2 text-sm text-charcoal hover:text-terracotta transition-colors"
            aria-label="User menu"
          >
            <User className="w-4 h-4" strokeWidth={1.5} />
            <span>{userName}</span>
            <ChevronDown className="w-4 h-4" strokeWidth={1.5} />
          </button>

          {/* Dropdown Menu */}
          {isDropdownOpen && (
            <div className="absolute right-0 mt-2 w-48 bg-paper-white border-2 border-line-warm rounded-lg shadow-lg overflow-hidden">
              <button
                onClick={() => {
                  onLogout();
                  setIsDropdownOpen(false);
                }}
                className="w-full flex items-center gap-2 px-4 py-3 text-sm text-charcoal hover:bg-blush-light/20 transition-colors text-left"
              >
                <LogOut className="w-4 h-4" strokeWidth={1.5} />
                <span>Sign out</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
