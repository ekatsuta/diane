import { ReactNode } from 'react';
import { motion } from 'framer-motion';
import { DianeLogo } from '@/components/DianeLogo';

interface AuthLayoutProps {
  children: ReactNode;
}

export const AuthLayout = ({ children }: AuthLayoutProps) => {
  return (
    <div className="min-h-screen bg-paper-cream flex items-center justify-center p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md"
      >
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <DianeLogo size="lg" />
          </div>
          <p className="text-charcoal-light text-lg">
            Capture invisible labor
            <br />
            and organize your mental load
          </p>
        </div>

        {children}

        {/* Quote */}
        <div className="mt-8 text-center">
          <p className="text-charcoal-light italic text-sm">
            "The Bullet Journal is a mindfulness practice
            <br />
            disguised as a productivity system."
          </p>
          <p className="text-warm-gray text-xs mt-2">— Ryder Carroll</p>
        </div>
      </motion.div>
    </div>
  );
};
