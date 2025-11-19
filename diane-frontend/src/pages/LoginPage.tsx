import { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '@/api/auth';
import { useUserStore } from '@/stores/userStore';
import { AuthLayout, AuthCard, AuthInput } from '@/components/auth';

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
    <AuthLayout>
      <AuthCard
        title="Welcome Back"
        onSubmit={handleSubmit}
        submitText="Sign In"
        linkText="Don't have an account? Sign up"
        linkHref="/signup"
        loading={loading}
        disabled={!email.trim()}
        error={error}
      >
        <AuthInput
          id="email"
          type="email"
          label="Email"
          value={email}
          onChange={setEmail}
          placeholder="you@example.com"
          disabled={loading}
          required
        />
      </AuthCard>
    </AuthLayout>
  );
};

export default LoginPage;
