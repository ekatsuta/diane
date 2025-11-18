import { useState, FormEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Loader2, ArrowRight } from 'lucide-react';
import { login } from '@/api/auth';
import { useUserStore } from '@/stores/userStore';
import { DianeLogo } from '@/components/DianeLogo';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const setUser = useUserStore((state) => state.setUser);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const user = await login(email);
      setUser(user);
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to log in. Please try again.');
    } finally {
      setLoading(false);
    }
  };

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

        {/* Auth Card */}
        <div className="bg-paper-white border-2 border-line-warm shadow-none rounded-xl flex flex-col gap-6">
          <div className="px-6 pt-6 pb-6 border-b border-line-warm">
            <h2 className="text-2xl text-center text-charcoal leading-none">Welcome Back</h2>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="px-6">
              <label className="block text-xs mb-3 text-warm-gray uppercase tracking-widest">
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="w-full border-0 border-b-2 border-line-warm rounded-none bg-transparent px-0 pb-2 focus:outline-none focus:ring-0 focus:border-terracotta transition-colors"
                disabled={loading}
                required
              />
            </div>

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
                disabled={loading || !email.trim()}
                className="w-full inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg font-medium transition-all bg-terracotta text-paper-white hover:bg-terracotta-dark border-0 shadow-none py-6 group outline-none disabled:pointer-events-none disabled:opacity-50"
              >
                {loading ? (
                  <div className="flex items-center justify-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin" strokeWidth={1.5} />
                    <span>Please wait...</span>
                  </div>
                ) : (
                  <div className="flex items-center justify-center gap-2">
                    <span>Sign In</span>
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
              to="/signup"
              className="text-warm-gray hover:text-terracotta transition-colors text-sm underline"
            >
              Don't have an account? Sign up
            </Link>
          </div>
        </div>

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

export default LoginPage;
