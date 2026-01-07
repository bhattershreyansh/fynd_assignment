import { createContext, useContext, useEffect, useState } from 'react';

interface DemoUser {
  id: string;
  email: string;
}

interface AuthContextType {
  user: DemoUser | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const DEMO_ADMIN = {
  email: 'admin@example.com',
  password: 'admin123',
};

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<DemoUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem('admin_user');
    if (stored) {
      setUser(JSON.parse(stored));
    }
    setLoading(false);
  }, []);

  const signIn = async (email: string, password: string) => {
    if (email === DEMO_ADMIN.email && password === DEMO_ADMIN.password) {
      const demoUser: DemoUser = {
        id: '1',
        email,
      };
      setUser(demoUser);
      localStorage.setItem('admin_user', JSON.stringify(demoUser));
    } else {
      throw new Error('Invalid credentials. Use admin@example.com / admin123');
    }
  };

  const signOut = async () => {
    setUser(null);
    localStorage.removeItem('admin_user');
  };

  return (
    <AuthContext.Provider value={{ user, loading, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
