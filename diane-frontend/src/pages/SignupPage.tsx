import { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { signup } from '@/api/auth';
import { useUserStore } from '@/stores/userStore';
import { AuthLayout, AuthCard, AuthInput } from '@/components/auth';

const SignupPage = () => {
  const [email, setEmail] = useState('');
  const [firstName, setFirstName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const setUser = useUserStore((state) => state.setUser);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const user = await signup(email, firstName);
      setUser(user);
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to sign up. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout>
      <AuthCard
        title="Create Account"
        onSubmit={handleSubmit}
        submitText="Create Account"
        linkText="Already have an account? Sign in"
        linkHref="/login"
        loading={loading}
        disabled={!email.trim() || !firstName.trim()}
        error={error}
      >
        <AuthInput
          id="firstName"
          type="text"
          label="Your Name"
          value={firstName}
          onChange={setFirstName}
          placeholder="Alex"
          disabled={loading}
          required
        />
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

export default SignupPage;
