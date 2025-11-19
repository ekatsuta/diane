import { Outlet, NavLink, useNavigate, useLocation } from 'react-router-dom';
import { useUserStore } from '@/stores/userStore';
import { UserHeader } from '@/components/UserHeader';
import { Home, CheckSquare, Calendar, ShoppingCart } from 'lucide-react';

const MainLayout = () => {
  const user = useUserStore((state) => state.user);
  const clearUser = useUserStore((state) => state.clearUser);
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    clearUser();
    navigate('/login');
  };

  const navLinks = [
    { to: '/', label: 'Home', icon: Home },
    { to: '/tasks', label: 'Tasks', icon: CheckSquare },
    { to: '/shopping', label: 'Shopping', icon: ShoppingCart },
    { to: '/calendar', label: 'Calendar', icon: Calendar },
  ];

  return (
    <div className="min-h-screen bg-paper-cream relative pb-20">
      <UserHeader userName={user?.first_name || user?.email || ''} onLogout={handleLogout} />

      {/* Main Content */}
      <main className="px-6 pt-24 pb-8">
        <Outlet />
      </main>

      {/* Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 bg-paper-white/95 backdrop-blur-sm border-t-2 border-line-warm">
        <div className="max-w-4xl mx-auto flex items-center justify-around py-4">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const isActive =
              link.to === '/' ? location.pathname === '/' : location.pathname.startsWith(link.to);

            return (
              <NavLink
                key={link.to}
                to={link.to}
                className={`flex flex-col items-center gap-1 p-2 transition-colors ${
                  isActive ? 'text-terracotta' : 'text-charcoal-light hover:text-terracotta'
                }`}
              >
                <Icon className="w-5 h-5" strokeWidth={isActive ? 2 : 1.5} />
                <span className="text-xs">{link.label}</span>
              </NavLink>
            );
          })}
        </div>
      </nav>
    </div>
  );
};

export default MainLayout;
